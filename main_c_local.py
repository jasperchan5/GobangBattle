import pygame,sys
from pygame.locals import QUIT
from gobang import Board, Chess
import socket
from _thread import *
import time
import random

# Initialize a client
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
            print(self.getPosition)
            if self.getPosition:
                self.newPositionX, self.newPositionY = coord[0], coord[1]
                self.actualPositionX, self.actualPositionY = displayedPos[0], displayedPos[1]
                self.ClientMultiSocket.send(str.encode(f"{str(self.newPositionX)},{str(self.newPositionY)},{str(self.actualPositionX)},{str(self.actualPositionY)}")) # we need to get newposition from JC
        except Exception as e:
            print(e)
            pass

    def otherPlayerProcess(self, game, screen):
        try:
            # Display the other 3 players' status
            print(f"placing current player's chess!")
            step = self.ClientMultiSocket.recv(1024).decode("utf-8")
            print(step)
            pos, self.newColor = [int(step.split(",")[0]), int(step.split(",")[1])], step.split(",")[2]
            displaySuccess, _, _ = game.displayChess(screen, [pos[1], pos[0]], pygame.Color(self.newColor))
            print("Display result:", displaySuccess)
            return displaySuccess
        except Exception as e:
            print(e)
            pass

    def close(self):
        self.ClientMultiSocket.close()


def main():
    client = Client()
    game = Board(client.playerID, client.color)
    resolution = (620, 620)
    screen = game.initGame(resolution)
    while not client.someoneWin:
        message = client.ClientMultiSocket.recv(1024).decode("utf-8")
        print(f"This is player {client.playerID}, message: {message}")
        client.getPosition = False
        while len(message) != 0:
            if message == "your_turn":
                game.nowPlayerGlow(screen)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            print("Chess placed")
                            client.currentPlayerProcess(game, screen)
                            print(f"Get position: {client.getPosition}")
                            if client.getPosition:
                                message = ""
                                break
                            else:
                                continue
            elif message == "not_your_turn":
                game.otherPlayerNoGlow(screen)
                displaySuccess = client.otherPlayerProcess(game, screen)
                print("Placing done!")
                if displaySuccess:
                    print("Other player placing success")
                    message = ""
                    break
                else:
                    print("Other player placing not success")
                    continue

            elif message == "you_win":
                # render win in this line
                game.drawYouWin(screen)
                client.someoneWin = True
                break

            elif message == "you_lose":
                # render lose in this line
                game.drawYouLose(screen)
                client.someoneWin = True
                break

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