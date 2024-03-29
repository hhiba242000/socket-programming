import socket
import json
import os
import socket
import sys
from typing import List

host = "127.0.0.1"
port = 8027  # take it as argument from command line

def prepare_packet(port, host, data):
    i = len(data)
    # print(data + " &&&&&&&" + str(i))
    return f"POST /session HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {i}\r\n{data}\r\n"


def extract_data(data):
    split_post = data.split("\r\n")
    # print(split_post)
    msg = split_post[1]
    # print("msg " + str(msg)+" in function\n")
    return msg

def client_program():
        host = "127.0.0.1"  # Standard loopback interface address (localhost)
        port = 8027
        if len(sys.argv) == 3:
            host = str(sys.argv[1])
            port = int(sys.argv[2])

        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # SOCK_STREAM for TCP sockets and SOCK_DGRAM for UDP sockets
        client_socket.connect((host, port))

        while True:
            jsonResult = {}
            jsonResult['equations'] = []
            while True:
                message = input(" -> ")
                if message == '':
                    break
                else:
                    jsonResult['equations'].append(message)


            jsonResult = json.dumps(jsonResult)
            jsonResult = prepare_packet(port, host,jsonResult)

            client_socket.send(bytes(jsonResult.encode()))
            # print("waiting to receive in client\n")
            data = client_socket.recv(1024).decode()
            # print("after receive in client\n")
            # print(data)
            if not data:
                break
            data = extract_data(data)
            # print("after extraction")
            if data == "bye":
                print("Client is notified you left")
                break

            print('Received from server: ' + str(data))

        client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
