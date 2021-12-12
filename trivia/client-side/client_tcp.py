import socket

SERVER_IP = "127.0.0.1"
PORT = 8820
MAX_MSG_SIZE = 1024

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((SERVER_IP, PORT))

server_data = ""
while server_data != "Bye":
    client_msg = input("Please enter your message: NAME, TIME ,RAND or Quit\n")
    my_socket.send(client_msg.encode())
    server_data = my_socket.recv(MAX_MSG_SIZE).decode()
    print("The server send: " + server_data)


print("Closing TCP client socket")
my_socket.close()
