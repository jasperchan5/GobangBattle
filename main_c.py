import pygame,sys
from pygame.locals import QUIT
from gobang import Board, Chess
import socket
from _thread import *
import time
import random

# # Initialize a server
# class Server:
#     def __init__(self):
#         self.ServerSideSocket = socket.socket()
#         self.host = '127.0.0.1'
#         self.port = 2004
#         self.ThreadCount = 0
#         self.nowPlayer = -1
#         self.Finish = False
#         self.Winner = -1
#         self.board_size = 15 
#         self.board = []
#         self.newPositionX = -1
#         self.newPositionY = -1
#         self.newcolor = ""
#         self.color_list = ["#000000", "#000080", "#008000", "#ff0000", "#800080", "#00ff00", "#00ffff"]
        
#     def startGame(self):
#         try:
#             self.ServerSideSocket.bind((self.host, self.port))
#         except socket.error as e:
#             print(str(e))
#         print('Socket is listening..')
#         self.ServerSideSocket.listen(4)
#         for i in range(self.board_size):
#             self.board.append([])
#             for j in range(self.board_size):
#                 self.board[i].append(0)
#         random.shuffle(self.color_list)
#         Client_list = []
#         while self.ThreadCount < 4:
#             Client, address = self.ServerSideSocket.accept()
#             Client_list.append(Client)
#             start_new_thread(self.gamestart, (Client_list[self.ThreadCount], self.color_list[self.ThreadCount], self.ThreadCount))
#             self.ThreadCount += 1    

#     def send_color(self, connection, color):
#         connection.send(str.encode(color))
        
#     def gamestart(self, connection, color, id):
#         # connection.send(str.encode('Server is working:'))
#         # print(connection)
#         self.send_color(connection, color)
#         while not self.Finish:
#             if id == self.nowPlayer:
#                 # ask player to play
#                 # newposition = get the position the player played
#                 connection.send(str.encode("your_turn"))
#                 try:
#                     newPosition = connection.recv(1024).decode("utf-8")
#                     self.newPositionX = int(newPosition[0])
#                     self.newPositionY = int(newPosition[1])
#                     newcolor = color
#                 except:
#                     continue
#             else:
#                 connection.send(str.encode("not_your_turn"))
#                 while self.newPositionX == -1 and self.newPositionY == -1:
#                     continue
#                 while self.board[self.newPositionX][self.newPositionY]:
#                     continue
#                 connection.send(str.encode([str(self.newPositionX), str(self.newPositionY), newcolor]))
#         if id == self.Winner:
#             connection.send(str.encode("you_win"))
#         else:
#             connection.send(str.encode("you_lose"))
#         time.sleep(10)
#         connection.close()

#     def close(self):
#         self.ServerSideSocket.close()

# Initialize clients
class Client:
    def __init__(self):
        self.ClientMultiSocket = socket.socket()
        self.host = '127.0.0.1'
        self.port = 2004
        print('Waiting for connection response')
        try:
            self.ClientMultiSocket.connect((self.host, self.port))
            print("Client connected successfully!")
        except socket.error as e:
            print(str(e))
        self.playerID = self.ClientMultiSocket.recv(1024).decode("utf-8")
        self.color = self.ClientMultiSocket.recv(1024).decode("utf-8")
        self.newPositionX = 0
        self.newPositionY = 0
        self.actualPositionX = 0
        self.actualPositionY = 0
        self.newColor = ""
        self.getPosition = False
        self.someoneWin = False
    
    def currentPlayerProcess(self, game, screen):
        try:
            pos = pygame.mouse.get_pos()
            displaySuccess, coord, displayedPos = game.displayChess(screen, [pos[1], pos[0]], pygame.Color(self.color))
            self.getPosition = displaySuccess
            self.newPositionX, self.newPositionY = coord[0], coord[1]
            self.actualPositionX, self.actualPositionY = displayedPos[0], displayedPos[1]
            self.ClientMultiSocket.send(str.encode(f"{str(self.newPositionX)},{str(self.newPositionY)},{str(self.actualPositionX)},{str(self.actualPositionY)}")) # we need to get newposition from JC
        except Exception as e:
            print(e)
            pass
        
    def otherPlayerProcess(self, game, screen):
        try:
            # Display the other 3 players' status
            step = self.ClientMultiSocket.recv(1024).decode("utf-8")
            print(step)
            pos, self.newColor = [int(step.split(",")[0]), int(step.split(",")[1])], step.split(",")[2]
            print(pos, self.newColor)
            print(pygame.Color(self.newColor))
            displaySuccess, _, _ = game.displayChess(screen, [pos[1], pos[0]], pygame.Color(self.newColor))
            print(displaySuccess)
        except Exception as e:
            print(e)
            pass
        
    def close(self):
        self.ClientMultiSocket.close()


def main():
    client = Client()
    game = Board(client.playerID)
    resolution = (620, 620)
    screen = game.initGame(resolution)
    while not client.someoneWin:
        message = client.ClientMultiSocket.recv(1024).decode("utf-8")
        print(f"This is player {client.playerID}, message: {message}")
        client.getPosition = False
        while len(message) != 0:
            if message == "your_turn":
                placed = False
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            print("Chess placed")
                            client.currentPlayerProcess(game, screen)
                            print(f"Get position: {client.getPosition}")
                            placed = True
                            break   
                if placed:
                    break
            elif message == "not_your_turn":
                print(f"placing current player's chess!")
                client.otherPlayerProcess(game, screen)
                print("Placing done!")
                break
            elif message == "you_win":
                # render win in this line
                youWin = pygame.font.SysFont(None, 60)
                renderedYouWin = youWin.render("Gobang", True, (0, 0, 0))
                screen.blit(renderedYouWin,(10, 10))
                client.someoneWin = True

            elif message == "you_lose":
                # render lose in this line
                youLose = pygame.font.SysFont(None, 60)
                renderedYouLose = youLose.render("Gobang", True, (0, 0, 0))
                screen.blit(renderedYouLose,(10, 10))
                client.someoneWin = True
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
    client.close()
main()