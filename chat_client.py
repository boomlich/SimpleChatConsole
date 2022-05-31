from socket import socket, create_connection
from threading import Thread


def send_msg(server: socket, message: str):
    message += "#" * (128 - len(message))
    server.send(message.encode())

def _recv(server: socket):
    while True:
        data = server.recv(128)
        if data:
            cmd, msg = data.decode().split("|")
            msg = msg.replace("#", "")        
            if cmd == "PRT":
                print(msg)
            elif cmd == "INP":
                msg = give_input()
                server.send(msg.encode())

def give_input() -> str:
    message = input()
    message += "#" * (128 - len(message))
    return message


def connect_to_server():
    name = input("Username: ")
    server = create_connection(("localhost", 5550))
    send_msg(server, name)
    return server

def init():
    server = connect_to_server()
    _recv(server)


init()