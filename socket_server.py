import socket
import os
import signal
import sys
import logging

logging.basicConfig(filename="./serverfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a', force=True)

# Creating an object
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print ( f'Hi, {name}' )  # Press Ctrl+F8 to toggle the breakpoint.


Operators = set ( [ '+', '-', '*', '/', '(', ')', '^' ] )  # collection of Operators

Priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}  # dictionary having priorities of Operators


def infixToPostfix(expression):
    stack = [ ]  # initialization of empty stack

    output = ''

    for character in expression:
        if character == ' ':
            continue
        if character not in Operators:  # if an operand append in postfix expression

            output += character

        elif character == '(':  # else Operators push onto stack

            stack.append ( '(' )

        elif character == ')':

            while stack and stack [ -1 ] != '(':
                output += stack.pop ()

            stack.pop ()

        else:

            while stack and stack [ -1 ] != '(' and Priority [ character ] <= Priority [ stack [ -1 ] ]:
                output += stack.pop ()

            stack.append ( character )

    while stack:
        output += stack.pop ()

    return output


def postfixEvaluator(expression):
    stack = [ ]  # initialization of empty stack
    for character in expression:
        if character not in Operators:
            stack.append ( character )
        else:
            temp1 = stack.pop ()
            temp2 = stack.pop ()
            if character == '+':
                stack.append ( int ( temp2 ) + int ( temp1 ) )
            elif character == '-':
                stack.append ( int ( temp2 ) - int ( temp1 ) )
            elif character == '*':
                stack.append ( int ( temp2 ) * int ( temp1 ) )
            elif character == '/':
                stack.append ( int ( temp2 ) / int ( temp1 ) )
    return stack.pop ()
if len(sys.argv)==3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind ( (host, port) )

def signal_handler(signal, frame):
    logger.info('\nYou pressed Ctrl+C, keyboardInterrupt detected,Server is exiting!')
    server_socket.close()
    sys.exit(0)

def server_program():
    current=0
    signal.signal(signal.SIGINT, signal_handler)  
    while True:
        server_socket.listen ()
        while True:
            conn, address = server_socket.accept()
            with conn:
                if (current==0):
                    current=1
                    logger.info("Connection from: " + str(address))
                    while True:
                        data = conn.recv(1024).decode()
                        if str(data) == "bye" or str(data)=="":
                            current=0
                            break
                        logger.info("from connected user: " + str(data))
                        inp = str(data)
                        out = infixToPostfix(inp)
                        res = postfixEvaluator(out)
                        logger.info("result sent to user:" + str(res))

                        data = (str(res)).encode()
                        conn.send(data)
                else:
                    # connE, addressE = server_socket.accept()
                    # with connE:
                    message = "Server is busy."
                    conn.send(message.encode())
                    conn.close()
                    break
                
            
    


if __name__ == '__main__':
    server_program()
