# telnet program example
import socket, select, string, sys
 

class Client:
    def __init__(self):
        self.PORT = 5000
        self.HOST = 'localhost'
        self.RECV_BUFFER = 4096
        self.createTcpIpSocket()
        self.connect()

    def createTcpIpSocket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)

    def connect(self):
        try :
            self.client_socket.connect((self.HOST, self.PORT))
        except :
            print 'Unable to connect'
            sys.exit()
    def run(self):
        decision = self.client_socket.recv(4096) 
        if(decision == 'no'):
            print ("Serwer pelny!")
            sys.exit()
        print ("Podaj swoje imie: ")
        playerName = raw_input();
        self.client_socket.send(playerName)
        print ("Podaj znak jakim chcesz grac: ")
        playerMark = raw_input();
        self.client_socket.send(playerMark) 
        print 'Connected to remote host. Start sending messages'
        self.prompt()    

        while 1:    
            socket_list = [sys.stdin, self.client_socket]

            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

            for sock in read_sockets:
                if sock == self.client_socket:
                    data = sock.recv(4096)
                    if not data :
                        print '\nDisconnected from chat server'
                        sys.exit()
                    else :
                        sys.stdout.write(data)
                        self.prompt()
                else :
                    move = sys.stdin.readline()
                    msg = move.rstrip() + ":" + playerName
                    self.client_socket.send(msg)

    def prompt(self) :
        sys.stdout.write('<You> ')
        sys.stdout.flush()        

    
#main function
if __name__ == "__main__":
     
   Client = Client()
   Client.run()
     
    # connect to remote host
    
    
    
    
    
                