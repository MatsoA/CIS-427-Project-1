import socket
import sys
port = 3107
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## creates socket
s.connect((sys.argv[1], port)) ## Connects to the socket at port number
response = ""
message = ""

while True:
#   send command to server
    message = input(">> ").upper()
    response = ""
    s.send(message.encode('ascii'))

#   message = message.upper()
    if (message == "QUIT"): ## QUIT stops client
        break
    if (message == "SHUTDOWN"): ## SHUTDOWN stops server
        s.shutdown(1) #indicates client is done sending but will wait for a final receive
        print(s.recv(2108).decode('ascii'))
        break
    #read response from server
    response = s.recv(6000).decode('ascii')
    print(response)
    
s.close()