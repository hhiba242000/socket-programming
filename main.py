# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math

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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        inp = input("Enter input: ")
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
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
