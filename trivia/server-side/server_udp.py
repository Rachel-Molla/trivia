import socket
import random

SERVER_IP = "0.0.0.0"
PORT = 8821
MAX_MSG_SIZE = 1024
SERIAL_NUMBER_FIELD_SIZE = 4
MAX_SERIAL_NUM = 10000


def special_sendto(socket_object, response, client_address):
    fail = random.randint(1, 3)
    if not (fail == 1):
        socket_object.sendto(response.encode(), client_address)
    else:
        print("Oops")


request_serial_number = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, PORT))
data = ""


while data != "EXIT":

    (client_message, client_address) = server_socket.recvfrom(MAX_MSG_SIZE)
    data = client_message.decode()

    serial_number_field = str(request_serial_number).zfill(SERIAL_NUMBER_FIELD_SIZE)
    request_serial_number += 1
    if request_serial_number == MAX_SERIAL_NUM:
        request_serial_number = 0

    print("Client send " + data + ", request_serial_number: " + serial_number_field)
    response = "Super " + data
    special_sendto(server_socket, response, client_address)

server_socket.close()
