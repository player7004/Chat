import socket
import rsa
from src.log import Log
from threading import Thread
from time import sleep
import datetime


class Server:
    def __init__(self, port, timeout):
        now = datetime.datetime.now()
        self.server_log = Log("server_log.txt")
        self.running = True
        self.timeout = timeout
        self.name = ""  # Имя сервера

        self.clients = []  # Список подключённых ip
        self.requests = {}  # Карта входящий сообщений адрес: сообщение
        self.clients_names = Log.read_and_return_dict("clients_names.txt")  # Карта ников пользователей адрес: имя

        self.public_key, self.private_key = rsa.newkeys(512)
        self.keys = [0 for i in range(3)]

        self.first_client = socket.socket()
        self.second_client = socket.socket()
        self.third_client = socket.socket()
        self.clients_info = [0 for i in range(3)]  # Индикатор загруженности соккетов
        self.client_map = {}  # Карта пользователей адрес: индекс
        self.max_clients = 3

        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('localhost', port))
        self.server_socket.listen()
        self.first_client.settimeout(timeout)
        self.second_client.settimeout(timeout)
        self.third_client.settimeout(timeout)

        self.server_log.save_message("\n\n{}\nServer initialized".format(str(now)))

    # set - функции

    def set_server_name(self, name):  # Уставляет имя сервера
        self.name = name
        self.server_log.save_message("Server name set to {}".format(name))

    # add - функции

    def add_user(self, address, sock_ind):  # Полноценно добавляет клинента
        if address == "localhost" or address == "127.0.0.1":
            self.clients.append("localhost")
            self.clients.append("127.0.0.1")
            self.client_map.update({"localhost": sock_ind, "127.0.0.1": sock_ind})
        else:
            self.clients.append(address)
            self.client_map.update({address: sock_ind})
        self.server_log.save_message("Added user: {} to sock {}".format(str(address), str(sock_ind)))

    def add_key(self, address, key):
        sock_ind = self.get_ind_by_address(address)
        self.keys[sock_ind] = key

    def add_user_name(self, address, name):  # Добавляет имя пользователя
        self.clients_names.update({address: name})
        self.server_log.save_message("Added name {} to user {}".format(name, address))

    def add_request(self, address, message):  # Добавляет сообщение от клиента
        self.requests.update({address: message})
        self.server_log.save_message("Added request from {}".format(address))

    # del - функции

    def del_user(self, address, sock_ind):  # Удаляет пользвателя из списка
        if address == "localhost" or "127.0.0.1":
            try:
                self.client_map.pop("localhost")
                self.client_map.pop("127.0.0.1")
            except KeyError:
                pass
            try:
                self.clients.remove("localhost")
                self.clients.remove("127.0.0.1")
            except ValueError:
                pass
        else:
            self.client_map.pop(address)
            self.clients.remove(address)
        self.server_log.save_message("Deleted user {} with socket {}".format(address, sock_ind))

    def del_key(self, address):
        sock_ind = self.get_ind_by_address(address)
        self.keys[sock_ind] = 0

    # server - функции

    def create_connection(self, address, port):  # Создаёт чат-сессию
        self.server_log.save_message("Creating connection with {}:{}".format(address, port))
        sock_ind = self.get_free_socket()
        self.server_log.save_message("Socket {}".format(sock_ind))
        if not sock_ind and sock_ind != 0:
            self.server_log.save_message("Failed to create connection: {}".format("All sockets are in use"))
            return OSError
        try:
            self.server_log.save_message("Trying to create connection with {}".format(address))
            thread = Thread(target=self.connect, args=(address, port, sock_ind))
            thread.start()
            thread.join(0)
            connection, address_1 = self.server_socket.accept()
            connection.settimeout(0.2)
            self.add_user(address, sock_ind)
        except OSError:
            self.server_log.save_message("Failed to create connection: {}".format("Socket is busy or offline"))
            return OSError
        self.raw_send(address, self.public_key.save_pkcs1())
        key = connection.recv(162)
        key = rsa.PublicKey.load_pkcs1(key)
        self.add_key(address, key)
        while self.running and self.clients_info[sock_ind]:
            try:
                data = connection.recv(4096)
            except socket.timeout:
                continue
            except OSError:
                self.server_log.save_message("Connection with {} lost".format(address))
                self.close_connection(address, sock_ind)
                return OSError
            if data:
                data = rsa.decrypt(data, self.private_key)
                self.server_log.save_message("Received message from {}".format(address))
                self.add_request(address, data.decode())
        self.close_connection(address, sock_ind)

    def send(self, address, message):
        ind = self.get_ind_by_address(address)
        try:
            if ind == 0:
                self.first_client.send(rsa.encrypt(message.encode(), self.keys[ind]))
            elif ind == 1:
                self.second_client.send(rsa.encrypt(message.encode(), self.keys[ind]))
            elif ind == 2:
                self.third_client.send(rsa.encrypt(message.encode(), self.keys[ind]))
        except OSError:
            self.server_log.save_message("Error sending message to {}".format(address))
            return OSError
        self.server_log.save_message("Send message to {} with socket {}".format(address, ind))

    def raw_send(self, address, message):
        ind = self.get_ind_by_address(address)
        try:
            if ind == 0:
                self.first_client.send(message)
            elif ind == 1:
                self.second_client.send(message)
            elif ind == 2:
                self.third_client.send(message)
        except OSError:
            return OSError

    def connect(self, address, port, sock_ind):  # Создаёт подключение c соккетом по индексу
        if sock_ind == 0:
            try:
                self.first_client.connect((address, port))
            except OSError:
                return OSError
        elif sock_ind == 1:
            try:
                self.second_client.connect((address, port))
            except OSError:
                return OSError
        elif sock_ind == 2:
            try:
                self.third_client.connect((address, port))
            except OSError:
                return OSError
        self.clients_info[sock_ind] = 1

    def reload_socket(self, sock_ind):  # Перезагружает соккет с указанным индексом
        if sock_ind == 0:
            self.first_client.close()
            self.first_client = socket.socket()
        elif sock_ind == 1:
            self.second_client.close()
            self.second_client = socket.socket()
        elif sock_ind == 2:
            self.third_client.close()
            self.third_client = socket.socket()
        self.clients_info[sock_ind] = 0
        self.server_log.save_message("Socket {} was successfully reload".format(sock_ind))

    def get_free_socket(self):  # Возвращает индекс свободного соккета, иначе ничего
        for ind in range(self.max_clients):
            if self.clients_info[ind] == 0:
                return ind
        return None

    def get_request(self, address):  # Возвращает сообщение по адресу, иначе ничего
        try:
            message = self.requests.pop(address)
        except KeyError:
            message = None
        self.server_log.save_message("Request from {} was taken".format(address))
        return message

    def check_request(self, address):  # Возвращает Правда, если сообщение есть
        message = self.requests.get(address)
        return bool(message)

    def get_ind_by_address(self, address):  # Возвращет номер соккета, к которому подключён адрес
        ind = self.client_map.get(address)
        return ind

    def get_user_name_by_address(self, address):   # Возвращает имя пользователя по его адресу
        name = self.clients_names.get(address)
        return name

    def check_address(self, address):  # Возвращает Правда, если к адрессу уже есть подключение
        for i in self.clients:
            if i == address:
                return True
        return False

    def close_connection(self, address, sock_ind):  # Закрывает соединение
        try:
            self.reload_socket(sock_ind)
            self.del_user(address, sock_ind)
            self.server_log.save_message("Connection with {} closed".format(address))
        except TypeError:
            quit()

    def kill(self):  # Останавливает сервер
        self.running = False
        sleep(1)
        Log.save_dict(self.clients_names, "clients_names.txt")
        self.server_log.save_message("Server successfully stopped")
        self.server_log.close()
        self.first_client.close()
        self.server_socket.close()


