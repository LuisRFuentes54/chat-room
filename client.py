import socket
import threading

def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == 'NICK':
                nickname = input("Choose a nickname: ")
                client.send(nickname.encode("ascii"))
                print(client.recv(1024).decode("ascii"))
            elif message != "":
                print(message)
            else:
                print("Server Error")
                client.close()
                break
        except:
            print("Network Error")
            client.close()
            break


def write():
    while True:
        message = input('')
        client.send(message.encode("ascii"))

if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((input("IP Server: "), 5400))
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    write_thread = threading.Thread(target=write)
    write_thread.start()