import os, sys

# Window dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Colors
GREEN = (88, 129, 87)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (52, 78, 65)
BROWN = (111, 40, 12)

# Menu Button Dimensions, Colors, and Font
MUTTON_WIDTH = 200
MUTTON_HEIGHT = 100
MUTTON_COLOR = DARK_GREEN
MUTTON_HOVER_COLOR = GREEN
MUTTON_TEXT_COLOR = WHITE
MUTTON_FONT_SIZE = 36 # Default font size for menu buttons
MUTTON_PADDING = 20

# More Font sizes
FONT_SIZE_TITLE_MAIN_MENU = 72
FONT_SIZE_TITLE_SCREENS = 72
FONT_SIZE_PLAYER_LABELS_VALUES = 48
FONT_SIZE_CHIPS_LABELS_VALUES = 40
FONT_SIZE_ADJUST_BUTTON_INTERNAL = 48 
FONT_SIZE_INSTRUCTION_LINES = 36    
FONT_SIZE_GAME_OVER_MESSAGE = 28

# Game Settings Screen Layout (GS_ prefix)
GS_ADJUST_BUTTON_SIZE = 70
GS_SPACING_TITLE_TO_FIRST_ROW = 75  # Vertical space below "Game Settings" title to player row (center-to-center aspect)
GS_SPACING_ROW_TO_ROW_CENTER = 120  # Vertical space between player row center and chip row center

GS_LABEL_CENTER_X_OFFSET = -150
GS_VALUE_BLOCK_CENTER_X_OFFSET = 120
GS_ADJUST_BTN_OFFSET_FROM_VALUE = 70

# Other UI Element Spacing
MENU_TITLE_Y_POS = 150
INSTRUCTIONS_TITLE_Y_POS = 100 # Initial Y for instructions title, might be adjusted by centering logic if applied there too
INSTRUCTIONS_TEXT_Y_START = 200
INSTRUCTIONS_TEXT_LINE_SPACING = 40

# I have to do this because it throws a fit when I try to execute main from src instead of the root folder
# This is a workaround to get the base directory of the assets folder
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Game Screen HUD (Chips, Bet Buttons, Reset, Return to Menu)
HUD_CHIP_COUNT_X = 100 # X position for chip count text
HUD_CHIP_COUNT_Y = SCREEN_HEIGHT - 50 
HUD_CHIP_IMAGE_PATH = os.path.join(BASE_DIR, 'assets', 'pokerstack.png')
HUD_CHIP_IMAGE_SIZE = (40, 40)
HUD_CHIP_IMAGE_X = HUD_CHIP_COUNT_X - 50
HUD_CHIP_IMAGE_Y = HUD_CHIP_COUNT_Y

HUD_BET_CONTROLS_Y_CENTER = SCREEN_HEIGHT - 70 # center the bet button and text rows
HUD_GAME_MESSAGE_Y_OFFSET = 45 # space for message above controls

HUD_CURRENT_BET_X = SCREEN_WIDTH // 2
HUD_CURRENT_BET_Y = SCREEN_HEIGHT - 100
HUD_BET_BUTTON_SIZE = 50
HUD_BET_BUTTON_FONT_SIZE = 36
HUD_CHIP_FONT_SIZE = 40
HUD_LABEL_FONT_SIZE = 28
HUD_BET_BUTTON_Y = SCREEN_HEIGHT - 50
HUD_DEAL_BUTTON_WIDTH = 120
HUD_DEAL_BUTTON_HEIGHT = 50
HUD_BET_ELEMENT_SPACING = 15
GAME_OVER_MESSAGE_MARGIN_ABOVE_BUTTON = 20

# Bet Constraints
MIN_CHIP_SETTING = 100
MIN_BET = 10
MAX_BET = 500
BET_INCREMENT = 10

# Player Action Buttons Constants
ACTION_BUTTON_WIDTH = 150
ACTION_BUTTON_HEIGHT = 60
ACTION_BUTTON_FONT_SIZE = 28
ACTION_BUTTON_Y = SCREEN_HEIGHT - 150 # Y position for the row of action buttons
ACTION_BUTTON_SPACING = 20 # Horizontal spacing between action buttons

# Text Display Positions for Hands/Scores
PLAYER_HAND_TEXT_X = SCREEN_WIDTH // 2
PLAYER_HAND_TEXT_Y = SCREEN_HEIGHT // 2
DEALER_HAND_TEXT_X = SCREEN_WIDTH // 2
DEALER_HAND_TEXT_Y = SCREEN_HEIGHT // 2 - 100

CARD_IMAGE_FOLDER = os.path.join(BASE_DIR, 'assets', 'cards')

# Card Dimensions
CARD_WIDTH = 100
CARD_HEIGHT = 140
CARD_SPACING = 25

CARD_SPACING_IN_HAND = 30 # when displayed in hand
CARD_BACK_KEY = "back_of_card"

# Card positions
DEALER_HAND_Y_CENTER = SCREEN_HEIGHT // 4
PLAYER_HAND_Y_CENTER = SCREEN_HEIGHT - 300

# Action buttons positions relative to hand
ACTION_BUTTON_Y_OFFSET_FROM_CARDS = CARD_HEIGHT // 2 + 40
HAND_VALUE_TEXT_Y_OFFSET = - (CARD_HEIGHT // 2 + 25)

# New Round Button (for after game over)
NEW_ROUND_BUTTON_WIDTH = MUTTON_WIDTH
NEW_ROUND_BUTTON_HEIGHT = MUTTON_HEIGHT
NEW_ROUND_FONT_SIZE = MUTTON_FONT_SIZE
NEW_ROUND_BUTTON_Y = ACTION_BUTTON_Y

# Utility buttons (reset, return to menu)
UTIL_BUTTON_WIDTH = 180  # Slightly smaller than main menu buttons
UTIL_BUTTON_HEIGHT = 50
UTIL_BUTTON_FONT_SIZE = 24
UTIL_BUTTON_TOP_MARGIN = 20
UTIL_BUTTON_RIGHT_MARGIN = 20
UTIL_BUTTON_SPACING = 10

FINAL_GAME_OVER_BUTTON_Y = SCREEN_HEIGHT // 2 + 100