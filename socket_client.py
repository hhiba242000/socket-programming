import socket
import os
import signal
import sys
import logging

logging.info('hello')
infinite_loop = True

def sig_exit(signal,frame):
    print('\nYou pressed Ctrl+C, keyboardInterrupt detected,Client is exiting!')
    sys.exit(0)
    #client_socket.close()

def sig_alarm(signal,frame):
    print("\nClient is busy at the moment, get back to it in another request")
    #client_socket.close()
    sys.exit(0)

def client_program():
    signal.signal(signal.SIGINT, sig_exit)
    signal.signal(signal.SIGALRM,sig_alarm)
    host = socket.gethostname()
    port = 5002

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
    logging.basicConfig(filename="newfile.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

    # Creating an object
    logger = logging.getLogger()

    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)

    # Test messages
    logger.debug("Harmless debug Message")
    logger.info("Just an information")
    logger.warning("Its a Warning")
    logger.error("Did you try to divide by zero")
    logger.critical("Internet is down")
    # client_program()


