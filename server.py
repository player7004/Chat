import socket
from log import Log
from threading import Thread


class Server(Log):
    def __init__(self,port):
        self.clients = []  # Список подключённых ip
        self.requests = {}  # Карта входящий сообщений
        self.clients_names = {}  # Карта ников пользователей
        self.name = ""  # Имя сервера

        self.running = True
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('localhost',port))
        self.server_socket.listen()
        self.server_socket.settimeout(1)
        self.client_socket.settimeout(1)

    def send(self, message):  # Отправляем сообщение на сервер
        try:
            self.client_socket.send(message.encode())
        except OSError:
            return OSError

    def connect(self, address, port):  # Подключаемся к серверу
        self.client_socket.connect((address, port))

    def create_connection(self, c_address, port):  # Создаёт подключение
        self.add_user(c_address, c_address)
        create_thread = Thread(target=self.connect, args=(c_address, port))
        create_thread.start()
        create_thread.join(0)
        connection, address = self.server_socket.accept()
        while connection and self.running:
            try:
                data = connection.recv(1024)
            except socket.timeout:
                continue
            self.requests.update({c_address: data.decode()})

    # check-функции
    def check_connections(self):
        for peer in self.clients:
            try:
                self.server_socket.accpet()
            except OSError:
                self.clients.remove(peer)

    def check_connection(self, address):
        for line in self.clients:
            if line == address:
                return True
        return False

    def check_request(self, address):
        try:
            data = self.requests.pop(address)
        except KeyError:
            return None
        return data

    # set-функции
    def set_name(self, name):
        self.name = name

    # add-функции
    def add_user(self, user_address, user_nick):
        self.clients.append(user_address)
        self.clients_names.update({user_address: user_nick})

    # del-функции
    def del_user(self, user_address):
        self.clients.remove(user_address)
        self.clients_names.pop(user_address)

    # get-функции
    def get_users_data(self):
        return self.clients_names.items()

    def get_user_name(self, address):
        return self.clients_names.get(address)

    def kill(self):
        self.running = False
        self.client_socket.close()
        self.server_socket.close()


