import socket
import Stage_0a_Manager as Stage0a
import Stage_4_Database as Stage4


if __name__=="__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', 7080))
        sock.listen(1)
        conn, addr = sock.accept()
    except:
        print "foobar server"
    
    print 'connected:', addr
    
    data = conn.recv(2048)
    
    data="".join(data)
    sqlAcc=Stage4.SQLAccess()
    facts = sqlAcc.give_input(data)
    if facts == []:
        Stage0a.main(data, conn)
    else:
        #conn.send("")
        Stage0a.send(facts, conn)
        Stage0a.main(data, conn)
    conn.close()
    print "server closed"
