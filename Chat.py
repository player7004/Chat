import socket
from server import Server
from log import Log
from threading import Thread
import os.path
from tkinter import *

server_port=6060
listen_port=6061
running=True
peers=Log.read_and_return_list("peers.txt")

def get_name():
    name=""
    window=Tk()
    window.geometry("300x300+400+400")
    window.title("Chat - enter name")
    text=Text(window,height=1)
    def getText():
        name=text.get(1.0,END)
        window.quit()
    label=Label(window,text="Write your name: ",font="Arial 10")
    button=Button(window,text="Continue",command=getText)
    label.pack(side=TOP,fill=BOTH)
    text.pack(fill=BOTH,side=TOP)
    button.pack(side=BOTTOM,fill=BOTH)
    window.mainloop()
    return name

def run(nick):
    server=Server(server_port,name)
    peers=Log.read_and_return_list("peers.txt")
    main_window=Tk()
    main_window.title("Chat - Main window")
    main_window.geometry("400x400+400+400")
    listen_frame=Frame(main_window,relief=RAISED,borderwidth=1)
    quit_button=Button(listen_frame,text="Close",command=main_window.quit)
    listen_on=Button(listen_frame,text="Start Listen")
    listen_off=Button(listen_frame,text="Stop Listen")
    enter_ip_frame=Frame(main_window,relief=RAISED,borderwidth=1)
    enter_ip_label=Label(enter_ip_frame,text="Write ip to Directional connect:",font="Arial 10")
    enter_ip_text=Text(enter_ip_frame,height=1,bg="white",fg="black",wrap=WORD)
    enter_ip_connect=Button(enter_ip_frame,text="Connect",command=NONE)
    listen_frame.pack(fill=X,side=BOTTOM)
    listen_on.pack(side=TOP,fill=BOTH,padx=5,pady=5)
    listen_off.pack(side=TOP,fill=BOTH,padx=5)
    quit_button.pack(side=BOTTOM,fill=BOTH,padx=5,pady=5)
    enter_ip_frame.pack(fill=X,side=TOP)
    enter_ip_label.pack(side=TOP, fill=BOTH,padx=5)
    enter_ip_text.pack(side=TOP,fill=BOTH,padx=5)
    enter_ip_connect.pack(side=BOTTOM,fill=BOTH,padx=5,pady=5)
    main_window.mainloop()

k=get_name()
print(k)