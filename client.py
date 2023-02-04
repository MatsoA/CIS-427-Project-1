import socket
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 3108))

message = s.recv(2108)

print(str(message))