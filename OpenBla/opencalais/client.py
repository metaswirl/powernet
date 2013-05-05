import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect(('localhost', 7080))
except:
    print "foobar client"
#sock.send('hello, world!')

inp = ""
inp = raw_input("Request: ")
sock.send(inp)
while True:
    data = sock.recv(2048)
    if not data:
        break
    print len(data)
    print data
sock.close()

print "client closed"
