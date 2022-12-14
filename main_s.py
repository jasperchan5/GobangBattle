import pygame,sys
from pygame.locals import QUIT
from gobang import AdminPerspect, Board
import socket
from _thread import *
import time
import random

# Initialize a server
class Server:
    def __init__(self):
        self.ServerSideSocket = socket.socket()
        self.host = '127.0.0.1'
        self.port = 2004
        self.ThreadCount = 0
        self.nowPlayer = -1
        self.Finish = False
        self.Winner = -1
        self.board_size = 15 
        self.board = []
        self.newPositionX = -1
        self.newPositionY = -1
        self.newcolor = ""
        self.color_list = ["#000000", "#000080", "#008000", "#ff0000", "#800080", "#00ff00", "#00ffff"]
        
    def initGame(self):
        try:
            self.ServerSideSocket.bind((self.host, self.port))
            print("Server is opened")
        except socket.error as e:
            print(str(e))
        print('Socket is listening..')
        self.ServerSideSocket.listen(1)
        for i in range(self.board_size):
            self.board.append([])
            for j in range(self.board_size):
                self.board[i].append(0)
        random.shuffle(self.color_list)
        Client_list = []
        while self.ThreadCount < 1:
            Client, address = self.ServerSideSocket.accept()
            Client_list.append(Client)
            start_new_thread(self.gamestart, (Client_list[self.ThreadCount], self.color_list[self.ThreadCount], self.ThreadCount))
            self.ThreadCount += 1 
            print(self.ThreadCount)   

    def send_color(self, connection, color):
        connection.send(str.encode(color))
        
    def gamestart(self, connection, color, id):
        # connection.send(str.encode('Server is working:'))
        # print(connection)
        self.send_color(connection, color)
        while not self.Finish:
            if id == self.nowPlayer:
                # ask player to play
                # newposition = get the position the player played
                connection.send(str.encode("your_turn"))
                try:
                    newPosition = connection.recv(1024).decode("utf-8")
                    self.newPositionX = int(newPosition[0])
                    self.newPositionY = int(newPosition[1])
                    newcolor = color
                except:
                    continue
            else:
                connection.send(str.encode("not_your_turn"))
                while self.newPositionX == -1 and self.newPositionY == -1:
                    continue
                while self.board[self.newPositionX][self.newPositionY]:
                    continue
                connection.send(str.encode([str(self.newPositionX), str(self.newPositionY), newcolor]))
        if id == self.Winner:
            connection.send(str.encode("you_win"))
        else:
            connection.send(str.encode("you_lose"))
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
    server = Server()
    server.initGame()
    print("start")
    admin = Board()
    resolution = (620, 620)
    black = (0, 0, 0)
    # client = Client()
    screen = admin.initGame(resolution)
    print("game inited")
    time.sleep(3)
    print(server.Finish)
    while not server.Finish:
        print("AA")
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Use "your turn", "not your turn" to determine current player
                    pos = pygame.mouse.get_pos()
                    while server.newPositionX == -1 and server.newPositionY == -1:
                        continue
                    while server.board[server.newPositionX][server.newPositionY]:
                        continue
                    displaySuccess, coord = admin.displayChess(screen, pos, black)
                    time.sleep(3)
                    if displaySuccess:
                        server.board[coord[1]][coord[0]] = True
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
        server.nowPlayer = (server.nowPlayer + 1) % 4
        print("nowPlayer=", server.nowPlayer, "\n")
        if server.Finish:
            break
                
    # client.close()
    server.close()
print("AAA")
main()
print("ASAS")