import pygame,sys
from pygame.locals import QUIT
from gobang import Board
import socket
from _thread import *
import time
import random


def main():
    game = Board()
    resolution = (620, 620)
    screen = game.initGame(resolution)
    pos = (100, 100)
    botPos = (100, 100)
    black = (0, 0, 0)
    white = (255, 255, 255)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Use "your turn", "not your turn" to determine current player
                    pos = pygame.mouse.get_pos()
                    game.displayChess(screen, [pos[1], pos[0]], black)        
                    if game.endGame():
                        pygame.quit()
                        sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
main()