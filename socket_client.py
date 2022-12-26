import socket
import os
import signal
import sys
import logging

# host = socket.gethostname()
# port = 5002
if len(sys.argv)==3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

logging.basicConfig(filename="./clientfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a', force=True)

# Creating an object
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

infinite_loop = True

def sig_exit(signal,frame):
    logger.info('\nYou pressed Ctrl+C, keyboardInterrupt detected,Client is exiting!')
    sys.exit(0)
    #client_socket.close()

def sig_alarm(signal,frame):
    logger.info("\nServer is busy at the moment, get back to it in another request")
    #client_socket.close()
    sys.exit(0)

def client_program():
    signal.signal(signal.SIGINT, sig_exit)
    signal.signal(signal.SIGALRM,sig_alarm)
    client_socket.connect((host, port))

    while infinite_loop == True:
        message = input(" -> ")
        client_socket.send(message.encode()) # send message
        # signal.alarm(2)
        data = client_socket.recv(1024).decode()
        # signal.alarm(0)
        if data == "bye":
            logger.info("Client is notified you left")
            break

        if not data:
            
            logger.info("Server is dead")
            break
        print('Received from server: ' + data)
        logger.info('Received from server: ' + data)  # show in terminal


    client_socket.close()  # close the connection


if __name__ == '__main__':
     client_program()


