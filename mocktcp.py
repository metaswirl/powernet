#!/usr/bin/python
'''
Description: Websocket server
Author: Niklas Semmler
'''
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.bind(('127.0.0.1', 5000))
    sock.listen(128)
except socket.error:
    print "could not listen bind to port" 
    raise
sock2, addr = sock.accept()
print sock2.recv(2048)
sock2.send("foo")
