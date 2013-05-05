import socket
import time

sock = socket.socket()
sock.connect(('localhost', 7070))
#sock.send('hello, world!')

inp = ""
inp = raw_input("Request: ")
sock.send(inp)
while True:
    data = sock.recv(1024)
    if not data:
        break
    print data[0]
sock.close()

print "client closed"
