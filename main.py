import pygame,sys
from pygame.locals import QUIT
from gobang import Board, StartPage

game = Board()
resolution = (620, 620)
screen = game.initGame(resolution)
pos = (100, 100)
botPos = (100, 100)
colors = ["#000000", "#000080", "#008000", "#ff0000",  "#800080", "#00ff00", "#00ffff"]
black = (0, 0, 0)
white = (255, 255, 255)

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Use "your turn", "not your turn" to determine current player
            pos = pygame.mouse.get_pos()
            game.displayChess(screen, pos, black)
            if game.endGame():
                # pygame.quit()
                # sys.exit()
                game = Board()
                game.initGame(resolution)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()