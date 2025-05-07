import pygame
from pygame.locals import *
import guiconstants as c

class Button:
    def __init__(self, x, y, width, height, text, action=None, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont(None, font_size)
        self.is_hovered = False

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
    
    def update_hover(self, pos):
        # Check if the mouse is hovering over the button
        if self.rect.collidepoint(pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

class GUI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        self.buttons = []

        self.current_screen = 'menu' # default screen

        # player and chip settings
        self.num_players = 1
        self.num_chips = 1000

        # Start menu buttons
        start_x = (c.SCREEN_WIDTH - c.MUTTON_WIDTH) // 2
        start_y = (c.SCREEN_HEIGHT - c.MUTTON_HEIGHT) // 2
        
        # Create three options for start menu
        self.start_button = Button(start_x, start_y, c.MUTTON_WIDTH, c.MUTTON_HEIGHT,
                              "Start Game", self.show_game_settings)
        self.instruct_button = Button(start_x, start_y + c.MUTTON_HEIGHT + c. MUTTON_PADDING,
                                c.MUTTON_WIDTH, c.MUTTON_HEIGHT, "Instructions",
                                self.show_instructions)
        self.exit_button = Button(start_x, start_y + 2 * (c.MUTTON_HEIGHT + c.MUTTON_PADDING),
                                c.MUTTON_WIDTH, c.MUTTON_HEIGHT, "Exit", self.exit_game)
        
        # create the back button to return to menu
        back_button_x = (c.SCREEN_WIDTH - c.MUTTON_WIDTH) // 2
        back_button_y = (c.SCREEN_HEIGHT - c.MUTTON_HEIGHT) - 50
        self.back_button = Button(back_button_x, back_button_y, c.MUTTON_WIDTH, c.MUTTON_HEIGHT, "Back",
                             self.setup_menu_screen)
        
        # Proceed to game button
        self.proceed_to_game_button = Button(back_button_x, back_button_y, c.MUTTON_WIDTH, c.MUTTON_HEIGHT, "Proceed to Game",
                                            self.game.start_round)
        
        self.player_minus_button = Button(0, 0, c.GS_ADJUST_BUTTON_SIZE, c.GS_ADJUST_BUTTON_SIZE, "-",
                                            self.decrease_players, font_size=c.FONT_SIZE_ADJUST_BUTTON_INTERNAL)
        self.player_plus_button = Button(0, 0, c.GS_ADJUST_BUTTON_SIZE, c.GS_ADJUST_BUTTON_SIZE, "+",
                                            self.increase_players, font_size=c.FONT_SIZE_ADJUST_BUTTON_INTERNAL)
        
        self.chips_minus_button = Button(0, 0, c.GS_ADJUST_BUTTON_SIZE, c.GS_ADJUST_BUTTON_SIZE, "-",
                                            self.decrease_chips, font_size=c.FONT_SIZE_ADJUST_BUTTON_INTERNAL)
        self.chips_plus_button = Button(0, 0, c.GS_ADJUST_BUTTON_SIZE, c.GS_ADJUST_BUTTON_SIZE, "+",
                                            self.increase_chips, font_size=c.FONT_SIZE_ADJUST_BUTTON_INTERNAL)
        
        self.gs_title_center_y = 0
        self.gs_player_row_center_y = 0
        self.gs_chips_row_center_y = 0
        
        self.setup_menu_screen()
    
    def setup_menu_screen(self):
        self.current_screen = 'menu'
        self.buttons.clear()
        self.buttons.extend([self.start_button, self.instruct_button, self.exit_button])

    def increase_players(self):
        if self.num_players < 6:
            self.num_players += 1
            print(f"Number of players: {self.num_players}")
        else:
            print("Maximum number of players reached!")

    def decrease_players(self):
        if self.num_players > 1:
            self.num_players -= 1
            print(f"Number of players: {self.num_players}")
        else:
            print("Minimum number of players reached!")

    def increase_chips(self):
        if self.num_chips < 9900:
            self.num_chips += 100
            print(f"Number of chips: {self.num_chips}")
        else:
            print("Maximum number of chips reached!")

    def decrease_chips(self):
        if self.num_chips > 100:
            self.num_chips -= 100
            print(f"Number of chips: {self.num_chips}")
        elif self.num_chips > 0:
            self.starting_chips = max(0, self.num_chips - 10)
            print(f"Number of chips: {self.num_chips}")

    def show_game_settings(self):
        print("Game Settings button pressed!")
        self.current_screen = "game_settings"
        self.buttons.clear()

        scaled_font_title_height = self.font.get_linesize()
        scaled_row_element_height = c.GS_ADJUST_BUTTON_SIZE

        # total height of settings block for centering
        total_block_height = (scaled_font_title_height +
                              c.GS_SPACING_TITLE_TO_FIRST_ROW +
                              scaled_row_element_height +
                              (c.GS_SPACING_ROW_TO_ROW_CENTER - scaled_row_element_height) +
                              scaled_row_element_height)
        
        block_top_y = (c.SCREEN_HEIGHT - total_block_height) // 2

        self.gs_title_center_y = block_top_y + scaled_font_title_height // 2
        self.gs_player_row_center_y = (self.gs_title_center_y + scaled_font_title_height // 2 +
                                       c.GS_SPACING_TITLE_TO_FIRST_ROW + scaled_row_element_height // 2)
        self.gs_chips_row_center_y = self.gs_player_row_center_y + c.GS_SPACING_ROW_TO_ROW_CENTER

        value_block_center_x = c.SCREEN_WIDTH // 2 + c.GS_VALUE_BLOCK_CENTER_X_OFFSET

        base_y_player = 200
        self.player_minus_button.rect.center = (value_block_center_x - c.GS_ADJUST_BTN_OFFSET_FROM_VALUE, self.gs_player_row_center_y)
        self.player_plus_button.rect.center = (value_block_center_x + c.GS_ADJUST_BTN_OFFSET_FROM_VALUE, self.gs_player_row_center_y)

        base_y_chips = 200 + 100
        self.chips_minus_button.rect.center = (value_block_center_x - c.GS_ADJUST_BTN_OFFSET_FROM_VALUE, self.gs_chips_row_center_y)
        self.chips_plus_button.rect.center = (value_block_center_x + c.GS_ADJUST_BTN_OFFSET_FROM_VALUE, self.gs_chips_row_center_y)

        self.buttons.extend([self.player_minus_button, self.player_plus_button,
                                self.chips_minus_button, self.chips_plus_button,
                                self.proceed_to_game_button])

        
    def show_instructions(self):
        print("Instructions button pressed!")
        self.current_screen = "instructions"
        self.buttons.clear()

        self.buttons.append(self.back_button)
        


    def exit_game(self):
        print("Exit button pressed!")
        pygame.quit()
        exit()

    # This is where the magic happens
    # The render method is called every frame to update the display
    # It draws the current screen and all buttons
    def render(self):
        self.screen.fill(c.GREEN)

        if self.current_screen == 'menu':
            menu_title_font = pygame.font.SysFont(None, c.FONT_SIZE_TITLE_MAIN_MENU)
            title_text = menu_title_font.render("Blackjack", True, c.WHITE)
            title_rect = title_text.get_rect(center=(c.SCREEN_WIDTH // 2, c.MENU_TITLE_Y_POS))
            self.screen.blit(title_text, title_rect)
        elif self.current_screen == 'instructions':
            instruction_font = pygame.font.SysFont(None, c.FONT_SIZE_TITLE_SCREENS)
            title_surf = instruction_font.render("Instructions", True, c.WHITE)
            title_rect = title_surf.get_rect(center=(c.SCREEN_WIDTH // 2, c.INSTRUCTIONS_TITLE_Y_POS))
            self.screen.blit(title_surf, title_rect)

            # FIXME: ALIGN INSTRUCTIONS TEXT
            # Create instructions text
            instructions_text = [
                "How to Play:",
                "1. The goal is to get as close to 21 as possible without going over.",
                "2. Each player is dealt two cards, and the dealer has one card face up and one face down.",
                "3. Players can choose to 'hit' (take another card) or 'stand' (keep their current hand).",
                "3,5. If the first two cards are the same rank, the player can choose to split them into two separate hands.",
                "4. If the player goes over 21, they lose."
            ]
            instruction_text_font = pygame.font.SysFont(None, c.FONT_SIZE_INSTRUCTION_LINES)
            for i, line in enumerate(instructions_text):
                text_surf = instruction_text_font.render(line, True, c.WHITE)
                text_rect = text_surf.get_rect(center=(c.SCREEN_WIDTH // 2, c.INSTRUCTIONS_TEXT_Y_START + i * c.INSTRUCTIONS_TEXT_LINE_SPACING))
                self.screen.blit(text_surf, text_rect)
        elif self.current_screen == 'game_settings':
            game_setting_font = pygame.font.SysFont(None, c.FONT_SIZE_TITLE_SCREENS)
            title_surf = game_setting_font.render("Game Settings", True, c.WHITE)
            title_rect = title_surf.get_rect(center=(c.SCREEN_WIDTH // 2, 100))
            self.screen.blit(title_surf, title_rect)

            base_y = 200
            setting_spacing = 100
            label_x_offset = -80 # buttons cover labels, move them right
            value_block_x_offset = 60 # buttons cover labels, move them right

            # Show number of players
            player_font = pygame.font.SysFont(None, c.FONT_SIZE_PLAYER_LABELS_VALUES)
            chip_font = pygame.font.SysFont(None, c.FONT_SIZE_CHIPS_LABELS_VALUES)
            players_text_surf = player_font.render("Number of Players:", True, c.WHITE)
            players_text_rect = players_text_surf.get_rect(center=(c.SCREEN_WIDTH // 2 + c.GS_LABEL_CENTER_X_OFFSET, self.gs_player_row_center_y))
            self.screen.blit(players_text_surf, players_text_rect)

            # Animate number of players
            players_val_surf = player_font.render(str(self.num_players), True, c.WHITE)
            players_val_rect = players_val_surf.get_rect(center=(c.SCREEN_WIDTH // 2 + c.GS_VALUE_BLOCK_CENTER_X_OFFSET, self.gs_player_row_center_y))
            self.screen.blit(players_val_surf, players_val_rect)

            # Show number of chips
            chips_text_surf = chip_font.render("Number of Chips:", True, c.WHITE)
            chips_text_rect = chips_text_surf.get_rect(center=(c.SCREEN_WIDTH // 2 + c.GS_LABEL_CENTER_X_OFFSET, self.gs_chips_row_center_y))
            self.screen.blit(chips_text_surf, chips_text_rect)

            chips_val_surf = chip_font.render(str(self.num_chips), True, c.WHITE)
            chips_val_rect = chips_val_surf.get_rect(center=(c.SCREEN_WIDTH // 2  + c.GS_VALUE_BLOCK_CENTER_X_OFFSET, self.gs_chips_row_center_y))
            self.screen.blit(chips_val_surf, chips_val_rect)
        elif self.current_screen == 'game_placeholder':
            title_surf = self.font.render("Game Screen Placeholder", True, c.WHITE)
            title_rect = title_surf.get_rect(center=(c.SCREEN_WIDTH // 2, c.INSTRUCTIONS_TITLE_Y_POS))
            self.screen.blit(title_surf, title_rect)

            # Placeholder for game screen
            game_placeholder_text = self.font.render("Game Screen Placeholder", True, c.WHITE)
            game_placeholder_rect = game_placeholder_text.get_rect(center=(c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 2))
            self.screen.blit(game_placeholder_text, game_placeholder_rect)


        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == MOUSEMOTION:
            for button in self.buttons:
                button.update_hover(mouse_pos)

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for button in self.buttons:
                    if button.is_clicked(mouse_pos):
                        if button.action:
                            button.action()
                        if self.current_screen == 'menu':
                            for b in self.buttons:
                                b.update_hover(mouse_pos)
                        elif self.current_screen == 'instructions':
                            self.back_button.update_hover(mouse_pos)
                        break




    