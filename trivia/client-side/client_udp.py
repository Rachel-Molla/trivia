import socket
import random

SERVER_IP = "127.0.0.1"
PORT = 8821
MAX_MSG_SIZE = 1024
TIMEOUT_IN_SECONDS = 2000


def special_sendto(socket_object, response, client_address):
    fail = random.randint(1, 3)
    if not (fail == 1):
        socket_object.sendto(response.encode(), client_address)
    else:
        print("Oops")


my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
packet = ""

while packet != "EXIT":

    packet = input("Please enter your message (insert 'EXIT' to quit):\n")
    special_sendto(my_socket, packet, (SERVER_IP, PORT))
    my_socket.settimeout(TIMEOUT_IN_SECONDS)
    try:
        (response, remote_address) = my_socket.recvfrom(MAX_MSG_SIZE)
        data = response.decode()
        print("The server sent " + data)
    except IndexError:
        print("This code reached despite server not answering")


print("Closing UDP client socket")
my_socket.close()
