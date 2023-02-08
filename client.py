import socket
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 3108))
response = ""
message = ""
while True:
    #send command to server
    message = input(">> ")
    response = ""
    s.send(message.encode('ascii'))

    message = message.upper()
    if (message == "QUIT"):
        break
    if (message == "SHUTDOWN"):
        s.shutdown(1) #indicates client is done sending but will wait for a final receive
        print(s.recv(2108).decode('ascii'))
        break
    #read response from server
    response = s.recv(6000).decode('ascii')
    print(response)
s.close()