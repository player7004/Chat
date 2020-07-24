import socket, time
import curses, curses.textpad
from cursesmenu import CursesMenu
from cursesmenu.items import *
from threading import Thread
from src.server import Server
from src.log import Log


# def load_error_window(text):  # Загружает окно загрузки с указанным текстом
#     def end():
#         root.quit()
#         root.destroy()
#
#     root = Tk()
#     root.resizable(False, False)
#     root.title("Error!")
#
#     quit_frame = Frame(root, relief=RAISED, borderwidth=1)
#
#     error_label = Label(root, text="Error: " + text, font=label_font)
#     quit_continue = Button(quit_frame, text="Continue", command=end)
#
#     quit_frame.pack(fill=BOTH, side=BOTTOM)
#
#     error_label.pack(fill=BOTH)
#     quit_continue.pack(fill=BOTH, padx=5, pady=5)
#
#     root.mainloop()
#
#
# def load_chat_window(address, your_name):  # Загружает окно чата. Нужен адрес пользователя и имя локального клиента
#     def end():
#         window_manager.pop(address)
#         nonlocal running
#         server.close_connection(address, server.get_ind_by_address(address))
#         user_log.close()
#         running = False
#         time.sleep(2)
#         window.quit()
#         window.destroy()
#
#     def get_message():
#         while running:
#             time.sleep(0.1)
#             if server.check_request(address):
#                 message = server.get_request(address)
#                 messages.insert(END, "{}: {}".format(user, message))
#                 user_log.save_message("{}: {}".format(user, message))
#
#     def send():
#         text = send_text.get(1.0, END)
#         text = text[:text.find("\n")]
#         if text == "":
#             return
#         try:
#             server.send(address, text)
#         except OSError:
#             end()
#             load_error_window("User disconnected")
#             return
#         send_text.delete(1.0, END)
#         messages.insert(END, your_name + ": " + text)
#         user_log.save_message("{}: {}".format(your_name, text))
#
#     user = str(server.get_user_name_by_address(address))
#     running = True
#     user_log = Log(user + ".txt")
#
#     window_manager.update({address: True})
#
#     window = Tk()
#     window.geometry("400x270+400+400")
#     window.title("Chat with " + user)
#     window.resizable(False, False)
#
#     send_frame = Frame(window, relief=RAISED, borderwidth=1)
#     message_frame = Frame(window, relief=RAISED, borderwidth=1)
#
#     messages_scrollbar = Scrollbar(message_frame)
#     messages = Listbox(message_frame, yscrollcommand=messages_scrollbar.set)
#
#     send_text = Text(send_frame, height=1)
#     send_button = Button(send_frame, text="Send", command=send, font=button_font)
#     quit_button = Button(send_frame, text="Close", command=end, font=button_font)
#
#     message_frame.pack(fill=X)
#     send_frame.pack(fill=X, side=BOTTOM)
#
#     messages_scrollbar.pack(fill=Y, side=RIGHT)
#     messages.pack(padx=5, pady=5, fill=BOTH)
#     messages_scrollbar.config(command=messages.yview)
#
#     send_text.pack(fill=X, padx=5, pady=5)
#     send_button.pack(fill=BOTH, padx=5)
#     quit_button.pack(fill=BOTH, padx=5, pady=5)
#     recieve_thread = Thread(target=get_message)
#     recieve_thread.start()
#     recieve_thread.join(0)
#
#     insert(user + ".txt", messages)
#
#     window.mainloop()
#
#
# def load_get_name_window():  # Загружает окно получения имени, возвращает полученное имя
#     name = ""
#
#     def get_text():
#         nonlocal name
#         out = text.get(1.0, 32.0)
#         out = out[:out.find("\n")]
#         if out == "":
#             load_error_window("Too short")
#             return
#         elif len(out) > 32:
#             load_error_window("Too long")
#             return
#         elif out.find("\n") != -1 or out.find("\\") != -1:
#             load_error_window("Invalid characters")
#             return
#         name = out
#         window.quit()
#         window.destroy()
#
#     window = Tk()
#     window.geometry("300x150+400+400")
#     window.title("Chat - enter name")
#     window.resizable(False, False)
#
#     text = Text(window, height=1)
#     label = Label(window, text="Write your name: ", font=label_font)
#     available_label = Label(window, text="Max length=32\nYou can`t use: \\n, \\", font=label_font)
#     button = Button(window, text="Continue", command=get_text, font=button_font)
#
#     label.pack(side=TOP, fill=BOTH)
#     text.pack(fill=BOTH, side=TOP, padx=5)
#     available_label.pack(fill=BOTH, pady=5)
#     button.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)
#
#     window.mainloop()
#     return name
#
#
# def load_main_window(nick):  # Загружает основное окно. Нужно имя локального пользователя
#     def connect():   # Исходящее подключение
#         address = enter_ip_text.get(1.0, END)
#         address = address[:address.find("\n")]
#         enter_ip_text.delete(1.0, END)
#         if server.check_address(address):
#             if not window_manager.get(address):
#                 load_chat_window(address, nick)
#             else:
#                 load_error_window("Chat already open")
#             return
#         if check_ip(address):
#             Log.save_with_ignore_same("peers.txt", address)
#             thread = Thread(target=server.create_connection, args=(address, server_port))
#             thread.start()
#             thread.join(0)
#             load_chat_window(address, nick)
#         else:
#             load_error_window("Can`t connect to: " + address)
#             return
#
#     def end():  # Останавливет работу
#         nonlocal listening, running
#         listening = False
#         running = False
#         time.sleep(1)
#         main_window.quit()
#         main_window.destroy()
#         server.kill()
#         listening_socket.close()
#
#     def change_status():  # Включает/Выключает прослушивание
#         nonlocal listening
#         listening = not listening
#         if listening:
#             settings_label_status['bg'] = "green"
#             settings_label_status['text'] = "You are online"
#         else:
#             settings_label_status['bg'] = "red"
#             settings_label_status['text'] = "You are offline"
#
#     def change_nick():  # Меняет имя пользователя
#         nonlocal nick
#         name = load_get_name_window()
#         name_frame_label['text'] = "Your nick: " + name
#         nick = name
#
#     running = True
#     listening = False
#
#     listen_thread = Thread(target=listen_loop)
#     listen_thread.start()
#     listen_thread.join(0)
#
#     check_thread = Thread(target=check_loop)
#     check_thread.start()
#     check_thread.join(0)
#
#     server.add_user_name("localhost", nick)
#     server.add_user_name("127.0.0.1", nick)
#
#     # Основное окно
#     main_window = Tk()
#     main_window.title("Chat - Main window")
#     main_window.geometry("454x424+400+400")
#     main_window.resizable(False, False)
#     # Фреймы и кнопки
#     enter_ip_frame = Frame(main_window, relief=RAISED, borderwidth=1)
#     name_frame = Frame(main_window, relief=RAISED, borderwidth=1)
#     listen_frame = Frame(main_window, relief=RAISED, borderwidth=1)
#     settings_frame = Frame(main_window, relief=RAISED, borderwidth=1)
#
#     enter_ip_label = Label(enter_ip_frame, text="Write ip to connect/open chat window:", font=label_font)
#     enter_ip_text = Text(enter_ip_frame, height=1, bg="white", fg="black", wrap=WORD)
#     enter_ip_connect = Button(enter_ip_frame, text="Connect", command=connect, font=button_font)
#
#     name_frame_label = Label(name_frame, text="Your nick: " + nick, font=label_font)
#     name_frame_ip_label = Label(name_frame, text="Your ip: " + socket.gethostbyname(socket.getfqdn()), font=label_font)
#     name_frame_change_button = Button(name_frame, text="Change nick", command=change_nick)
#
#     listen_frame_scrollbar_online = Scrollbar(listen_frame)
#     listen_frame_scrollbar_peers = Scrollbar(listen_frame)
#     listen_frame_label_online = Label(listen_frame, text="Users online: ", font=label_font)
#     listen_frame_label_peers = Label(listen_frame, text="Last users: ", font=label_font)
#     listen_frame_listbox_online = Listbox(listen_frame, yscrollcommand=listen_frame_scrollbar_online.set)
#     listen_frame_listbox_peers = Listbox(listen_frame, yscrollcomman=listen_frame_scrollbar_peers.set)
#     insert("peers.txt", listen_frame_listbox_peers)
#
#     settings_label_status = Label(settings_frame, text="You are offline", font=label_font, bg="red")
#     settings_change_listening_status = Button(settings_frame, text="Change listen status", command=change_status,
#                                               font=button_font)
#     settings_quit_button = Button(settings_frame, text="Close", command=end, font=button_font)
#
#     # Расстановка
#     enter_ip_frame.pack(fill=X)
#     name_frame.pack(fill=X)
#     listen_frame.pack(fill=X)
#     settings_frame.pack(fill=X)
#
#     enter_ip_label.pack(side=TOP, fill=BOTH, padx=5)
#     enter_ip_text.pack(side=TOP, fill=BOTH, padx=5)
#     enter_ip_connect.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)
#
#     listen_frame_label_online.pack(pady=5, side=LEFT)
#     listen_frame_listbox_online.pack(side=LEFT, fill=BOTH)
#     listen_frame_scrollbar_online.config(command=listen_frame_listbox_online.yview)
#     listen_frame_scrollbar_online.pack(side=LEFT, fill=Y)
#     listen_frame_label_peers.pack(side=LEFT,  pady=5)
#     listen_frame_listbox_peers.pack(side=LEFT)
#     listen_frame_scrollbar_peers.config(command=listen_frame_listbox_peers.yview)
#     listen_frame_scrollbar_peers.pack(side=LEFT, fill=Y)
#
#     name_frame_label.pack(fill=X, padx=5)
#     name_frame_ip_label.pack()
#     name_frame_change_button.pack(fill=BOTH, pady=5, padx=5)
#
#     settings_label_status.pack()
#     settings_change_listening_status.pack(fill=BOTH, padx=5, pady=5)
#     settings_quit_button.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)
#     # Запуск
#     main_window.mainloop()


# Обовляет основное окно
def refresh_main_window():
    main_window.clear()
    main_window.refresh()
    main_window.border(0)


# Выключает всё
def end_main_window():
    global running
    running = False
    for i in users_online:
        server.close_connection(i, server.get_ind_by_address(i))
    server.kill()
    main_window.clear()
    main_window.refresh()
    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)
    curses.endwin()
    quit(0)


def incoming_connect(_address):
    if not server.check_address(_address):
        return
    if check_ip(_address):
        thread = Thread(target=server.create_connection, args=(_address, server_port))
        thread.start()
        thread.join(0)
        users_online.append(_address)
    else:
        print_error_window("Can`t connect to: " + _address)
        return


def disconnect_via_ip(_ip: str):
    if check_in_online(_ip):
        server.close_connection(_ip, server.get_ind_by_address(_ip))
        users_online.remove(_ip)
    else:
        print_error_window("Wrong ip or you aren`t connected to this user")


def listen_loop():
    while running:
        time.sleep(0.1)
        if listening:
            try:
                data, address = listening_socket.recvfrom(32)
            except socket.timeout:
                continue
            except OSError:
                print_error_window("Unknown error")
                end_main_window()
                return
            server.add_user_name(address[0], data.decode())
            if not check_in_online(address[0]):
                users_online.append(address[0])
            incoming_connect(address[0])


def check_loop():
    while running:
        time.sleep(0.1)
        try:
            data, address = listening_socket.recvfrom(5)
        except socket.timeout:
            continue
        except OSError:
            print_error_window("Unknown error")
            end_main_window()
            return
        if data == b"alive":
            check_socket.sendto(b"alive", (address[0], check_port))
    else:
        return


# Проверка ip на валидность
def check_ip(_address):
    try:
        check_socket.sendto(b"alive", (_address, check_port))
        data, addr = check_socket.recvfrom(5)
    except socket.timeout:
        return False
    except OSError:
        return False
    if data == b"alive":
        listening_socket.sendto(name.encode(), (_address, check_port))
        return True


def print_connect_menu():
    def end():
        refresh_main_window()
        return

    refresh_main_window()
    curses.echo()

    data_const = "Enter user ip: "

    win_size = (6 if size[0] // 2 > 6 else size[0] // 2, 30 if size[1] // 2 > 30 else size[1] // 2)
    add_window = main_window.subwin(win_size[0], win_size[1], 1, 1)
    add_size = add_window.getmaxyx()

    add_window.border(0)
    add_window.addstr(add_size[0] // 2 - 1, add_size[1] // 2 - len(data_const) // 2, data_const)

    address = add_window.getstr(add_size[0] // 2, add_size[1] // 2)

    if server.check_address(address):
        end()
    end()


def connect_via_ip(_ip: str):
    if server.check_address(_ip):
        print_error_window("You already connected to this user")
    if check_ip(_ip):
        Log.save_with_ignore_same("peers.txt", _ip)
        thread = Thread(target=server.create_connection, args=(_ip, server_port))
        thread.start()
        thread.join(0)
        users_online.append(_ip)
    else:
        print_error_window("User if offline or ip is not valuable")


def print_get_command_window():
    # Возвращает арг или ничего
    def get_arg(_list):
        try:
            return _list[1]
        except IndexError:
            return None

    refresh_main_window()

    # Команды и описание
    commands_list = ["connect", "disconnect", "open", "listen", "quit", "help"]
    commands_list_description = [" *user_ip*", " *user_ip*", " *user_ip*", " *on/off", "", ""]

    # Вывод на экран комманд
    main_window.addstr(2, 2, "Available commands: ")
    for i in enumerate(commands_list):
        main_window.addstr(3 + i[0], 4, i[1] + commands_list_description[i[0]])
    main_window.addstr(size[0] - 2, 2, "Input: ")

    # Получаем команды
    command = str(main_window.getstr(size[0] - 2, 2 + len("Input: ")))
    command = command[2:len(command)-1].split("|")
    command = [i.split() for i in command]
    # Разбираем и выполняем команды
    is_quit = False
    for i in command:
        try:
            comm = i[0]
            if comm == 'connect':
                arg = get_arg(i)
                if arg is None:
                    pass
                connect_via_ip(arg)
            elif comm == 'disconnect':
                arg = get_arg(i)
                if arg is None:
                    pass
                disconnect_via_ip(arg)
            elif comm == 'open':
                arg = get_arg(i)
                if arg is None:
                    pass
            elif comm == 'listen':
                arg = get_arg(i)
                if arg is None:
                    pass
            elif comm == 'quit':
                is_quit = True
            elif command == 'help':
                pass
                # print help window
            else:
                pass
        except:
            pass
    # Если дана команда на выход - выходим
    if is_quit:
        end_main_window()
    else:
        print_get_command_window()


def print_get_name_window():
    refresh_main_window()

    # Размеры создаваемого окна
    info_const1 = "Available length between 4 and 32"
    info_const2 = "Wrong characters: \\n, \\"

    # Само окно
    win_size = (8 if size[0] // 2 > 8 else size[0] // 2, 50 if size[1] // 2 > 50 else size[1] // 2)
    add_window = main_window.subwin(win_size[0], win_size[1], 1, 1)
    add_size = add_window.getmaxyx()
    add_window.border(0)

    add_window.addstr(add_size[0] // 2 - 2, add_size[1] // 2 - len("Enter your name: ") // 2, "Enter your name: ")
    add_window.addstr(add_size[0] // 2 - 1, add_size[1] // 2 - len(info_const1) // 2, info_const1)
    add_window.addstr(add_size[0] // 2, add_size[1] // 2 - len(info_const2) // 2, info_const2)

    # Получаем имя
    name = str(add_window.getstr(add_size[0] // 2 + 1,
                                 add_size[1] // 2 - len("Enter your name: ") // 4, 32)).replace('b', '').replace('\'',
                                                                                                                 '')
    add_window.standend()
    refresh_main_window()
    return name


def print_error_window(_text: str):
    error_const = " Oh, shit i`m sorry, there is some error:"
    refresh_main_window()

    win_size = (size[0] - 2, size[1] - 2)
    add_window = main_window.subwin(win_size[0], win_size[1], 1, 1)
    add_window.border(0)

    add_size = add_window.getmaxyx()
    add_window.addstr(add_size[0] // 2, add_size[1] // 2 - len(error_const) // 2, error_const)
    add_window.addstr(add_size[0] // 2 + 1, add_size[1] // 2 - len(_text) // 2, _text)

    curses.noecho()
    add_window.timeout(3000)
    add_window.getch()
    curses.echo(True)

    refresh_main_window()
    return


def check_in_online(_address):  # Проверяет пользователя в списке онлайн
    for i in users_online:
        if _address == i:
            return True
    return False


# Инициализация окна
main_window = curses.initscr()
curses.cbreak(True)
main_window.border(0)
main_window.keypad(True)
size = main_window.getmaxyx()

# Глбальные переменные необходимые для работы
running = True
listening = False

# Конфиги для сервера
config = Log.read_and_return_dict("config.TXT")
server_port = int(config["server_port"])
listen_port = int(config["listen_port"])
check_port = int(config["check_port"])
timeout = float(config["timeout"])

# Слушающий соккет
listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listening_socket.bind(('localhost', listen_port))
listening_socket.settimeout(timeout)

# Слушающий поток
listen_thread = Thread(target=listen_loop)
listen_thread.start()
listen_thread.join(0)

# Проверяющий соккет
check_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
check_socket.bind(('localhost', check_port))
check_socket.settimeout(timeout)

# Проверяющий поток
check_thread = Thread(target=check_loop)
check_thread.start()
check_thread.join(0)

# Сервер
server = Server(server_port, timeout)

# Лист с пользователей онлайн
users_online = []
connected_users = []
last_commands = []
name = ""


def run():
    print_get_command_window()

# def run():  # Запускает сервер
#     your_name = load_get_name_window()
#     if your_name == "":
#         return
#     server.set_server_name(your_name)
#     load_main_window(your_name)
