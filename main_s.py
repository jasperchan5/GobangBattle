import pygame,sys
from pygame.locals import QUIT
from gobang import Admin, Chess
import socket
from _thread import *
import time
import random
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Initialize a server
class Server:
    def __init__(self, admin, screen):
        self.ServerSideSocket = socket.socket()
        self.host = '54.174.225.113'
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
        self.totalPlayerCnt = 2
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
                        self.Finish = True
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
                print(f"Thread{id} A:", self.newPositionX, self.newPositionX)
                while self.newPositionX == -1 and self.newPositionY == -1:
                    continue
                print(f"Thread{id} B:", self.newPositionX, self.newPositionX)
                # while self.board[self.newPositionX][self.newPositionY] == 0:
                #     continue
                time.sleep(1)
                print("Send position!")
                connection.send(str.encode(f"{str(self.actualPositionX)},{str(self.actualPositionY)},{self.newcolor}"))
                time.sleep(3)
        if id == self.Winner:
            print("you win!")
            connection.send(str.encode("you_win"))
        else:
            print("you lose!")
            connection.send(str.encode("you_lose"))
        time.sleep(10)
        connection.close()

    def close(self):
        self.ServerSideSocket.close()

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