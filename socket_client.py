import socket


def client_program():
    host = socket.gethostname()
    port = 5004 #take it as argument from command line

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM for TCP sockets and SOCK_DGRAM for UDP sockets
    client_socket.connect((host, port))

    while True:
        message = input(" -> ")
        client_socket.sendall(message.encode())  # send message

        data = client_socket.recv(1024).decode() # receive response
        if data == "bye":
            print("Client is notified you left")
            break

        if  not data :
            print("Server is dead")
            break
        print('Received from server: ' + data)  # show in terminal

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()