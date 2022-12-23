import socket

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

Operators = set(['+', '-', '*', '/', '(', ')', '^'])  # collection of Operators

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

            stack.append('(')

        elif character == ')':

            while stack and stack[-1] != '(':
                output += stack.pop()

            stack.pop()

        else:

            while stack and stack[-1] != '(' and Priority[character] <= Priority[stack[-1]]:
                output += stack.pop()

            stack.append(character)

    while stack:
        output += stack.pop()

    return output

def postfixEvaluator(expression):
    stack = [] # initialization of empty stack
    for character in expression:
        if character not in Operators:
            stack.append(character)
        else:
            temp1=stack.pop()
            temp2=stack.pop()
            if character == '+':
                stack.append(int(temp2)+int(temp1))
            elif character == '-':
                stack.append(int(temp2)-int(temp1))
            elif character == '*':
                stack.append(int(temp2)*int(temp1))
            elif character == '/':
                stack.append(int(temp2)/int(temp1))
    return stack.pop()


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5008  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen()

    while True:
        conn, address = server_socket.accept ()  # accept new connection
        print ( "Connection from: " + str ( address ) )
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()

        print("from connected user: " + str(data))
        inp = str(data)
        out = infixToPostfix ( inp )
        res = postfixEvaluator ( out )
        print ( "result sent to user:" + str(res) )

        data = (str(res)).encode()
        conn.send(data)  # send data to the client



if __name__ == '__main__':
    server_program()
