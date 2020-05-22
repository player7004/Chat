import socket
from log import Log
from threading import Thread

class Server(Log):
    def __init__(self,port,user_name):
        self.your_name=user_name
        self.client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0",port))
        self.server_socket.listen()

    def connect(self,host,port): #Костыль
        self.client_socket.connect((host,port))
        print("You connected: "+ host)

    def connect_to_server(self,host,port): 
        connect_thread=Thread(target=self.connect, args=(host,port))
        connect_thread.start()
        connect_thread.join()
        self.conn, self.addr=self.server_socket.accept()
        print(str(self.addr[0]) + " connected to you")
        
    def send(self,message):
        self.client_socket.send(str(message).encode())

    def get_message(self):
        data=self.conn.recv(1024)
        print(data.decode())

    def kill(self):
        self.client_socket.close()
        self.server_socket.close()


