import socket
from server import Server
from log import Log
from threading import Thread
from tkinter import *

server_port = 6060
listen_port = 6061
font_size = "Arial 10"
listening = False


def load_error_window(text):
    def end():
        root.quit()
        root.destroy()

    root = Tk()
    root.geometry("200x100+400+400")
    root.resizable(False, False)
    root.title("Error!")

    error_label = Label(root, text="Error: " + text, font=font_size)
    error_continue = Button(root, text="Continue", command=end)

    error_label.pack(fill=BOTH)
    error_continue.pack(fill=BOTH, side=BOTTOM, padx=5, pady=5)

    root.mainloop()


def load_get_name_window():
    def get_text():
        out = text.get(1.0, 32.0)
        label1['text'] = out
        window.quit()

    window = Tk()
    window.geometry("300x150+400+400")
    window.title("Chat - enter name")
    window.resizable(False, False)

    text = Text(window, height=1)
    label = Label(window, text="Write your name: ", font=font_size)
    available_label = Label(window, text="Max length=32\nYou can`t use: \\n ", font=font_size)
    label1 = Label()
    button = Button(window, text="Continue", command=get_text)

    label.pack(side=TOP, fill=BOTH)
    text.pack(fill=BOTH, side=TOP, padx=5)
    available_label.pack(fill=BOTH, pady=5)
    button.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)
    window.mainloop()
    name = label1['text']
    window.destroy()
    return name


def load_main_window(nick):
    def end():
        main_window.quit()
        main_window.destroy()

    def change_status():
        global listening
        listening = not listening
        if listening:
            settings_label_status['bg'] = "green"
            settings_label_status['text'] = "You are listening for users"
        else:
            settings_label_status['bg'] = "red"
            settings_label_status['text'] = "You are not listening for users"

    def change_nick():
        main_window.quit()
        main_window.destroy()
        run()

    def insert_peers():
        for line in Log.read_and_return_list("peers.txt"):
            listen_frame_listbox_peers.insert(END, line)

    # Основное окно
    main_window = Tk()
    main_window.title("Chat - Main window")
    main_window.geometry("500x652+400+400")
    main_window.resizable(False,False)
    # Фреймы и кнопки
    settings_frame = Frame(main_window, relief=RAISED, borderwidth=1)
    name_frame = Frame(main_window, relief=RAISED, borderwidth=1)
    listen_frame = Frame(main_window, relief=RAISED, borderwidth=1)
    enter_ip_frame = Frame(main_window, relief=RAISED, borderwidth=1)

    enter_ip_label = Label(enter_ip_frame, text="Write ip to connect:", font=font_size)
    enter_ip_text = Text(enter_ip_frame, height=1, bg="white", fg="black", wrap=WORD)
    enter_ip_connect = Button(enter_ip_frame, text="Connect", command=NONE)

    name_frame_label = Label(name_frame, text="Your nick: " + nick[:nick.find("\n")], font=font_size)
    name_frame_ip_label = Label(name_frame, text=socket.gethostbyname(socket.getfqdn()), font=font_size)
    name_frame_change_button = Button(name_frame, text="Change nick", command=change_nick)

    listen_frame_scrollbar_online = Scrollbar(listen_frame)
    listen_frame_scrollbar_peers = Scrollbar(listen_frame)
    listen_frame_label_online = Label(listen_frame, text="Users online: ", font=font_size)
    listen_frame_label_peers = Label(listen_frame, text="Last users: ", font=font_size)
    listen_frame_listbox_online = Listbox(listen_frame, yscrollcommand=listen_frame_scrollbar_online.set)
    listen_frame_listbox_peers = Listbox(listen_frame, yscrollcomman= listen_frame_scrollbar_peers.set)
    insert_peers()

    settings_label_status = Label(settings_frame, text="You are not listening for users", font=font_size, bg="red")
    settings_change_listening_status = Button(settings_frame, text="Change listen status", command=change_status)
    settings_quit_button = Button(settings_frame, text="Close", command=end)

    # Расстановка
    enter_ip_frame.pack(fill=X)
    name_frame.pack(fill=X)
    listen_frame.pack(fill=X)
    settings_frame.pack(fill=X)

    enter_ip_label.pack(side=TOP, fill=BOTH, padx=5)
    enter_ip_text.pack(side=TOP, fill=BOTH, padx=5)
    enter_ip_connect.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)

    listen_frame_label_online.pack(fill=BOTH, pady=5)
    listen_frame_listbox_online.pack(fill=BOTH)
    listen_frame_label_peers.pack(fill=BOTH, pady=5)
    listen_frame_listbox_peers.pack(fill=BOTH)
    listen_frame_scrollbar_online.config(command=listen_frame_listbox_online.yview)
    listen_frame_scrollbar_peers.config(command=listen_frame_listbox_peers.yview)

    name_frame_label.pack(fill=X, padx=5)
    name_frame_ip_label.pack()
    name_frame_change_button.pack(fill=BOTH, pady=5, padx=5)

    settings_label_status.pack()
    settings_change_listening_status.pack(fill=BOTH, padx=5, pady=5)
    settings_quit_button.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)
    # Запуск
    main_window.mainloop()


def run():
    your_name = ""
    while your_name == "":
        sit_name = load_get_name_window()
        if sit_name == "\n":
            load_error_window("Too short")
            continue
        elif len(sit_name) > 32:
            load_error_window("Too long")
            continue
        your_name = sit_name
    load_main_window(your_name)


run()