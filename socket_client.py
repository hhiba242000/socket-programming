import socket
import json

def client_program():

    host = socket.gethostname()
    port = 5003 #take it as argument from command line

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM for TCP sockets and SOCK_DGRAM for UDP sockets
    client_socket.connect((host, port))

    while True:
        infinite_loop = True
        jsonResult={}
        jsonResult['equations']=[]
        #jsonResult=json.dumps(jsonResult)
        while True:
            message = input(" -> ")
            if message == '':
                break
            else:
                jsonResult['equations'].append(message)

        jsonResult = json.dumps(jsonResult)

        client_socket.send(bytes(jsonResult.encode())) # send message

        data = client_socket.recv(1024) # receive response
        if data == "bye":
            print("Client is notified you left")
            break

        if  not data :
            print("Server is dead")
            break
        print('Received from server: ' + str(data))  # show in terminal

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()