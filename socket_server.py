import socket
import os
import signal
import sys
import math
import json

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
                stack.append(float(temp2) / float(temp1))
            return stack.pop()

def signal_handler(signal, frame):
    print('\nYou pressed Ctrl+C, keyboardInterrupt detected,Server is exiting!')
    sys.exit(0)


def server_program():
    signal.signal(signal.SIGINT, signal_handler)
    host = socket.gethostname ()
    port = 5003

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind ( (host, port) )
    while True:
        server_socket.listen()
        while True:
            conn, address = server_socket.accept()
            with conn:
                pid = os.fork()
                if pid == 0:
                    print("Connection from: " + str(address))
                    while True:
                        data = conn.recv(1024).decode()
                        dict_of_eq = json.loads(str(data))
                        list_of_eq = dict_of_eq['equations']
                        results = {}
                        results['result'] = []
                        res=[]
                        for s in list_of_eq:
                            inp = str(s)
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

                            out = infixToPostfix(inp)
                            num = postfixEvaluator(out)
                            if type(num) == float:
                                res.append(str(num))
                            else:
                                res.append('error')

                        results['result'].append(res)
                        print("dictionary")
                        print(list_of_eq)
                        data = (str(results)).encode()
                        conn.send(data)

        
        


if __name__ == '__main__':
    server_program()
