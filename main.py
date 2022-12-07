import pygame,sys
from pygame.locals import QUIT
from gobang import Board

game = Board()
resolution = (620,620)
screen = game.initGame(resolution)
pos = (100,100)
botPos = (100,100)
black = (0,0,0)
white = (255,255,255)

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            game.displayChess(screen, pos, black)
            if game.endGame() == "Black wins":
                pygame.quit()
                sys.exit()
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()