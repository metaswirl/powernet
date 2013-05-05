import socket

sock = socket.socket()
sock.bind(('', 7070))
sock.listen(1)
conn, addr = sock.accept()

print 'connected:', addr

data = conn.recv(2048)

#peterfunction(data, sock)
conn.close()
print "server closed"
