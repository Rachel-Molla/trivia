import socket
import select

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5555
MAX_MSG_LENGTH = 1024


def print_client_sockets(client_sockets):
    print("Client sockets connected:")
    for c in client_sockets:
        print("\t", c.getpeername())


def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Listening to clients...")
    client_sockets = []
    while True:
        # ready_to_read, ready_to_write, in_error = select.select(read_list, write_list, error_list)
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, [], [])
        for current_socket in ready_to_read:
            # Do something for every client
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            else:
                print("New data from client")
                data = current_socket.recv(MAX_MSG_LENGTH).decode()
                if data == "exit":
                    print("Connection closed")
                    client_sockets.remove(current_socket)
                    current_socket.close()
                    print_client_sockets(client_sockets)
                else:
                    print(data)
                    current_socket.send(data.encode())
                    print_client_sockets(client_sockets)


main()
