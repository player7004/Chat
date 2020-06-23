import socket
from server import Server
from log import Log
from tkinter import *
import time
from threading import Thread

config = Log.read_and_return_dict("config.txt")

server_port = int(config["server_port"])
listen_port = int(config["listen_port"])
check_port = int(config["check_port"])
timeout = float(config["timeout"])
label_font = config["label_font"]
button_font = config["button_font"]


def load_error_window(text):
    def end():
        root.quit()
        root.destroy()

    root = Tk()
    root.resizable(False, False)
    root.title("Error!")

    quit_frame = Frame(root, relief=RAISED, borderwidth=1)

    error_label = Label(root, text="Error: " + text, font=label_font)
    quit_continue = Button(quit_frame, text="Continue", command=end)

    quit_frame.pack(fill=BOTH, side=BOTTOM)

    error_label.pack(fill=BOTH)
    quit_continue.pack(fill=BOTH, padx=5, pady=5)

    root.mainloop()


def load_chat_window(address, your_name):
    def end():
        window_manager.pop(address)
        nonlocal running
        print(server.get_ind_by_address(address))
        server.close_connection(address, server.get_ind_by_address(address))
        user_log.close()
        running = False
        time.sleep(2)
        window.quit()
        window.destroy()

    def get_message():
        while running:
            time.sleep(0.1)
            if server.check_request(address):
                message = server.get_request(address)
                messages.insert(END, "{}: {}".format(user, message))
                user_log.save_message("{}: {}".format(user, message))

    def send():
        text = send_text.get(1.0, END)
        text = text[:text.find("\n")]
        if text == "":
            return
        try:
            server.send(address, text)
        except OSError:
            end()
            load_error_window("User disconnected")
            return
        send_text.delete(1.0, END)
        messages.insert(END, your_name + ": " + text)
        user_log.save_message("{}: {}".format(your_name, text))

    user = str(server.get_user_name_by_address(address))
    running = True
    user_log = Log(user + ".txt")

    window_manager.update({address: True})

    window = Tk()
    window.geometry("400x270+400+400")
    window.title("Chat with " + user)
    window.resizable(False, False)

    send_frame = Frame(window, relief=RAISED, borderwidth=1)
    message_frame = Frame(window, relief=RAISED, borderwidth=1)

    messages_scrollbar = Scrollbar(message_frame)
    messages = Listbox(message_frame, yscrollcommand=messages_scrollbar.set)

    send_text = Text(send_frame, height=1)
    send_button = Button(send_frame, text="Send", command=send, font=button_font)
    quit_button = Button(send_frame, text="Close", command=end, font=button_font)

    message_frame.pack(fill=X)
    send_frame.pack(fill=X, side=BOTTOM)

    messages_scrollbar.pack(fill=Y, side=RIGHT)
    messages.pack(padx=5, pady=5, fill=BOTH)
    messages_scrollbar.config(command=messages.yview)

    send_text.pack(fill=X, padx=5, pady=5)
    send_button.pack(fill=BOTH, padx=5)
    quit_button.pack(fill=BOTH, padx=5, pady=5)
    recieve_thread = Thread(target=get_message)
    recieve_thread.start()
    recieve_thread.join(0)

    insert(user + ".txt", messages)

    window.mainloop()


def load_get_name_window():
    name = ""

    def get_text():
        nonlocal name
        out = text.get(1.0, 32.0)
        out = out[:out.find("\n")]
        if out == "":
            load_error_window("Too short")
            return
        elif len(out) > 32:
            load_error_window("Too long")
            return
        elif out.find("\n") != -1 or out.find("\\") != -1:
            load_error_window("Invalid characters")
            return
        name = out
        window.quit()
        window.destroy()

    window = Tk()
    window.geometry("300x150+400+400")
    window.title("Chat - enter name")
    window.resizable(False, False)

    text = Text(window, height=1)
    label = Label(window, text="Write your name: ", font=label_font)
    available_label = Label(window, text="Max length=32\nYou can`t use: \\n, \\", font=label_font)
    button = Button(window, text="Continue", command=get_text, font=button_font)

    label.pack(side=TOP, fill=BOTH)
    text.pack(fill=BOTH, side=TOP, padx=5)
    available_label.pack(fill=BOTH, pady=5)
    button.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)

    window.mainloop()
    return name


def load_main_window(nick):

    def listen_loop():
        while running:
            time.sleep(0.1)
            if listening:
                try:
                    data, address = listening_socket.recvfrom(32)
                except socket.timeout:
                    continue
                except OSError:
                    end()
                    load_error_window("Unknown error")
                    return
                server.add_user_name(address[0], data.decode())
                if not check_in_online(address[0]):
                    listen_frame_listbox_online.insert(END, address[0])
                    users_online.append(address[0])
                listen_connect(address[0])

    def check_loop():
        while running:
            time.sleep(0.1)
            try:
                data, address = listening_socket.recvfrom(5)
                print(data, address)
            except socket.timeout:
                continue
            except OSError:
                end()
                load_error_window("Unknown error")
                return
            if data == b"alive":
                check_socket.sendto(b"alive", (address[0], check_port))

    def check_ip(address):
        try:
            check_socket.sendto(b"alive", (address, check_port))
            data, address = check_socket.recvfrom(5)
        except socket.timeout:
            return False
        except OSError:
            return False
        if data == b"alive":
            listening_socket.sendto(nick.encode(), (address[0], listen_port))
            return True
        return False

    def listen_connect(address):
        if server.check_address(address):
            if not window_manager.get(address):
                load_chat_window(address, nick)
            else:
                load_error_window("Chat already open")
            return
        if check_ip(address):
            thread = Thread(target=server.create_connection, args=(address, server_port))
            thread.start()
            thread.join(0)
            load_chat_window(address, nick)
        else:
            load_error_window("Can`t connect to: " + address)
            return

    def connect():
        address = enter_ip_text.get(1.0, END)
        address = address[:address.find("\n")]
        enter_ip_text.delete(1.0, END)
        if server.check_address(address):
            if not window_manager.get(address):
                load_chat_window(address, nick)
            else:
                load_error_window("Chat already open")
            return
        if check_ip(address):
            Log.save_with_ignore_same("peers.txt", address)
            thread = Thread(target=server.create_connection, args=(address, server_port))
            thread.start()
            thread.join(0)
            load_chat_window(address, nick)
        else:
            load_error_window("Can`t connect to: " + address)
            return

    def end():
        nonlocal listening, running
        listening = False
        running = False
        time.sleep(1)
        main_window.quit()
        main_window.destroy()
        server.kill()
        listening_socket.close()

    def change_status():
        nonlocal listening
        listening = not listening
        if listening:
            settings_label_status['bg'] = "green"
            settings_label_status['text'] = "You are online"
        else:
            settings_label_status['bg'] = "red"
            settings_label_status['text'] = "You are offline"

    def change_nick():
        nonlocal nick
        name = load_get_name_window()
        name_frame_label['text'] = "Your nick: " + name
        nick = name

    running = True
    listening = False

    listen_thread = Thread(target=listen_loop)
    listen_thread.start()
    listen_thread.join(0)

    check_thread = Thread(target=check_loop)
    check_thread.start()
    check_thread.join(0)

    server.add_user_name("localhost", nick)
    server.add_user_name("127.0.0.1", nick)

    # Основное окно
    main_window = Tk()
    main_window.title("Chat - Main window")
    main_window.geometry("454x424+400+400")
    main_window.resizable(False, False)
    # Фреймы и кнопки
    enter_ip_frame = Frame(main_window, relief=RAISED, borderwidth=1)
    name_frame = Frame(main_window, relief=RAISED, borderwidth=1)
    listen_frame = Frame(main_window, relief=RAISED, borderwidth=1)
    settings_frame = Frame(main_window, relief=RAISED, borderwidth=1)

    enter_ip_label = Label(enter_ip_frame, text="Write ip to connect/open chat window:", font=label_font)
    enter_ip_text = Text(enter_ip_frame, height=1, bg="white", fg="black", wrap=WORD)
    enter_ip_connect = Button(enter_ip_frame, text="Connect", command=connect, font=button_font)

    name_frame_label = Label(name_frame, text="Your nick: " + nick, font=label_font)
    name_frame_ip_label = Label(name_frame, text="Your ip: " + socket.gethostbyname(socket.getfqdn()), font=label_font)
    name_frame_change_button = Button(name_frame, text="Change nick", command=change_nick)

    listen_frame_scrollbar_online = Scrollbar(listen_frame)
    listen_frame_scrollbar_peers = Scrollbar(listen_frame)
    listen_frame_label_online = Label(listen_frame, text="Users online: ", font=label_font)
    listen_frame_label_peers = Label(listen_frame, text="Last users: ", font=label_font)
    listen_frame_listbox_online = Listbox(listen_frame, yscrollcommand=listen_frame_scrollbar_online.set)
    listen_frame_listbox_peers = Listbox(listen_frame, yscrollcomman=listen_frame_scrollbar_peers.set)
    insert("peers.txt", listen_frame_listbox_peers)

    settings_label_status = Label(settings_frame, text="You are offline", font=label_font, bg="red")
    settings_change_listening_status = Button(settings_frame, text="Change listen status", command=change_status,
                                              font=button_font)
    settings_quit_button = Button(settings_frame, text="Close", command=end, font=button_font)

    # Расстановка
    enter_ip_frame.pack(fill=X)
    name_frame.pack(fill=X)
    listen_frame.pack(fill=X)
    settings_frame.pack(fill=X)

    enter_ip_label.pack(side=TOP, fill=BOTH, padx=5)
    enter_ip_text.pack(side=TOP, fill=BOTH, padx=5)
    enter_ip_connect.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)

    listen_frame_label_online.pack(pady=5, side=LEFT)
    listen_frame_listbox_online.pack(side=LEFT, fill=BOTH)
    listen_frame_scrollbar_online.config(command=listen_frame_listbox_online.yview)
    listen_frame_scrollbar_online.pack(side=LEFT, fill=Y)
    listen_frame_label_peers.pack(side=LEFT,  pady=5)
    listen_frame_listbox_peers.pack(side=LEFT)
    listen_frame_scrollbar_peers.config(command=listen_frame_listbox_peers.yview)
    listen_frame_scrollbar_peers.pack(side=LEFT, fill=Y)

    name_frame_label.pack(fill=X, padx=5)
    name_frame_ip_label.pack()
    name_frame_change_button.pack(fill=BOTH, pady=5, padx=5)

    settings_label_status.pack()
    settings_change_listening_status.pack(fill=BOTH, padx=5, pady=5)
    settings_quit_button.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)
    # Запуск
    main_window.mainloop()


listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Слушающий соккет
listening_socket.bind(('localhost', listen_port))
listening_socket.settimeout(timeout)

check_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Соккет проверки
check_socket.bind(('localhost', check_port))
check_socket.settimeout(timeout)

server = Server(server_port, timeout)

window_manager = {}  # Менеджер открытых окон аддресс: правда - открыто/ ложь - закрыто
users_online = []  # Лист с пользователей онлайн


def check_in_online(address):
    for i in users_online:
        if address == i:
            return True
    return False


def insert(file_name, listbox):
    for line in Log.read_and_return_list(file_name):
        listbox.insert(END, line)


def run():
    your_name = load_get_name_window()
    if your_name == "":
        return
    server.set_server_name(your_name)
    load_main_window(your_name)


if __name__ == "__main__":
    run()
