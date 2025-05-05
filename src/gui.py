import pygame
from pygame.locals import *
import guiconstants as c

class Button:
    def __init__(self, x, y, width, height, text, action=None, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont(None, font_size)

    def draw(self, screen):
        # Draw button rectange on screen using default color
        pygame.draw.rect(screen, c.DARK_GREEN, self.rect)

        # Render text and center it on the button
        text_surf = self.font.render(self.text, True, c.WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        # Check if the button was clicked
        return self.rect.collidepoint(pos)

class GUI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 36)
        self.buttons = []
    
    def create_menu_buttons(self):
        start_x = (c.SCREEN_WIDTH - c.MUTTON_WIDTH) // 2
        start_y = (c.SCREEN_HEIGHT - c.MUTTON_HEIGHT) // 2
        
        # Create three options for start menu
        start_button = Button(start_x, start_y, c.MUTTON_WIDTH, c.MUTTON_HEIGHT,
                              "Start Game", self.game_settings)
        instruct_button = Button(start_x, start_y + c.MUTTON_HEIGHT + c. MUTTON_PADDING,
                                c.MUTTON_WIDTH, c.MUTTON_HEIGHT, "Instructions",
                                self.instructions)
        exit_button = Button(start_x, start_y + 2 * (c.MUTTON_HEIGHT + c.MUTTON_PADDING),
                                c.MUTTON_WIDTH, c.MUTTON_HEIGHT, "Exit", self.exit_game)
        
        # Add buttons to list so they can be rendered
        self.buttons.extend([start_button, instruct_button, exit_button])

    
    def render(self):
        self.screen.fill(c.GREEN)

        self.create_menu_buttons()

        # Draw menu buttons first
        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.is_clicked(pos):
                    if button.action:
                        button.action()

    def game_settings(self):
        print("Game Settings button pressed!")

        
    def instructions(self):
        print("Instructions button pressed!")

    def exit_game(self):
        print("Exit button pressed!")
        pygame.quit()
        exit()


    