import numpy as np
import random as rd
import time
import pygame

class Chess:
    def __init__(self, gameScreen, color, centerCoord):
        self.gameScreen = gameScreen
        self.color = color
        self.centerCoord = centerCoord
        self.radius = 10

class Admin:
    # Initialize the board
    def __init__(self, playerCnt, colorList):
        pygame.init()
        self.board = np.zeros((15,15), dtype=object)
        self.len = 15
        self.width = 15
        self.backgroundColor = "#cdcfd0"
        self.colorList = colorList
        self.playerCnt = playerCnt

    def initGame(self, resolution): # Create a blank game interface
        # Create screen
        gameScreen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Admin")
        gameScreen.fill(self.backgroundColor)

        # Create title
        self.drawPlayerStatus(gameScreen, 0)
        self.drawBoard(gameScreen)
        return gameScreen
    
    def drawPlayerStatus(self,  gameScreen, nowPlayerID):
        for e, i in enumerate(range(0, 140*(self.playerCnt-1)+1, 140)):
            if e == nowPlayerID:
                self.nowPlayerGlow(gameScreen, self.colorList[e], e+1, i)
            else:
                self.otherPlayerNoGlow(gameScreen, self.colorList[e], e+1, i)
        pygame.display.update()
        
    def nowPlayerGlow(self, gameScreen, thisPlayerColor, thisPlayerID, offset):
        colorWidth, colorHeight = 128, 36
        tagWidth, tagHeight = 82, 26
        colorRenderX, colorRenderY = 32+offset, 24
        tagRenderX, tagRenderY = colorRenderX+23, colorRenderY+5
        tagRenderXCenter, tagRenderYCenter = tagRenderX+0.5*tagWidth, tagRenderY+0.5*tagHeight
        pygame.draw.rect(gameScreen, thisPlayerColor, (colorRenderX, colorRenderY, colorWidth, colorHeight))
        pygame.draw.rect(gameScreen, (0, 0, 0), (tagRenderX, tagRenderY, tagWidth, tagHeight))
        title = pygame.font.Font(None, 24)
        renderedTitle = title.render(f"Player {thisPlayerID}", True, (255, 255, 255), pygame.SRCALPHA)
        text_rect = renderedTitle.get_rect(center=(tagRenderXCenter, tagRenderYCenter))
        gameScreen.blit(renderedTitle, text_rect)
        pygame.display.update()
    
    def otherPlayerNoGlow(self, gameScreen, thisPlayerColor, thisPlayerID, offset):
        colorWidth, colorHeight = 12, 36
        tagWidth, tagHeight = 116, 36
        colorRenderX, colorRenderY = 32+offset, 24
        tagRenderX, tagRenderY = colorRenderX+colorWidth, colorRenderY
        tagRenderXCenter, tagRenderYCenter = tagRenderX+0.5*tagWidth, tagRenderY+0.5*tagHeight
        pygame.draw.rect(gameScreen, thisPlayerColor, (colorRenderX, colorRenderY, colorWidth, colorHeight))
        pygame.draw.rect(gameScreen, (0, 0, 0), (tagRenderX, tagRenderY, tagWidth, tagHeight))
        title = pygame.font.Font(None, 24)
        renderedTitle = title.render(f"Player {thisPlayerID}", True, (255, 255, 255), pygame.SRCALPHA)
        text_rect = renderedTitle.get_rect(center=(tagRenderXCenter, tagRenderYCenter))
        gameScreen.blit(renderedTitle, text_rect)
        pygame.display.update()


    def drawBoard(self, gameScreen):
        # Create rows and columns
        for i in range(0, 15):
            pygame.draw.rect(gameScreen, (0, 0, 0, 0.5), pygame.Rect(100+30*i, 100, 2, 422))
            pygame.draw.rect(gameScreen, (0, 0, 0, 0.5), pygame.Rect(100, 100+30*i, 422, 2))
        pygame.display.update()
    
    def drawWhoWins(self, gameScreen, winner):
        backgroundRenderX, backgroundRenderY = 0, 274
        backgroundWidth, backgroundHeight = 620, 72
        pygame.draw.rect(gameScreen, (0, 0, 0, 0.5), (backgroundRenderX, backgroundRenderY, backgroundWidth, backgroundHeight))
        pygame.display.update()
        backgroundRenderXCenter, backgroundRenderYCenter = backgroundRenderX+0.5*backgroundWidth, backgroundRenderY+0.5*backgroundHeight
        youWin = pygame.font.Font(None, 60)
        renderedYouWin = youWin.render(f"Player {winner} wins!", True, (255, 255, 255), pygame.SRCALPHA)
        text_rect = renderedYouWin.get_rect(center=(backgroundRenderXCenter, backgroundRenderYCenter))
        gameScreen.blit(renderedYouWin, text_rect)
        pygame.display.update()
    
    def displayChess(self, gameScreen, pos, color):
        # Adjust location if you put the chess outside the board
        if pos[0] >= 85 and pos [0] < 535 and pos[1] >= 85 and pos[1] < 535:
            posList = [pos[0], pos[1]]
            coord, displayedPosList = self.posAdjustment(posList)
            displayedPos = (displayedPosList[1], displayedPosList[0])

            # Display chess
            # Coord argument is a tuple of (x, y)
            # print(newChess.centerCoord)
            if self.board[coord[0]][coord[1]] == 0:
                self.board[coord[0]][coord[1]] = 1
                newChess = Chess(gameScreen, color, displayedPos)
                pygame.draw.circle(newChess.gameScreen, newChess.color, newChess.centerCoord, newChess.radius)
                pygame.display.update()
                return True, coord
            else:
                return False, coord
    
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
        print("Start examinging end game")
        for i in range(self.len):
            for j in range(self.width):
                if self.board[i][j] != 0:
                    try:
                        if self.board[i][j] == self.board[i+1][j] and self.board[i+1][j] == self.board[i+2][j] and self.board[i+2][j] == self.board[i+3][j]:
                            print("vertical")
                            return True
                    except:
                        pass
                    try:
                        if self.board[i][j] == self.board[i][j+1] and self.board[i][j+1] == self.board[i][j+2] and self.board[i][j+2] == self.board[i][j+3]:
                            print("horizontal")
                            return True
                    except:
                        pass
                    try:
                        if self.board[i][j] == self.board[i+1][j+1] and self.board[i+1][j+1] == self.board[i+2][j+2] and self.board[i+2][j+2] == self.board[i+3][j+3]:
                            print("slant right")
                            return True
                    except:
                        pass
                    try:
                        if self.board[i][j] == self.board[i+1][j-1] and self.board[i+1][j-1] == self.board[i+2][j-2] and self.board[i+2][j-2] == self.board[i+3][j-3]:
                            print("slant left")
                            return True
                    except:
                        pass
        print("No one wins")
        return False
class Board:
    # Initialize the board
    def __init__(self, id, color):
        pygame.init()
        self.id = id
        self.board = np.zeros((15,15), dtype=object)
        self.len = 15
        self.width = 15
        self.backgroundColor = "#cdcfd0"
        self.color = color

    def initGame(self, resolution): # Create a blank game interface
        # Create screen
        gameScreen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Gobang")
        gameScreen.fill(self.backgroundColor)
        self.otherPlayerNoGlow(gameScreen)
        self.drawBoard(gameScreen)
        return gameScreen
    
    def drawBoard(self, gameScreen):
        # Create rows and columns
        for i in range(0, 15):
            pygame.draw.rect(gameScreen, (0, 0, 0, 0.5), pygame.Rect(100+30*i, 100, 2, 422))
            pygame.draw.rect(gameScreen, (0, 0, 0, 0.5), pygame.Rect(100, 100+30*i, 422, 2))
        pygame.display.update()

    def nowPlayerGlow(self, gameScreen):
        colorWidth, colorHeight = 128, 36
        tagWidth, tagHeight = 82, 26
        colorRenderX, colorRenderY = 32, 24
        tagRenderX, tagRenderY = colorRenderX+23, colorRenderY+5
        tagRenderXCenter, tagRenderYCenter = tagRenderX+0.5*tagWidth, tagRenderY+0.5*tagHeight
        pygame.draw.rect(gameScreen, self.color, (colorRenderX, colorRenderY, colorWidth, colorHeight))
        pygame.draw.rect(gameScreen, (0, 0, 0), (tagRenderX, tagRenderY, tagWidth, tagHeight))
        title = pygame.font.Font(None, 24)
        renderedTitle = title.render(f"Player {self.id}", True, (255, 255, 255))
        text_rect = renderedTitle.get_rect(center=(tagRenderXCenter, tagRenderYCenter))
        gameScreen.blit(renderedTitle, text_rect)
        pygame.display.update()
    
    def otherPlayerNoGlow(self, gameScreen):
        colorWidth, colorHeight = 12, 36
        tagWidth, tagHeight = 116, 36
        colorRenderX, colorRenderY = 32, 24
        tagRenderX, tagRenderY = colorRenderX+colorWidth, colorRenderY
        tagRenderXCenter, tagRenderYCenter = tagRenderX+0.5*tagWidth, tagRenderY+0.5*tagHeight
        pygame.draw.rect(gameScreen, self.color, (colorRenderX, colorRenderY, colorWidth, colorHeight))
        pygame.draw.rect(gameScreen, (0, 0, 0), (tagRenderX, tagRenderY, tagWidth, tagHeight))
        title = pygame.font.Font(None, 24)
        renderedTitle = title.render(f"Player {self.id}", True, (255, 255, 255))
        text_rect = renderedTitle.get_rect(center=(tagRenderXCenter, tagRenderYCenter))
        gameScreen.blit(renderedTitle, text_rect)
        pygame.display.update()
        
    def drawYouWin(self, gameScreen):
        backgroundRenderX, backgroundRenderY = 0, 274
        backgroundWidth, backgroundHeight = 620, 72
        pygame.draw.rect(gameScreen, (0, 0, 0, 0.5), (backgroundRenderX, backgroundRenderY, backgroundWidth, backgroundHeight))
        pygame.display.update()
        backgroundRenderXCenter, backgroundRenderYCenter = backgroundRenderX+0.5*backgroundWidth, backgroundRenderY+0.5*backgroundHeight
        youWin = pygame.font.Font(None, 60)
        renderedYouWin = youWin.render("You win!", True, (255, 255, 255), pygame.SRCALPHA)
        text_rect = renderedYouWin.get_rect(center=(backgroundRenderXCenter, backgroundRenderYCenter))
        gameScreen.blit(renderedYouWin, text_rect)
        pygame.display.update()
        
    def drawYouLose(self, gameScreen):
        backgroundRenderX, backgroundRenderY = 0, 274
        backgroundWidth, backgroundHeight = 620, 72
        pygame.draw.rect(gameScreen, (0, 0, 0, 0.5), (backgroundRenderX, backgroundRenderY, backgroundWidth, backgroundHeight))
        pygame.display.update()
        backgroundRenderXCenter, backgroundRenderYCenter = backgroundRenderX+0.5*backgroundWidth, backgroundRenderY+0.5*backgroundHeight
        youWin = pygame.font.Font(None, 60)
        renderedYouWin = youWin.render("You lose!", True, (255, 255, 255), pygame.SRCALPHA)
        text_rect = renderedYouWin.get_rect(center=(backgroundRenderXCenter, backgroundRenderYCenter))
        gameScreen.blit(renderedYouWin, text_rect)
        pygame.display.update()
        
    def displayChess(self, gameScreen, pos, color):
        # Adjust location if you put the chess outside the board
        if pos[0] >= 85 and pos [0] < 535 and pos[1] >= 85 and pos[1] < 535:
            posList = [pos[0], pos[1]]
            coord, displayedPosList = self.posAdjustment(posList)
            displayedPos = (displayedPosList[1], displayedPosList[0])

            # Display chess
            # Coord argument is a tuple of (x, y)
            # print(newChess.centerCoord)
            if self.board[coord[0]][coord[1]] == 0:
                self.board[coord[0]][coord[1]] = 1
                newChess = Chess(gameScreen, color, displayedPos)
                pygame.draw.circle(newChess.gameScreen, newChess.color, newChess.centerCoord, newChess.radius)
                pygame.display.update()
                return True, coord, displayedPos
            else:
                return False, coord, displayedPos
    
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