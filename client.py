import socket
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 3108))

response = ""

while response != "Bye":

    #send command to server
    message = input()
    s.send(message.encode('ascii'))

    #read response from server
    response = s.recv(2108).decode('ascii')
    print(response)

