import numpy as np
import random as rd
import math
import pygame

class Chess:
    def __init__(self, gameScreen, color, centerCoord):
        self.gameScreen = gameScreen
        self.color = color
        self.centerCoord = centerCoord
        self.radius = 10

class Player:
    def __init__(self):
        pass

class StartPage:
    def __init__(self):
        pass

class Board:
    # Initialize the court
    def __init__(self):
        pygame.init()
        self.court = np.zeros((15,15), dtype=object)
        self.len = 15
        self.width = 15
        self.backgroundColor = "#cdcfd0"

    def initGame(self, resolution): # Create a blank game interface
        # Create screen
        gameScreen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Gobang")
        gameScreen.fill(self.backgroundColor)

        # Create title
        title = pygame.font.SysFont(None, 60)
        renderedTitle = title.render("Gobang",True,(0, 0, 0))
        gameScreen.blit(renderedTitle,(10, 10))

        # Create rows and columns
        for i in range(0, 15):
            pygame.draw.rect(gameScreen, (0, 0, 0, 0.5), pygame.Rect(100+30*i, 100, 2, 422))
            pygame.draw.rect(gameScreen, (0, 0, 0, 0.5), pygame.Rect(100, 100+30*i, 422, 2))
        pygame.display.update()
        return gameScreen
    
    def displayChess(self, gameScreen, pos, color):
        # Adjust location if you put the chess outside the board
        if pos[0] >= 85 and pos [0] < 535 and pos[1] >= 85 and pos[1] < 535:
            posList = [pos[0], pos[1]]
            coord, displayedPosList = self.posAdjustment(posList)
            displayedPos = (displayedPosList[0], displayedPosList[1])

            # Display chess
            # Coord argument is a tuple of (x, y)
            newChess = Chess(gameScreen, color, displayedPos)
            # print(newChess.centerCoord)
            pygame.draw.circle(newChess.gameScreen, newChess.color, newChess.centerCoord, newChess.radius)
            if color == (0, 0, 0):
                self.court[coord[1]][coord[0]] = 1
            else:
                self.court[coord[1]][coord[0]] = 0
            pygame.display.update()
    
    # To avoid location mistake
    def posAdjustment(self, pos):
        # Coord is what program sees
        # Pos is what we sees
        coord = [-1, -1]
        for i in range(0, 15):
            if pos[0] >= 100 + (30*i) - 15 and pos[0] < 100 + (30*i) +15:
                pos[0] = 100 + (30*i)
                coord[0] = i
            if pos[1] >= 100 + (30*i) -15 and pos[1] < 100 + (30*i) +15:
                pos[1] = 100 + (30*i)
                coord[1] = i
        return coord, pos
    
    def endGame(self):
        # Pass board information to server and retrieve who wins and who loses
        for i in range(self.len):
            for j in range(self.width):
                try:
                    if self.court[i][j] == 1 and self.court[i+1][j] == 1 and self.court[i+2][j] == 1 and self.court[i+3][j] == 1:
                        print("vertical")
                        return True
                except:
                    pass
                try:
                    if self.court[i][j] == 1 and self.court[i][j+1] == 1 and self.court[i][j+2] == 1 and self.court[i][j+3] == 1:
                        print("horizontal")
                        return True
                except:
                    pass
                try:
                    if self.court[i][j] == 1 and self.court[i+1][j+1] == 1 and self.court[i+2][j+2] == 1 and self.court[i+3][j+3] == 1:
                        print("slant right")
                        return True
                except:
                    pass
                try:
                    if self.court[i][j] == 1 and self.court[i+1][j-1] == 1 and self.court[i+2][j-2] == 1 and self.court[i+3][j-3] == 1:
                        print("slant left")
                        return True
                except:
                    pass
        return False
    
class ResultPage:
    def __init__(self):
        pass