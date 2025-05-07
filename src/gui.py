import pygame
from pygame.locals import *
import guiconstants as c
from gamelogic import GameState

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

        # FONT for HUD
        self.hud_font = pygame.font.SysFont(None, c.HUD_LABEL_FONT_SIZE)
        self.chip_font = pygame.font.SysFont(None, c.HUD_CHIP_FONT_SIZE)

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
                                            self.prepare_game_screen)
        
        self.player_minus_button = Button(0, 0, c.GS_ADJUST_BUTTON_SIZE, c.GS_ADJUST_BUTTON_SIZE, "-",
                                            self.decrease_players, font_size=c.FONT_SIZE_ADJUST_BUTTON_INTERNAL)
        self.player_plus_button = Button(0, 0, c.GS_ADJUST_BUTTON_SIZE, c.GS_ADJUST_BUTTON_SIZE, "+",
                                            self.increase_players, font_size=c.FONT_SIZE_ADJUST_BUTTON_INTERNAL)
        
        self.chips_minus_button = Button(0, 0, c.GS_ADJUST_BUTTON_SIZE, c.GS_ADJUST_BUTTON_SIZE, "-",
                                            self.decrease_chips, font_size=c.FONT_SIZE_ADJUST_BUTTON_INTERNAL)
        self.chips_plus_button = Button(0, 0, c.GS_ADJUST_BUTTON_SIZE, c.GS_ADJUST_BUTTON_SIZE, "+",
                                            self.increase_chips, font_size=c.FONT_SIZE_ADJUST_BUTTON_INTERNAL)
        
        # Dynamic variable y positions for game setting screen
        self.gs_title_center_y = 0
        self.gs_player_row_center_y = 0
        self.gs_chips_row_center_y = 0

        self.current_bet = c.MIN_BET
        # Use try, except statement for image loading and scaling
        try:
            self.chip_image_original = pygame.image.load(c.HUD_CHIP_IMAGE_PATH).convert_alpha()
            self.chip_image = pygame.transform.scale(self.chip_image_original, c.HUD_CHIP_IMAGE_SIZE)
        except pygame.error as e:
            print(f"Error loading chip image: {e}. Using Placeholder")
            self.chip_image = None

        # Bet and deal buttons for game screen
        self.bet_decrease_button = Button(0, 0, c.HUD_BET_BUTTON_SIZE, c.HUD_BET_BUTTON_SIZE, "-", self.decrease_current_bet, font_size=c.HUD_BET_BUTTON_FONT_SIZE)
        self.bet_increase_button = Button(0, 0, c.HUD_BET_BUTTON_SIZE, c.HUD_BET_BUTTON_SIZE, "+", self.increase_current_bet, font_size=c.HUD_BET_BUTTON_FONT_SIZE)
        self.deal_button = Button(0, 0, c.HUD_DEAL_BUTTON_WIDTH, c.HUD_DEAL_BUTTON_HEIGHT, "Deal", self.place_bet_and_deal)

        # Player action buttons (hit, stand, double, split)
        self.hit_button = Button(0, 0, c.ACTION_BUTTON_WIDTH, c.ACTION_BUTTON_HEIGHT, "Hit", self.player_hit, font_size=c.ACTION_BUTTON_FONT_SIZE)
        self.stand_button = Button(0, 0, c.ACTION_BUTTON_WIDTH, c.ACTION_BUTTON_HEIGHT, "Stand", self.player_stand, font_size=c.ACTION_BUTTON_FONT_SIZE)
        self.double_down_button = Button(0, 0, c.ACTION_BUTTON_WIDTH, c.ACTION_BUTTON_HEIGHT, "Double", self.player_double_down, font_size=c.ACTION_BUTTON_FONT_SIZE)
        self.split_button = Button(0, 0, c.ACTION_BUTTON_WIDTH, c.ACTION_BUTTON_HEIGHT, "Split", self.player_split, font_size=c.ACTION_BUTTON_FONT_SIZE)
        
        # Default is menu screen
        self.setup_menu_screen()
    
    ##### Menu Screen Methods #####
    def setup_menu_screen(self):
        self.current_screen = 'menu'
        self.buttons.clear()
        self.buttons.extend([self.start_button, self.instruct_button, self.exit_button])

    ##### Game Settings Methods #####
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
            self.num_chips = max(0, self.num_chips - 10)
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

    ##### Game Screen Methods #####
    def prepare_game_screen(self):
        print("Preparing game screen!")
        self.current_screen = 'game_active'
        self.current_bet = c.MIN_BET
        # We set the chips from the settings in the game object, it will rollover to game screen
        self.game.player.chips = self.num_chips
        print(f"Player starting chips set to: {self.game.player.chips} (from GUI settings: {self.num_chips})")

        self.game.new_round()
        self.update_game_buttons()

    def increase_current_bet(self):
        if self.current_bet < c.MAX_BET:
            self.current_bet += c.BET_INCREMENT
            print(f"Bet increased to {self.current_bet}")
        else:
            print("Maximum bet reached!")

    def decrease_current_bet(self):
        if self.current_bet > c.MIN_BET:
            self.current_bet -= c.BET_INCREMENT
            self.current_bet = max(self.current_bet, c.MIN_BET)
            print(f"Bet decreased to {self.current_bet}")
        else:
            print("Minimum bet reached!")

    def place_bet_and_deal(self):
        print(f"Placing bet: {self.current_bet} and dealing cards.")
        if self.current_bet > self.game.player.chips:
            print("Bet exceeds available chips!")
            self.game.message = "Bet exceeds available chips! Lower bet to continue."
            return
        
        success = self.game.start_round(self.current_bet)
        if not success:
            print(f"Failed to start round: {self.game.message}")
        
        self.update_game_buttons()

    ##### Player Action Methods #####
    def player_hit(self):
        print("Player hit!")
        self.game.hit()
        self.update_game_buttons()
    
    def player_stand(self):
        print("Player stand!")
        self.game.stand()
        self.update_game_buttons()

    def player_double_down(self):
        print("Player double down!")
        self.game.double_down()
        self.update_game_buttons()

    def player_split(self):
        print("Player split!")
        self.game.split()
        self.update_game_buttons()

    def update_game_buttons(self):
        self.buttons.clear()
        if self.game.state == GameState.BETTING:
            bet_text_str = f"Bet: ${self.current_bet}"
            bet_text_surf = self.hud_font.render(bet_text_str, True, c.WHITE)
            bet_text_rect = bet_text_surf.get_rect()

            total_width = (self.bet_decrease_button.rect.width +
                           c.HUD_BET_ELEMENT_SPACING +
                           bet_text_rect.width +
                           c.HUD_BET_ELEMENT_SPACING +
                           self.bet_increase_button.rect.width +
                           c.HUD_BET_ELEMENT_SPACING +
                           self.deal_button.rect.width)
            current_x = (c.SCREEN_WIDTH - total_width) // 2
            
            # Position bet decrease button
            self.bet_decrease_button.rect.left = current_x
            self.bet_decrease_button.rect.centery = c.HUD_BET_CONTROLS_Y_CENTER
            current_x += self.bet_decrease_button.rect.width + c.HUD_BET_ELEMENT_SPACING

            # bet text position (we want it to be centered between the two buttons)
            self.bet_text_render_rect = bet_text_surf.get_rect(left=current_x, centery=c.HUD_BET_CONTROLS_Y_CENTER)
            current_x += bet_text_rect.width + c.HUD_BET_ELEMENT_SPACING

            # Position bet increase button
            self.bet_increase_button.rect.left = current_x
            self.bet_increase_button.rect.centery = c.HUD_BET_CONTROLS_Y_CENTER
            current_x += self.bet_increase_button.rect.width + c.HUD_BET_ELEMENT_SPACING

            # Position deal button
            self.deal_button.rect.left = current_x
            self.deal_button.rect.centery = c.HUD_BET_CONTROLS_Y_CENTER

            self.buttons.extend([self.bet_decrease_button, self.bet_increase_button, self.deal_button])
        elif self.game.state == GameState.PLAYER_TURN:
            # Player action buttons (hit, stand, double, split)
            action_buttons_to_display = [self.hit_button, self.stand_button]

            # Log to determine if double down is available
            # Because game logic already checks for double down, we can just check if the player has enough chips
            if len(self.game.player.current_hand.cards) == 2:
                action_buttons_to_display.append(self.double_down_button)
                # check for split
                p_hand = self.game.player.current_hand
                if len(p_hand.cards) == 2 and p_hand.cards[0].rank == p_hand.cards[1].rank and self.game.player.chips >= self.game.player.current_bet:
                    action_buttons_to_display.append(self.split_button)

            num_actions_buttons = len(action_buttons_to_display)
            # calculate the total width of the action buttons
            total_action_buttons_width = num_actions_buttons * c.ACTION_BUTTON_WIDTH +(num_actions_buttons - 1) * c.ACTION_BUTTON_SPACING
            current_x = (c.SCREEN_WIDTH - total_action_buttons_width) // 2

            for btn in action_buttons_to_display:
                btn.rect.left = current_x
                btn.rect.centery = c.ACTION_BUTTON_Y
                self.buttons.append(btn)
                current_x += btn.rect.width + c.ACTION_BUTTON_SPACING
        elif self.game.state == GameState.DEALER_TURN:
            # TODO: ADD "new round" button or "continue" button
            pass

    ##### Instructions and Exit Methods #####
    def show_instructions(self):
        print("Instructions button pressed!")
        self.current_screen = "instructions"
        self.buttons.clear()

        self.buttons.append(self.back_button)

    def exit_game(self):
        print("Exit button pressed!")
        pygame.quit()
        exit()

    ##### This is where the magic happens #####
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

        elif self.current_screen == 'game_active':
            # Draw chip image
            chip_text_surf = self.chip_font.render(f"$ {self.game.player.chips}", True, c.WHITE)
            chip_text_rect = chip_text_surf.get_rect(centery=c.HUD_CHIP_COUNT_Y)
            chip_text_rect.left = c.HUD_CHIP_COUNT_X

            if self.chip_image:
                img_rect = self.chip_image.get_rect(centery=c.HUD_CHIP_COUNT_Y)
                img_rect.right = chip_text_rect.left - 10
                self.screen.blit(self.chip_image, img_rect)
            else:
                # Placeholder for chip image if loading fails
                placeholder_img = pygame.Rect(self.screen, c.BROWN, (0, 0, c.HUD_CHIP_IMAGE_SIZE[0], c.HUD_CHIP_IMAGE_SIZE[1]))
                placeholder_img.right = chip_text_rect.left - 10
                placeholder_img.centery = c.HUD_CHIP_COUNT_Y
                pygame.draw.rect(self.screen, c.BROWN, placeholder_img)
            self.screen.blit(chip_text_surf, chip_text_rect)

            if self.game.state == GameState.BETTING:
                bet_text_str = f"Bet: ${self.current_bet}"
                bet_text_str = self.hud_font.render(bet_text_str, True, c.WHITE)
                if hasattr(self, 'bet_text_render_rect'):
                    self.screen.blit(bet_text_str, self.bet_text_render_rect)
                if self.game.message:
                    message_surf = self.chip_font.render(self.game.message, True, c.WHITE)
                    msg_y_pos = c.HUD_BET_CONTROLS_Y_CENTER - c.HUD_GAME_MESSAGE_Y_OFFSET
                    message_rect = message_surf.get_rect(center=(c.SCREEN_WIDTH // 2, msg_y_pos))
                    self.screen.blit(message_surf, message_rect)
            else:
                if self.game.message:
                    message_surf = self.chip_font.render(self.game.message,True, c.WHITE)
                    message_rect = message_surf.get_rect(center=(c.SCREEN_WIDTH // 2, 50))
                    self.screen.blit(message_surf, message_rect)
                # Display player and dealer hands
                if self.game.dealer and self.game.dealer.hand.cards:
                    dealer_hand_str = self.game.dealer.show_partial_hand() if self.game.state == GameState.PLAYER_TURN else str(self.game.dealer.hand)
                    dealer_text_surf = self.hud_font.render(f"Dealer: {dealer_hand_str} (Value: {self.game.dealer.hand.value if self.game.state != GameState.PLAYER_TURN or not self.game.dealer.hand.cards[1].face_up == False else '?'})", True, c.WHITE)
                    dealer_text_rect = dealer_text_surf.get_rect(center=(c.DEALER_HAND_TEXT_X, c.DEALER_HAND_TEXT_Y))
                    self.screen.blit(dealer_text_surf, dealer_text_rect)

                # Display Player's hand(s) (text placeholder)
                if self.game.player and self.game.player.hands:
                    for i, hand in enumerate(self.game.player.hands):
                        player_hand_str = str(hand)
                        player_text_surf = self.hud_font.render(f"Player Hand {i+1}: {player_hand_str} (Value: {hand.value})", True, c.WHITE)
                        # Adjust Y for multiple hands if splitting occurs
                        player_text_rect = player_text_surf.get_rect(center=(c.PLAYER_HAND_TEXT_X, c.PLAYER_HAND_TEXT_Y + i * 40))
                        self.screen.blit(player_text_surf, player_text_rect)

                

            if self.game.message:
                message_surf = self.chip_font.render(self.game.message, True, c.WHITE)
                msg_y_pos = c.HUD_BET_CONTROLS_Y_CENTER - c.HUD_GAME_MESSAGE_Y_OFFSET
                message_rect = message_surf.get_rect(center=(c.SCREEN_WIDTH // 2, msg_y_pos))
                self.screen.blit(message_surf, message_rect)

        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()

    # Handles event mouse clicks and keyboard inputs
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




    