import socket


def client_program():
    host = socket.gethostname()
    port = 5008

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        message = input(" -> ")
        client_socket.send(message.encode())  # send message
        if message == "bye":
            break
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal


    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()