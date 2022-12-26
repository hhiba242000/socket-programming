import socket
import logging
import signal
import sys
import argparse

def signal_handler(signal, frame):
    logger.info('\nYou pressed Ctrl+C, keyboardInterrupt detected,Client is exiting!')
    sys.exit(0)

def client_program():
    signal.signal(signal.SIGINT, signal_handler)
    logging.basicConfig(filename="./clientfile.log",
                        format='%(asctime)s %(message)s',
                        filemode='w', force=True)
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if len(sys.argv) == 3:
        for i in sys.argv:
            print(str(i))
        host = str(sys.argv[1])
        port = int(sys.argv[2])
    else:
        host = '127.0.0.1'
        port = 5005

    print(host)
    print(port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM for TCP sockets and SOCK_DGRAM for UDP sockets
    client_socket.connect((host, port))

    while True:
        message = input(" -> ")
        logger.info("message sent to server "+message)
        client_socket.sendall(message.encode())  # send message

        data = client_socket.recv(1024).decode() # receive response
        if data == "bye":
            logger.info("Server is notified you left")
            break

        if  not data :
            logger.info("Server is dead")
            break
        logger.info('Received from server: ' + data)  # show in terminal

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()