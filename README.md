# Chat
Chat for use in locale network.
>You may try to use it with VPN

# Installation
+ main.pyw 
    >Run chat
+ chat.py
    >Interface and main cycle                                                                                      
+ log.py
    >Class Log
+ server.py
    >Class Server with server functions
+ config.txt
    >Config file for server Interface
+ requirements.txt
    >Libraries that you need to run chat

# Requirements
To run chat you need to install python version 3.5 or later and  rsa version 4.6 or later.
>
    >>pip install rsa
[Click here to visit Python page](https://www.python.org/)

[Click here to visit RSA page](https://pypi.org/project/rsa/4.6/)

# Quick Start
To start you may run main.pyw

Also program can be started from terminal
>
    >>python main.pyw
    
# Server module
If you want to use my server module in your project.

You must have file log.py too. 

Server module bases on sockets. Max 3 clients at one time
>
    >>>from server import Server
Server need port(int) and timeout(float) to be initialized
>
    >>>server = Server(port, timeout)
You can set name to server by set_name(name) fucntion
>
    >>>server.set_name(name)
To create connection with user use create_connection(address, port)

Better to create connection in separate Thread
>
    >>>server.create_connection(address, port)
At first it`s creating connection with user and sending RSA public key to user, getting RSA public key from user.

Then it will listen for incoming message and adding it in request map.

To get message from user you at first check_request(address)
and the if there is message from address use get_request(address)
>
    >>>if server.check_request(address):
        message = server.get_request(address)
Server module has 2 ways to send message: raw_send(address, message) and send(address, message). 

The only difference is that raw_send sending message without any cipher, but send with RSA cipher
>
    >>>server.send(address, message) # With cipher
    >>>server.raw_send(address, message) # Withoout cipher

To close connection use close_connection(address, sock_ind). sock_ind is socket index.
You can get it by address and function get_ind_by_address(address).
>
    >>>server.close_connection(address, server.get_ind_by_address(address))
At least you can work with user names by functions add_user_name(address, name) 
and get_user_name_by_address(address). Server will save user names in 
client_names.txt and read they from this file on next launch
>
    >>>server.add_user_name(address, name)
    >>>user_name = server.get_user_name_by_address(address)
To close server run function kill()
>
    >>>server.kill()