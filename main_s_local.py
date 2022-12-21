import pygame,sys
from pygame.locals import QUIT
from gobang import Admin, Chess
import socket
from _thread import *
import time
import random

# Initialize a server
class Server:
    def __init__(self, admin, screen, playerCnt, color_list):
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
        self.color_list = color_list
        self.totalPlayerCnt = playerCnt
        self.game = admin
        self.screen = screen
        self.chessPlaced = False
        self.begin = 0
        self.beginwait = 0

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
        Client_list = []
        while self.ThreadCount < self.totalPlayerCnt:
            Client, address = self.ServerSideSocket.accept()
            Client_list.append(Client)
            self.ThreadCount += 1
            print(self.ThreadCount)
        for t, client in enumerate(Client_list):
            start_new_thread(self.gamestart, (client, self.color_list[t], t))
            time.sleep(3)


    def gamestart(self, connection, color, id):
        # connection.send(str.encode('Server is working:'))
        # print(connection)
        connection.send(str.encode(str(id+1)))
        connection.send(str.encode(color))

        while not self.Finish:
            if self.begin < self.totalPlayerCnt:
                time.sleep(3)
                self.begin += 1
            #time.sleep(2)
            if id == self.nowPlayer:
                print(f"Thread{id}. It's player {id+1}'s turn!")
                self.game.drawPlayerStatus(self.screen, self.nowPlayer)
                # ask player to play
                # newposition = get the position the player played

                while self.beginwait < self.totalPlayerCnt - 1:
                    continue
                connection.send(str.encode("your_turn"))

                try:
                    newPosition = connection.recv(1024).decode("utf-8")
                    self.newPositionX, self.newPositionY = int(newPosition.split(",")[0]), int(newPosition.split(",")[1])
                    self.actualPositionX, self.actualPositionY = int(newPosition.split(",")[2]), int(newPosition.split(",")[3])
                    self.newcolor = color

                    self.board[self.newPositionX][self.newPositionY] = 1
                    self.game.board[self.newPositionX][self.newPositionY] = self.newcolor
                    newChess = Chess(self.screen, color, (self.actualPositionX, self.actualPositionY))
                    pygame.draw.circle(newChess.gameScreen, newChess.color, newChess.centerCoord, newChess.radius)
                    pygame.display.update()
                    if self.game.endGame():
                        print(f"Player {id} wins!")
                        time.sleep(3)
                        self.Winner = id
                        self.Finish = True
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
                self.beginwait += 1

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
            time.sleep(2)
            print("you win!")
            connection.send(str.encode("you_win"))
            self.game.drawWhoWins(self.screen, self.Winner+1)
        else:
            time.sleep(2)
            print("you lose!")
            connection.send(str.encode("you_lose"))

def main():
    playerCnt = 4
    color_list = [
        "#85332d", "#ff7b24", "#ff201c", "#f0ec1f", "#63cc43", "#357bb8", "#35b8ab", "#9530c7", "#cf19b6", "#cf1958"
    ]
    random.shuffle(color_list)
    admin = Admin(playerCnt, color_list)
    resolution = (620, 620)
    screen = admin.initGame(resolution)
    server = Server(admin, screen, playerCnt, color_list)
    server.initGame()
    while not server.Finish:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        continue
main()