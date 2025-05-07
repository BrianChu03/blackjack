import pygame, sys
from pygame.locals import *
import gui as ui
import gamelogic as game
import guiconstants as c

pygame.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()

# Game object that persists the entire game session
game_state = game.BlackjackGame()
# Instance of the GUI that handles the display and user input
gui_display = ui.GUI(screen, game_state)

#### ---- Main Game Loop ---- ####
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # gui.py handles other inputs
        gui_display.handle_event(event)

    gui_display.render()

    # Game reset
    # pygame.display.flip() # flip is called in the render method of GUI, KEEP THIS HERE FOR NOW
    clock.tick(60)  # Limit to 60 frames per second

pygame.quit()
