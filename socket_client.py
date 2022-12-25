import socket
import os
import signal
import sys

infinite_loop = True
socket client_socket = None
def sig_exit(signal,frame):
    print('\nYou pressed Ctrl+C, keyboardInterrupt detected,Client is exiting!')
    client_socket.close()

def sig_alarm(signal,frame):
    print("\nClient is busy at the moment, get back to it in another request")
    sys.exit(0)

def client_program():
    signal.signal(signal.SIGINT, sig_exit)
    signal.signal(signal.SIGALRM,sig_alarm)
    host = socket.gethostname()
    port = 5003

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while infinite_loop == True:
        message = input(" -> ")
        client_socket.send(message.encode()) # send message
        print("before receive\n")
        signal.alarm(5)
        data = client_socket.recv(1024).decode()
        signal.alarm(0)
        print("after receive\n")# receive response
        if data == "bye":
            print("Client is notified you left")
            break

        if not data:
            print("Server is dead")
            break

        print('Received from server: ' + data)  # show in terminal


    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()

import socket

