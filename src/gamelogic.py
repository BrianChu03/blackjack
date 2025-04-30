import pygame
import sys
import guiconstants as c
from gui import GUI

class GameState:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption("My Pygame Menu")
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.game_state = 'menu'

        # Create the GUI, passing the screen and this game instance
        self.gui = GUI(self.screen, self)
        self.gui.create_menu_buttons() # Create buttons upon initialization



    def start_game(self):
        """Action for the 'Start Game' button."""
        print("Start Game button pressed!")
        self.game_state = 'playing'
        print(f"Game state changed to: {self.game_state}")
        self.gui.buttons = []


    def instructions(self):
        """Action for the 'Instructions' button."""
        print("Instructions button pressed!")
        self.game_state = 'instructions'
        print(f"Game state changed to: {self.game_state}")
        self.gui.buttons = []


    def exit_game(self):
        """Action for the 'Exit' button."""
        print("Exit button pressed!")
        self.is_running = False