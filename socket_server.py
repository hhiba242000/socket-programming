import socket
import os
import signal
import sys
import math
import logging

global logger
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print ( f'Hi, {name}' )  # Press Ctrl+F8 to toggle the breakpoint.

Operators = set ( [ '+', '-', '*', '/', '(', ')', '^' ] )  # collection of Operators

Priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}  # dictionary having priorities of Operators


def infixToPostfix(expression):
    stack = []  # initialization of empty stack

    output = ''

    for character in expression:
        if character == ' ':
            continue
        if character not in Operators:  # if an operand append in postfix expression

            output += character

        elif character == '(':  # else Operators push onto stack
            output+=' '
            stack.append('(')

        elif character == ')':
            output+=' '
            while stack and stack[-1] != '(':
                output += stack.pop()

            stack.pop()

        else:
            output+=' '
            while stack and stack[-1] != '(' and Priority[character] <= Priority[stack[-1]]:
                output += stack.pop()

            stack.append(character)
    output+=' '
    while stack:
        output += stack.pop()

    return output

def postfixEvaluator(expression):
    stack = [] # initialization of empty stack
    numberTemp1=''
    for character in expression:
        if character not in Operators and character != ' ':
            numberTemp1+=character
            continue
        elif character==' ':
            stack.append(float(numberTemp1))
            numberTemp1=''
            continue
        else:
            temp1 = stack.pop()
            temp2 = stack.pop()
            if character == '+':
                stack.append(float(temp2)+float(temp1))
            elif character == '-':
                stack.append(float(temp2)-float(temp1))
            elif character == '*':
                stack.append(float(temp2)*float(temp1))
            elif character == '/':
                stack.append(float(temp2)/float(temp1))
            elif character == '^':
                stack.append(math.pow(float(temp2),float(temp1)))
    return stack.pop()


def signal_handler(signal, frame):
    logger.info('\nYou pressed Ctrl+C, keyboardInterrupt detected,Client is exiting!')
    print('\nYou pressed Ctrl+C, keyboardInterrupt detected,Client is exiting!')
    sys.exit(0)
def calculate_result(data):
    inp = str(data)
    if inp.__contains__ ( "sin" ):
        inp = inp.replace ( "sin(", str ( math.sin ( float ( inp[4:inp.index(")")] ) ) ) )
        tmp = inp[:inp.index(".")+1]
        inp = inp[inp.index("."):].replace(".", "")
        inp = inp.replace ( ")", "" )
        inp = tmp + inp
            
    elif inp.__contains__ ( "exp" ):
        inp = inp.replace ( "exp(", str ( math.exp ( float ( inp[4:inp.index(")")] ) ) ) )
        tmp = inp[:inp.index(".")+1]
        inp = inp[inp.index("."):].replace(".", "")
        inp = inp.replace ( ")", "" )
        inp = tmp + inp
    print(inp)

    out = infixToPostfix(inp)
    res = postfixEvaluator(out)
    return res

def server_program():
    signal.signal(signal.SIGINT, signal_handler)
    logging.basicConfig(filename="./serverfile.log",
                        format='%(asctime)s %(message)s',
                        filemode='w', force=True)
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if len(sys.argv) == 3:
        # for i in sys.argv:
        #     print(str(i))
        host = str(sys.argv[1])
        port = int(sys.argv[2])
    else:
        host = '127.0.0.1'
        port = 5005

    # print(host)
    # print(port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind ( (host, port) )
    while True:
        server_socket.listen()
        while True:
            conn, address = server_socket.accept()
            with conn:
                pid = os.fork()
                if pid == 0:
                    logger.info("Connection from: " + str(address))
                    print("Connection from: " + str(address))
                    while True:
                        data = conn.recv(1024).decode()
                        logger.info("data decoded: "+str(data))
                        print("data decoded: "+str(data))
                        if str(data) == "bye":
                            data = "bye"
                            logger.info("Client is wants to leave")
                            print("Client is wants to leave")
                            conn.send(data.encode())
                            break

                        if not data:
                            data = "nothing"
                            logger.info("Client exited by keyboard interrupt")
                            print("Client exited by keyboard interrupt")
                            break
                        res = calculate_result(data)
                        if not res:
                            res = "NaN"
                        logger.info("result sent to user:" + str(res))
                        print("result sent to user " + str(address[1]) +" :" + str(res))
                        data = (str(res)).encode()
                        conn.send(data)

        
        


if __name__ == '__main__':
    server_program()
