from socket import socket, create_server
from threading import Thread

class Client:

    def __init__(self, sock: socket, name: str):
        self.sock = sock
        self.name = name

    def print_msg(self, message: str) -> None:
        send_msg(self.sock, "PRT", message)

    def give_input(self) -> None:
        send_msg(self.sock, "INP", "")



def send_msg(client: socket, command: str, message: str) -> None:
    message = f"{command}|{message}"
    message += "#" * (128 - len(message))
    client.send(message.encode())


def _recv(client: Client, other_client: Client) -> None:
    global clients
    print(f"[SERVER] started listening for messages from {client.name}")
    while True:
        data = client.sock.recv(128)
        if data:
            msg = data.decode().replace("#", "")
            print(msg)  
            other_client.print_msg(f"{client.name} : {msg}")


def init(sock: socket, clients: list) -> None:
    sock.listen()
    print("[SERVER] listnening for connections...")

    clientA = establish_client(sock)
    clientA.print_msg(f"[SERVER] Welcome {clientA.name}, please wait for another client...")
    clients.append(clientA)

    clientB = establish_client(sock)
    clients.append(clientB)
    start_chat(clients)

def start_chat(clients: list[Client]) -> None:
    for client in clients:
        other_client = clients[1] if client == clients[0] else clients[0]

        Thread(target = _recv, args=[client, other_client]).start()

        client.print_msg(f"{other_client.name} connected. You can now start chatting.")
        client.give_input()

def establish_client(sock: socket) -> Client:
    client_socket = accept_socket(sock)
    client_name = client_socket.recv(128).decode().replace("#", "")
    client = Client(client_socket, client_name)
    return client


def accept_socket(sock: socket) -> socket:
    client_socket, _ = sock.accept()
    print("Client connected:", client_socket)
    return client_socket

clients = []

if __name__ == "__main__":
    sock = create_server(("localhost", 5550))
    init(sock, clients)