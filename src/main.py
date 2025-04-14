import pygame, sys
from pygame.locals import *
import constants as c

pygame.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()

#### ---- Main Game Loop ---- ####
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # gui.py handles other inputs

    # Game reset
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

pygame.quit()
