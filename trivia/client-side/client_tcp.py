import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", 8820))

server_data = ""
while server_data != "Bye":
    client_msg = input("Please enter your message: NAME, TIME ,RAND or Quit\n")
    my_socket.send(client_msg.encode())
    server_data = my_socket.recv(1024).decode()
    print("The server send: " + server_data)


print("Closing client socket")
my_socket.close()



