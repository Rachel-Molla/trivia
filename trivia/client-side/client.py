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
    return msg_code, data
    # error_and_exit


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


def play_question(conn):
    """get question"""
    command = "GET_QUESTION"
    data = ""
    msg_code, msg_data = build_send_recv_parse(conn, command, data)
    print(msg_data)
    msg_data_arr = chatlib.split_data(msg_data, 5)
    trivia_question_id = msg_data_arr[0]
    question = msg_data_arr[1]
    option1 = msg_data_arr[2]
    option2 = msg_data_arr[3]
    option3 = msg_data_arr[4]
    option4 = msg_data_arr[5]
    """print question"""
    print("question: " + question + " :\n1." + option1 + "\n2. " + option2 + "\n3. " + option3 + "\n4. " + option4)
    """send answer"""
    choice = input("Please choose an answer number [1-4]: ")
    command = "SEND_ANSWER"
    msg_arr = [trivia_question_id, choice]
    data = chatlib.join_data(msg_arr)
    server_cmd, server_data = build_send_recv_parse(conn, command, data)
    """correct or wrong answer replay"""
    if server_cmd == "CORRECT_ANSWER":
        print("Your answer is correct")
    if server_data == "WRONG_ANSWER":
        print("The correct answer is " + server_data)
    # if error: return


def get_logged_users(conn):
    command = "LOGGED"
    data = ""
    server_cmd, server_data = build_send_recv_parse(conn, command, data)
    print(server_data)


def main():
    conn = connect()
    login(conn)
    while not logout(conn):
        client_choose = input("Please enter your message:\n 'p'. Play a trivia question\n 's'. Get my score\n " +
                              "'h'. Get high score\n 'l'. Get logged users\n 'q'. Quit\n")
        switcher = {
            "p": play_question(conn),
            "s": get_score(conn),
            "h": get_highscore(conn),
            "l": get_logged_users(conn),
            "q": logout(conn)
        }
        switcher.get(client_choose)
    print("Closing client socket")
    conn.close()


if __name__ == '__main__':
    main()
