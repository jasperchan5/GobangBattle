import pygame,sys
from pygame.locals import QUIT
from gobang import Admin, Chess
import socket
from _thread import *
import time
import random

# Initialize a server
class Server:
    def __init__(self, admin, screen):
        self.ServerSideSocket = socket.socket()
        self.host = '127.0.0.1'
        self.port = 2004
        self.ThreadCount = 0
        self.nowPlayer = 0
        self.Finish = False
        self.Winner = -1
        self.board_size = 15 
        self.board = []
        self.newPositionX = -1
        self.newPositionY = -1
        self.newcolor = ""
        self.color_list = ["#000000", "#000080", "#008000", "#ff0000", "#800080", "#00ff00", "#00ffff"]
        self.totalPlayerCnt = 4
        self.game = admin
        self.screen = screen
        self.chessPlaced = False
        
    def initGame(self):
        try:
            self.ServerSideSocket.bind((self.host, self.port))
            print("Server is opened")
        except socket.error as e:
            print(str(e))
        print('Socket is listening..')
        self.ServerSideSocket.listen(self.totalPlayerCnt)
        for i in range(self.board_size):
            self.board.append([])
            for j in range(self.board_size):
                self.board[i].append(0)
        print("Board generated")
        random.shuffle(self.color_list)
        Client_list = []
        while self.ThreadCount < self.totalPlayerCnt:
            Client, address = self.ServerSideSocket.accept()
            Client_list.append(Client)
            self.ThreadCount += 1 
            print(self.ThreadCount)   
        for t, client in enumerate(Client_list):
            start_new_thread(self.gamestart, (client, self.color_list[t], t))

    def gamestart(self, connection, color, id):
        # connection.send(str.encode('Server is working:'))
        # print(connection)
        connection.send(str.encode(str(id+1)))
        connection.send(str.encode(color))
        
        while not self.Finish:
            if self.Winner == -1:
                if id == self.nowPlayer:
                    print(f"Thread{id}. It's player {id+1}'s turn!")
                    # ask player to play
                    # newposition = get the position the player played
                    connection.send(str.encode("your_turn"))
                    try:
                        newPosition = connection.recv(1024).decode("utf-8")                   
                        self.newPositionX, self.newPositionY = int(newPosition.split(",")[0]), int(newPosition.split(",")[1])
                        self.actualPositionX, self.actualPositionY = int(newPosition.split(",")[2]), int(newPosition.split(",")[3])
                        self.newcolor = color
                        
                        self.board[self.newPositionX][self.newPositionY] = 1
                        newChess = Chess(self.screen, color, (self.actualPositionX, self.actualPositionY))
                        
                        pygame.draw.circle(newChess.gameScreen, newChess.color, newChess.centerCoord, newChess.radius)
                        pygame.display.update()
                        if self.game.endGame():
                            print(f"Player {id} wins!")
                            self.Winner = id
                            continue
                        else:
                            self.chessPlaced = True
                            self.nowPlayer = (self.nowPlayer + 1) % self.totalPlayerCnt
                            time.sleep(3)
                            self.newPositionX, self.newPositionY = -1, -1
                    except:
                        print("No new position received")
                        continue
                else:
                    connection.send(str.encode("not_your_turn"))
                    while self.newPositionX == -1 and self.newPositionY == -1:
                        continue
                    while self.board[self.newPositionX][self.newPositionY] == 0:
                        continue
                    time.sleep(3)
                    connection.send(str.encode(f"{str(self.actualPositionX)},{str(self.actualPositionY)},{self.newcolor}"))
            else:
                if id == self.Winner:
                    print("you win!")
                    connection.send(str.encode("you_win"))
                    break
                else:
                    print("you lose!")
                    connection.send(str.encode("you_lose"))
                    break
        time.sleep(10)
        connection.close()

    def close(self):
        self.ServerSideSocket.close()

# # Initialize clients
# class Client:
#     def __init__(self):
#         self.ClientMultiSocket = socket.socket()
#         self.host = '127.0.0.1'
#         self.port = 2004
#         print('Waiting for connection response')
#         try:
#             self.ClientMultiSocket.connect((self.host, self.port))
#         except socket.error as e:
#             print(str(e))
#         self.color = ""
#         self.newPositionX = 0
#         self.newPositionY = 0
#         self.newColor = ""
#         self.getPosition = False
        
#     def startClient(self):
#         self.color = self.ClientMultiSocket.recv(1024).decode("utf-8")
    
#     def gameProcess(self):
#         while True:
#             try:
#                 message = self.ClientMultiSocket.recv(1024).decode("utf-8")
#                 if message == "your_turn":
#                     while not self.getPosition:
#                         continue
#                     # Send chess displayed position
#                     # newPositionX = int(xx)
#                     # newPositionY = int(yy) 
#                     self.ClientMultiSocket.send(str.encode([str(newPositionX), str(newPositionY)])) # we need to get newposition from JC

#                 elif message == "not_your_turn":
#                     # Display the other 3 players' status
#                     step = self.ClientMultiSocket.recv(1024).decode("utf-8")
#                     newPositionX = step[0]
#                     newPositionY = step[1]
#                     self.newColor = step[2]
#                 elif message == "you_win":
#                     # render win in this line
#                     break

#                 elif message == "you_lose":
#                     # render lose in this line
#                     break
#             except:
#                 continue
        
#     def close(self):
#         self.ClientMultiSocket.close()


def main():
    admin = Admin()
    resolution = (620, 620)
    screen = admin.initGame(resolution)
    server = Server(admin, screen)
    server.initGame()
    while not server.Finish:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
    # client.close()
    server.close()
main()