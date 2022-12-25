import socket
import os
import signal
import sys

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


def signal_handler(signal, frame):
    print('\nYou pressed Ctrl+C, keyboardInterrupt detected,Server is exiting!')
    sys.exit(0)

def server_program():
    signal.signal(signal.SIGINT, signal_handler)
    host = socket.gethostname ()
    port = 5003

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind ( (host, port) )
    server_socket.listen (0)
    while True:
        conn, address = server_socket.accept()
        with conn:
            print("Connection from: " + str(address))
            while True:
                data = conn.recv(1024).decode()
                if str(data) == "bye":
                    break
                print("from connected user: " + str(data))
                inp = str(data)
                out = infixToPostfix(inp)
                res = postfixEvaluator(out)
                print("result sent to user:" + str(res))

                data = (str(res)).encode()
                conn.send(data)


if __name__ == '__main__':
    server_program()
