import socket

from trivia import chatlib

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    client_msg = chatlib.build_message(code, data)
    conn.send(client_msg.encode())


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data


def connect():
    socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_to_server.connect((SERVER_IP, SERVER_PORT))
    return socket_to_server


def error_and_exit(error_msg):
    print(error_msg)
    exit()


def login(conn):
    while chatlib.PROTOCOL_SERVER["login_failed_msg"]:
        username = input("Please enter username: \n")
        password = input("Please enter your password: \n")
        client_login_details = [username, password]
        client_login_msg = chatlib.join_data(client_login_details)
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], client_login_msg)
        server_cmd, server_msg = recv_message_and_parse(conn)
        if server_msg == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print(chatlib.PROTOCOL_SERVER["login_ok_msg"])
            return


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    print("log out succeed")


def main():
    conn = connect()
    login(conn)
    logout(conn)
    print("Closing client socket")
    conn.close()


if __name__ == '__main__':
    main()
