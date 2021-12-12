import socket
import datetime
import random

SERVER_IP = "0.0.0.0"
PORT = 8820
MAX_MSG_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, PORT))
server_socket.listen()
print("Server is up and running")
(client_socket, client_address) = server_socket.accept()
print("Client connected")

server_data = ""
while True:
    client_data = client_socket.recv(MAX_MSG_SIZE).decode()
    print("Client sent: " + client_data)
    if client_data == "Quit":
        print("closing client socket now...")
        client_socket.send("Bye".encode())
        break
    if client_data == "NAME":
        server_data = "my name is server"
    if client_data == "TIME":
        current_time = datetime.datetime.now()
        server_data = str(current_time)
    if client_data == "RAND":
        random_number = random.randint(1, 10)
        server_data = str(random_number)

    client_socket.send(server_data.encode())


client_socket.close()
server_socket.close()
