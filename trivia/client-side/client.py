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


def build_send_recv_parse(conn, command, data):
    build_and_send_message(conn, command, data)
    msg_code, data = recv_message_and_parse(conn)
    if msg_code and data:
        return msg_code, data
    error_and_exit


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
        if server_cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print("login succeed")
            return


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    print("log out succeed")


def get_score(conn):
    command = "MY_SCORE"
    data = ""
    msg_code, msg_data = build_send_recv_parse(conn, command, data)
    print(msg_data)


def get_highscore(conn):
    command = "HIGHSCORE"
    data = ""
    msg_code, msg_data = build_send_recv_parse(conn, command, data)
    print(msg_data)


def main():
    conn = connect()
    login(conn)
    while not logout(conn):
        client_choose = input("Please enter your message:\n 's'. Get my score\n 'h'.Get high score\n 'q'. Quit\n")
        switcher = {
            "s": get_score(conn),
            "h": get_highscore(conn),
            "q": logout(conn)
        }
        switcher.get(client_choose)
    print("Closing client socket")
    conn.close()


if __name__ == '__main__':
    main()
