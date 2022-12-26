import socket
import os
import signal
import sys
import logging
import math

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

if len(sys.argv)==3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind ( (host, port) )

def signal_handler(signal, frame):
    logger.info('\nYou pressed Ctrl+C, keyboardInterrupt detected,Server is exiting!')
    server_socket.close()
    sys.exit(0)

def calculateData(inp):
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
    out=infixToPostfix(inp)
    print(out)
    print(postfixEvaluator(out))
    return str(out)
    

def server_program():
    global current
    current=0
    signal.signal(signal.SIGINT, signal_handler) 
    flag=0 
    while True:
        server_socket.listen ()
        while True:
            conn, address = server_socket.accept()
            with conn:
                if (current==0):
                    current=1
                    pid = os.fork()
                    if pid !=0 :
                        # os.
                        # os.kill(int(os.getppid()), signal.SIGKILL)
                        logger.info("Connection from: " + str(address))
                        while True:
                            data = conn.recv(1024).decode()
                            if str(data) == "bye" or str(data)=="exit":
                                current=0
                                flag=1
                                server_socket.listen()
                                
                                break
                            logger.info("from connected user: " + str(data))
                            res=calculateData(str(data))
                            logger.info("result sent to user:" + str(res))

                            data = (str(res)).encode()
                            conn.send(data)
                        if flag ==1:
                            current=0
                            conn.close
                            os.kill(pid,signal.SIGKILL)
                            break
                    # else:
                    #     os.kill(0,signal.SIGKILL)
                else:
                # connE, addressE = server_socket.accept()
                # with connE:
                    message = "Server is busy."
                    conn.send(message.encode())
                    conn.close()
                    break
            # os.kill(pid,signal.SIGTERM)
            
            
    


if __name__ == '__main__':
    server_program()
