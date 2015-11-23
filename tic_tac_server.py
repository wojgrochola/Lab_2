# Tcp Chat server
 
import socket, select, sys
 #Tic tac toe
import random

class TicTacToeGame:
    def __init__(self, name1, name2, mark1, mark2):
        self.player1 = name1
        self.player2 = name2
        self.player1Mark = mark1
        self.player2Mark = mark2
        self.players = []
        self.marks = []
        self.board = [' '] * 10
        
    def printBoard(self):
        val = '\n'
        val += '   |   |   |\n'
        val += (' ' + self.board[7] + ' | ' + self.board[8] + ' | ' + self.board[9] + ' |\n')
        val += ('   |   |   |\n')
        val += ('--------------\n')
        val += ('   |   |   |\n')
        val += (' ' + self.board[4] + ' | ' + self.board[5] + ' | ' + self.board[6] + ' |\n')
        val += ('   |   |   |\n')
        val += ('--------------\n')
        val += ('   |   |   |\n')
        val += (' ' + self.board[1] + ' | ' + self.board[2] + ' | ' + self.board[3] + ' |\n')
        val += ('   |   |   |\n')
        return val

    def selectMark(self):
        mark = ''
        print ("Select Mark for player I:\n")
        while not (mark == 'X' or mark == 'O'):
            print ("Select X or O: ")
            mark = raw_input()
            mark = mark.upper()

    def playAgain(self):
        print ("Play again, yes or no?")
        decision = raw_input().lower()
        if (decision.startswith('y')):
            return True
        else:
            return False

    def makeMove(self, move, mark):
        self.board[move] = mark

    def isWin(self, mark):
        val = False
        if ((self.board[1] == mark and self.board[2] == mark and self.board[3] == mark) or
        (self.board[4] == mark and self.board[5] == mark and self.board[6] == mark) or
        (self.board[7] == mark and self.board[8] == mark and self.board[9] == mark) or
        (self.board[1] == mark and self.board[4] == mark and self.board[7] == mark) or
        (self.board[2] == mark and self.board[5] == mark and self.board[8] == mark) or
        (self.board[3] == mark and self.board[6] == mark and self.board[9] == mark) or
        (self.board[3] == mark and self.board[5] == mark and self.board[7] == mark) or
        (self.board[1] == mark and self.board[5] == mark and self.board[9] == mark)):
            val = True

        return val


    def isMovePossible(self, move):
        try: 
            if (self.board[int(move)] == ' '):
                return True
            else:
                
                return False
        except:
            return False

    def validMove(self, move):
        try:
            if (int(move) in '1 2 3 4 5 6 7 8 9'.split()):
                return True
            else:
                return False
        except:
            return False

    def getPlayerMove(self, name):
        move = ' '
        while ( not self.validMove(move) or not self.isMovePossible(move) ):
            if (move != ' ' and not self.isMovePossible(move)):
                print ("Move is not possibile!")
            print (name + " - your move (1-9): ")
            move = raw_input()
        return int(move)

    def getRandomMove(self):
        moveList = ['X', 'O']
        possibileMoves = []
        for i in moveList:
            if self.isMovePossible(i):
                possibileMoves.append(i)
        if len(possibileMoves) != 0:
            return random.choice(possibileMoves)
        else:
            print("No possibile moves.")
            sys.exit();

    def isBoardFull(self):
        for i in range(1,10):
            if self.isMovePossible(i):
                return False
            
        return True

    def playGame(self):
        print ("Welcome in Tic Tac Toe!")

        while True:
            self.board = [' '] * 10
            player1Mark = 'X'
            player2Mark = 'O'
            turn = self.player1
            print ("Player 1 letter is X, Player 2 is O")
            isPlaying = True;
            turn == self.player1
            mark = self.player1Mark
            while isPlaying:
                    self.printBoard()
                    move = self.getPlayerMove(turn)
                    self.makeMove(move, mark)
                    if self.isWin(mark):
                        self.printBoard()
                        print (turn +  " win!")
                        isPlaying = False
                    else: 
                        if self.isBoardFull():
                            self.printBoard()
                            print("A tie!")
                            isPlaying = False
                    if (turn == self.player1):
                        turn = self.player2
                        mark = self.player2Mark
                    else:
                        turn = self.player1
                        mark = self.player1Mark
            if not self.playAgain():
                break



# if __name__ == "__main__":
#     print("Graczu 1 podaj swoje imie: ")
#     name1 = raw_input()
#     print(name1 + ", jakim znakiem chcesz grac?: ")
#     mark1 = raw_input()

#     print("Graczu 2 podaj swoje imie: ")
#     name2 = raw_input()
#     print(name2 + ", jakim znakiem chcesz grac?: ")
#     mark2 = raw_input()

#     game = TicTacToeGame(name1, name2, mark1, mark2)
#     game.playGame()
#Function to broadcast chat messages to all connected clients

class Server:
    def __init__(self):
        self.PORT = 5000
        self.HOST = 'localhost'
        self.RECV_BUFFER = 4096
        self.createTcpIpSocket()
        self.bindSocketToThePort()
        self.startListen()

    def createTcpIpSocket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bindSocketToThePort(self):
        self.server_address = (self.HOST, self.PORT)
        print ("Bind to %s port %s" % self.server_address)
        self.server_socket.bind(self.server_address)

    def startListen(self):
        self.CONNECTION_LIST = []
        self.server_socket.listen(1)
        self.CONNECTION_LIST.append(self.server_socket)
        print "Chat server started on port " + str(self.PORT)

    def closeSocket(self):
        self.server_socket.close()

    def run(self):
        full = False
        tic_tac = TicTacToeGame("ja", "ty", "x", "o")
        player_index = 0
        isPlaying = True
        while 1:
            while isPlaying: 
                read_sockets,write_sockets,error_sockets = select.select(self.CONNECTION_LIST,[],[])

                       
           
                for sock in read_sockets:
                    number_of_players = len(self.CONNECTION_LIST)-1
                     # nowe polaczenie 
                    if sock == self.server_socket:
                        if number_of_players == 2:
                            full = True
                       
                        sockfd,addres = self.server_socket.accept()
                        if full:
                            sockfd.send("no")
                            sockfd.close()
                        else:
                            sockfd.send("yes")
                            self.CONNECTION_LIST.append(sockfd)
                            print ("Client append: %s, %s" % addres)
                            player = sockfd.recv(self.RECV_BUFFER)
                            tic_tac.players.append(player)
                            mark = sockfd.recv(self.RECV_BUFFER)
                            tic_tac.marks.append(mark)
                            print (player + ", " + mark)


                    else:
                        try:
                            move, player = sock.recv(self.RECV_BUFFER).split(":")

                            if (tic_tac.players[player_index] == player):
                                mark = tic_tac.marks[player_index]
                                print (move + " , " + player)
                                if move:
                                    while ( tic_tac.validMove(move) or not tic_tac.isMovePossible(move) ):
                                        sock.send("Pole jest zajete, lub wpisales zly znak. Sprobuj jeszcze raz (1-9): \n")
                                        move, player = sock.recv(self.RECV_BUFFER).split(":")

                                    tic_tac.makeMove(int(move), mark)
                                    if (tic_tac.isWin(mark)):
                                        self.broadcast_data(sock, "------ " + player + ": WIN! --------", 'all')
                                        self.broadcast_data(sock, tic_tac.printBoard(), 'all')
                                        isPlaying = False

                                    else: 
                                        sock.send("Twoj ruch: " + move)

                                        self.broadcast_data(sock, player + ": " + move, 'opp')
                                        self.broadcast_data(sock, tic_tac.printBoard(), 'all')
                                        if player_index == 1:
                                            player_index = 0
                                        else:
                                            player_index = 1
                            else:
                                sock.send("Teraz gra ktos inny!")
                        except:
                            print("Client (%s, %s) is offline: " % addres)
                            sock.close()
                            self.CONNECTION_LIST.remove(sock)
                            continue

    def broadcast_data (self, sock, message, mode):
        #Do not send the message to master socket and the client who has send us the message
        for socket in self.CONNECTION_LIST:
            if (mode == 'all'):
                if socket != self.server_socket :
                    try :
                        socket.send(message)
                    except :
                        # broken socket connection may be, chat client pressed ctrl+c for example
                        socket.close()
                        self.CONNECTION_LIST.remove(socket)
            else:
                if socket != self.server_socket  and socket != sock:
                    try :
                        socket.send(message)
                    except :
                        # broken socket connection may be, chat client pressed ctrl+c for example
                        socket.close()
                        self.CONNECTION_LIST.remove(socket)
 
if __name__ == "__main__":
    Server = Server()
    Server.run()
    
    
    
     
   