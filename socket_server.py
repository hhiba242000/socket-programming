import socket
import os
import signal
import sys
import math
import json

from typing import List



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

def calculate_equation(s):
    inp = str(s)
    if inp.__contains__("sin"):
        inp = inp.replace("sin(", str(math.sin(float(inp[4:inp.index(")")]))))
        tmp = inp[:inp.index(".") + 1]
        inp = inp[inp.index("."):].replace(".", "")
        inp = inp.replace(")", "")
        inp = tmp + inp

    elif inp.__contains__("exp"):
        inp = inp.replace("exp(", str(math.exp(float(inp[4:inp.index(")")]))))
        tmp = inp[:inp.index(".") + 1]
        inp = inp[inp.index("."):].replace(".", "")
        inp = inp.replace(")", "")
        inp = tmp + inp

    out = infixToPostfix(inp)
    num = postfixEvaluator(out)
    return num

def server_program():
    signal.signal(signal.SIGINT, signal_handler)
    host = "127.0.0.1"  # Standard loopback interface address (localhost)
    port = 8027
    if len(sys.argv) == 3:
        host = str(sys.argv[1])
        port = int(sys.argv[2])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind ( (host, port) )
    while True:
        server_socket.listen()
        while True:
            conn, address = server_socket.accept()
            with conn:
                print("Connection from: " + str(address))
                print("before receive\n")
                while True:
                    data = conn.recv(1024).decode()
                    print('dataaaa'+str(data))
                    if not data:
                        data = f'HTTP/1.0 500 \r\n'
                        print(data)
                        data = (str(data)).encode()
                        conn.send(data)
                        break
                    print("after receive "+str(data)+"\n")
                    split_post = data.split("\r\n")
                    print(split_post)
                    msg = split_post[4]
                    print("message "+str(msg)+"\n")
                    dict_of_eq = json.loads(str(msg))
                    list_of_eq = dict_of_eq['equations']
                    print(list_of_eq)
                    results = {}
                    results['qid'] = 1234
                    results['query'] = []
                    res=[]
                    i=1
                    for s in list_of_eq:
                        temp = {}
                        temp['id'] = str(i)
                        temp['requestedLine'] = str(s)

                        num = calculate_equation(s)
                        if type(num) == float:
                            temp['result'] = str(num)
                            #res.append(str(num))
                        else:
                            temp['result'] = 'error'
                            #res.append('error')

                        res.append(temp)
                        i=i+1
                    results['query'] = res
                    print("OUT OF FOR LOOP\n")
                    print(list_of_eq)
                    data = f'HTTP/1.0 200 OK\r\n{results}\r\n'
                    print(data)
                    data = (str(data)).encode()
                    conn.send(data)


        
        


if __name__ == '__main__':
    server_program()
