import socket
import threading
import os
from dotenv import load_dotenv

class User:
    def __init__(self, client, nickname):
        self.client = client
        self.nickname = nickname


def broadcast(sender, message):
    for user in users:
        if user != sender:
            user.client.send(f"{sender.nickname}: {message}".encode("ascii"))


def handle(user):
    while True:
        try:
            message = user.client.recv(1024).decode("ascii")
            broadcast(user, message)
        except:
            index = users.index(user)
            users.remove(user)
            user.client.close()
            break


def receive():
    while True:
        client, address = server.accept()
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        user = User(client, nickname)
        users.append(user)
        broadcast(user, f"{nickname} joined the chat")
        client.send("Connected".encode('ascii'))
        thread = threading.Thread(target=handle, args=(user,))
        thread.start()


if __name__ == '__main__':
    # Init dotenv
    if os.getenv('PY_ENV') != "PRO":
        load_dotenv()

    # Connection data
    SERVER_IP = os.getenv('IP_ADDRESS')
    SERVER_PORT = int(os.getenv('PORT'))

    # Starting Server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()

    users = []
    print(f"Server on port: {SERVER_PORT}")
    receive()