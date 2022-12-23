# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


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
                stack.append(float(temp2)+float(temp1))
            elif character == '-':
                stack.append(float(temp2)-float(temp1))
            elif character == '*':
                stack.append(float(temp2)*float(temp1))
            elif character == '/':
                stack.append(float(temp2)/float(temp1))
    return stack.pop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        inp = input("Enter input: ")
        print(inp)
        out=infixToPostfix(inp)
        print(out)
        print(postfixEvaluator(out))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
