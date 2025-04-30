# Program 4 - CS 335 - Spring 2025
# Black Jack Game using Python and Pygame
# Written By [Braxton Goble, Brian Chu, Clark Conrad, Leighanne Lyvers]
#


import random
import sys
import os
from enum import Enum
from typing import List, Tuple, Dict, Optional, Union
import time

# these are the different states our game can be in
class GameState(Enum):
    BETTING = 0
    PLAYER_TURN = 1
    DEALER_TURN = 2
    GAME_OVER = 3


class Card:
    
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank
        self.value = self._get_value()
        self.is_ace = (rank == 'A')
        self.face_up = True
        
    def _get_value(self) -> int:
       # get the value of the card for blackjack
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)
    
    def __str__(self) -> str:
        # string representation of the card
        if not self.face_up:
            return "Face Down Card"
        return f"{self.rank} of {self.suit}"


class Deck:
    
    def __init__(self, num_decks: int = 1):
        self.cards = []
        self._create_deck(num_decks)
        self.shuffle()
        
    def _create_deck(self, num_decks: int) -> None:
        # create a deck of cards with the specified number of decks
        for _ in range(num_decks):
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    self.cards.append(Card(suit, rank))
    
    def shuffle(self) -> None:
        # shuffle the deck randomly
        random.shuffle(self.cards)
    
    def deal(self) -> Optional[Card]:
        # take the top card from the deck
        if not self.cards:
            return None
        return self.cards.pop()
    
    def __len__(self) -> int:
        # how many cards left in the deck
        return len(self.cards)


class Hand:
    
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self, card: Card) -> None:
        # add a card to the hand and update the value
        self.cards.append(card)
        self.value += card.value
        
        # keep track of aces since their value can change
        if card.is_ace:
            self.aces += 1
            
        # If we're over 21, try to use aces as 1 instead of 11
        self._adjust_for_ace()
            
    def _adjust_for_ace(self) -> None:
        # adjust the value of aces if we go over 21
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
            
    def clear(self) -> None:
        # reset the hand
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def __str__(self) -> str:
        #list the cards in the hand
        return ", ".join(str(card) for card in self.cards)
    
    def is_blackjack(self) -> bool:
        # check if the hand is a blackjack (21 with 2 cards)
        return len(self.cards) == 2 and self.value == 21


class Player:
    
    def __init__(self, name: str, chips: int = 1000):
        self.name = name
        self.chips = chips
        self.hands = [Hand()]  # can have multiple hands when splitting
        self.current_hand_index = 0
        self.bets = [0]  # track bets for each hand
        
    def place_bet(self, amount: int, hand_index: int = 0) -> bool:
        #put the chips down, return True if successful
        if amount > self.chips:
            return False
        
        self.chips -= amount
        self.bets[hand_index] += amount
        return True
    
    def add_chips(self, amount: int) -> None:
        # add the winnings to the players stack
        self.chips += amount
        
    def clear_hands(self) -> None:
        # start fresh with emmpty hands
        self.hands = [Hand()]
        self.current_hand_index = 0
        self.bets = [0]
        
    def split_hand(self) -> bool:
        # split the current hand into two hands if possible
        current_hand = self.hands[self.current_hand_index]
        
        # can only split pairs (same value cards)
        if len(current_hand.cards) != 2 or current_hand.cards[0].value != current_hand.cards[1].value:
            return False
        
        # need enough chips to match the original bet
        if self.chips < self.bets[self.current_hand_index]:
            return False
        
        # create a new hand with one of the cards
        new_hand = Hand()
        new_hand.add_card(current_hand.cards.pop())
        
        # recalculate first hand's value after removing a card
        current_hand._adjust_for_ace()
        
        # set up the new hand with matching bet
        self.hands.append(new_hand)
        self.bets.append(0)
        self.place_bet(self.bets[self.current_hand_index], len(self.hands) - 1)
        
        return True
    
    @property
    def current_hand(self) -> Hand:
        # get the hand that is in play
        return self.hands[self.current_hand_index]


class Dealer:
    # the dealer will play by the book exactly
    
    def __init__(self):
        self.hand = Hand()
        
    def show_partial_hand(self) -> str:
        # show only the first card and hide the second one
        if len(self.hand.cards) > 0:
            return f"Dealer shows: {self.hand.cards[0]}, Face Down Card"
        return "Dealer has no cards"
    
    def should_hit(self) -> bool:
        # dealers play by the book - hit until they have 17 or more
        return self.hand.value < 17


class BlackjackGame:
    # main game logic and state management
    
    def __init__(self, num_decks: int = 6):
        self.deck = Deck(num_decks)
        self.player = Player("Player")
        self.dealer = Dealer()
        self.state = GameState.BETTING
        self.message = "Place your bet!"
        
    def start_round(self, bet: int) -> bool:
        # start a new round of blackjack
        if self.state != GameState.BETTING:
            self.message = "Complete the current round first!"
            return False
        
        if not self.player.place_bet(bet):
            self.message = "Not enough chips!"
            return False
        
        # fresh start with new cards
        self.player.clear_hands()
        self.dealer.hand.clear()
        
        # reshuffle if we're running low on cards
        if len(self.deck) < 10:
            self.deck = Deck(6)
        
        # deal the initial cards like in a real casino
        self.player.current_hand.add_card(self.deck.deal())
        self.dealer.hand.add_card(self.deck.deal())
        self.player.current_hand.add_card(self.deck.deal())
        
        # set the bet for this hand
        self.player.bets[0] = bet
        
        # dealer's second card is face down until player finishes
        card = self.deck.deal()
        card.face_up = False
        self.dealer.hand.add_card(card)
        
        # check if player hit blackjack right away
        if self.player.current_hand.is_blackjack():
             # flip dealer's card to see if they also have blackjack
            self.dealer.hand.cards[1].face_up = True
            
            if self.dealer.hand.is_blackjack():
                self.message = "Both have Blackjack! Push!"
                self.player.add_chips(self.player.bets[0])
            else:
                blackjack_payout = int(self.player.bets[0] * 2.5)
                self.message = f"Blackjack! You win ${blackjack_payout - self.player.bets[0]}!"
                self.player.add_chips(blackjack_payout)
            
            self.state = GameState.GAME_OVER
        else:
            self.state = GameState.PLAYER_TURN
            self.message = "Your turn! Hit, Stand, Double, or Split?"
        
        return True
    
    def hit(self) -> None:
        #take another card
        if self.state != GameState.PLAYER_TURN:
            self.message = "Cannot hit right now!"
            return
        
        current_hand = self.player.current_hand
        current_hand.add_card(self.deck.deal())
        
        if current_hand.value > 21:
            self.message = f"Bust! Hand value: {current_hand.value}"
            
            # move to next hand or dealer's turn
            self.next_hand()
        else:
            self.message = f"Hit! Hand value: {current_hand.value}"
    
    def stand(self) -> None:
        # stop taking cards and move to the next hand or dealer's turn
        if self.state != GameState.PLAYER_TURN:
            self.message = "Cannot stand right now!"
            return
        
        # move to next hand or dealer's turn
        self.next_hand()
    
    def double_down(self) -> None:
        #double your bet and take one final car
        if self.state != GameState.PLAYER_TURN:
            self.message = "Cannot double down right now!"
            return
        
        current_hand = self.player.current_hand
        current_hand_index = self.player.current_hand_index
        
        if len(current_hand.cards) != 2:
            self.message = "Can only double down on the initial two cards!"
            return
        
        current_bet = self.player.bets[current_hand_index]
        
        if not self.player.place_bet(current_bet, current_hand_index):
            self.message = "Not enough chips to double down!"
            return
        
        # take one final card and end turn
        current_hand.add_card(self.deck.deal())
        
        if current_hand.value > 21:
            self.message = f"Bust on double down! Hand value: {current_hand.value}"
        else:
            self.message = f"Doubled down! Hand value: {current_hand.value}"
        
        # move to next hand or dealer's turn
        self.next_hand()
    
    def split(self) -> None:
        #split the current hand into two hands if possible
        if self.state != GameState.PLAYER_TURN:
            self.message = "Cannot split right now!"
            return
        
        if self.player.split_hand():
            current_hand = self.player.current_hand
            
            # deal a card to the current hand
            current_hand.add_card(self.deck.deal())
            self.message = f"Hand split! Current hand value: {current_hand.value}"
        else:
            self.message = "Cannot split this hand!"
    
    def next_hand(self) -> None:
        # move to the next hand if we have one, otherwise dealer's turn
        # check if we have more hands to play
        if self.player.current_hand_index < len(self.player.hands) - 1:
            self.player.current_hand_index += 1
            self.message = f"Playing hand {self.player.current_hand_index + 1}. Hit, Stand, Double, or Split?"
        else:
            # all hands played, dealer's turn now
            self.start_dealer_turn()
    
    def start_dealer_turn(self) -> None:
        self.state = GameState.DEALER_TURN
        
        # flip over the dealer's hidden card
        self.dealer.hand.cards[1].face_up = True
        
        # if all player hands busted, no need for dealer to play
        all_busted = True
        for hand in self.player.hands:
            if hand.value <= 21:
                all_busted = False
                break
        
        if all_busted:
            self.end_round()
            return
        
        # let the dealer play their hand
        self.play_dealer_hand()
    
    def play_dealer_hand(self) -> None:
        # dealer plays by the book, hitting until they have 17 or more
        while self.dealer.should_hit():
            self.dealer.hand.add_card(self.deck.deal())
        
        self.end_round()
    
    def end_round(self) -> None:
        # determine the winner and update chips
        self.state = GameState.GAME_OVER
        dealer_value = self.dealer.hand.value
        dealer_busted = dealer_value > 21
        
        results = []
        
        for i, hand in enumerate(self.player.hands):
            bet = self.player.bets[i]
            
            if hand.value > 21:
                results.append(f"Hand {i+1}: Busted! You lose ${bet}")
                # no chips returned for a bust
            elif dealer_busted:
                # dealer busts, player wins
                self.player.add_chips(bet * 2)  # original bet + winnings
                results.append(f"Hand {i+1}: Dealer busts! You win ${bet}")
            elif hand.value > dealer_value:
                # player beats dealer
                self.player.add_chips(bet * 2)  # original bet + winnings
                results.append(f"Hand {i+1}: You win ${bet}!")
            elif hand.value < dealer_value:
                # dealer beats player
                results.append(f"Hand {i+1}: Dealer wins. You lose ${bet}")
            else:
                # push (tie)
                self.player.add_chips(bet)  # get your bet back
                results.append(f"Hand {i+1}: Push! Bet returned")
        
        self.message = " | ".join(results) + f" | Chips: ${self.player.chips}"
    
    def place_bet_and_start(self, bet: int) -> None:
        if self.state == GameState.BETTING or self.state == GameState.GAME_OVER:
            self.start_round(bet)
        else:
            self.message = "Complete the current round first!"
    
    def new_round(self) -> None:
        # reset everything
        self.state = GameState.BETTING
        self.message = "Place your bet!"


class TextInterface:
    # text-based interface for the game, will be replaced by a GUI later
    
    def __init__(self, game: BlackjackGame):
        self.game = game
        self.is_running = True
    
    def clear_screen(self) -> None:
        # wipe da screen
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_game_state(self) -> None:
        # show the state of the game
        self.clear_screen()

        print("\n" + "=" * 80)
        print(f"{'BLACKJACK':^80}")
        print("=" * 80 + "\n")

        # game message
        print(f"Message: {self.game.message}\n")

        # player's chip stack
        print(f"Chips: ${self.game.player.chips}\n")

        print("┏" + "━" * 78 + "┓")
        print("┃" + f"{'DEALER':^78}" + "┃")
        print("┣" + "━" * 78 + "┫")

        # show dealer's cards
        if self.game.state in [GameState.DEALER_TURN, GameState.GAME_OVER]:
            dealer_hand = f"Dealer's hand: {self.game.dealer.hand} (Value: {self.game.dealer.hand.value})"
            print("┃" + f"{dealer_hand:<78}" + "┃")
        else:
            partial_hand = self.game.dealer.show_partial_hand()
            print("┃" + f"{partial_hand:<78}" + "┃")
        print("┗" + "━" * 78 + "┛")

        print("\n")  # Add extra space between dealer and player sections

        print("┏" + "━" * 78 + "┓")
        print("┃" + f"{'YOUR HANDS':^78}" + "┃")
        print("┣" + "━" * 78 + "┫")

        # show player's hands
        if not self.game.player.hands or (len(self.game.player.hands) == 1 and not self.game.player.hands[0].cards):
            print("┃" + f"{'No cards dealt yet':<78}" + "┃")
        else:
            for i, hand in enumerate(self.game.player.hands):
                current_marker = " → " if i == self.game.player.current_hand_index and self.game.state == GameState.PLAYER_TURN else "   "

                hand_info = f"{current_marker}Hand {i+1}: {hand} (Value: {hand.value})"
                bet_info = f"   Bet: ${self.game.player.bets[i]}"

                print("┃" + f"{hand_info:<78}" + "┃")
                print("┃" + f"{bet_info:<78}" + "┃")

                # Add a separator between hands if there are multiple
                if i < len(self.game.player.hands) - 1:
                    print("┃" + "―" * 78 + "┃")

        print("┗" + "━" * 78 + "┛")

        print("\n")  # Add space before actions

        # show available actions based on game state
        print("Available Actions:")
        if self.game.state == GameState.BETTING:
            print("  [10-500] Enter bet amount")
            print("  [N] New round")
            print("  [Q] Quit")
        elif self.game.state == GameState.PLAYER_TURN:
            print("  [H] Hit")
            print("  [S] Stand")
            print("  [D] Double Down")
            print("  [P] Split")
            print("  [Q] Quit")
        elif self.game.state == GameState.GAME_OVER:
            print("  [N] New round")
            print("  [Q] Quit")
        else:
            print("  Dealer is playing...")
            time.sleep(1)

        print("\n" + "=" * 80 + "\n")
    
    def get_user_input(self) -> str:
        return input("Enter your choice: ").strip().upper()
    
    def handle_input(self, user_input: str) -> None:
        # quit the game
        if user_input == 'Q':
            self.is_running = False
            return
        
        # bet or start a new round
        if self.game.state == GameState.BETTING or self.game.state == GameState.GAME_OVER:
            if user_input == 'N':
                self.game.new_round()
            else:
                try:
                    bet_amount = int(user_input)
                    if 10 <= bet_amount <= 500:  # range of valid bets
                        self.game.place_bet_and_start(bet_amount)
                    else:
                        print("Invalid bet amount. Please enter a value between 10 and 500.")
                        time.sleep(1.5)
                except ValueError:
                    print("Invalid input. Please try again.")
                    time.sleep(1.5)
        
        # player's turn actions
        elif self.game.state == GameState.PLAYER_TURN:
            if user_input == 'H':
                self.game.hit()
            elif user_input == 'S':
                self.game.stand()
            elif user_input == 'D':
                self.game.double_down()
            elif user_input == 'P':
                self.game.split()
            else:
                print("Invalid action. Please try again.")
                time.sleep(1.5)
    
    def run(self) -> None:
        # main game loop
        while self.is_running:
            self.display_game_state()
            
            # dealer plays automatically without user input
            if self.game.state == GameState.DEALER_TURN:
                self.game.play_dealer_hand()
                continue
                
            user_input = self.get_user_input()
            self.handle_input(user_input)


def main():
    print("Welcome to Blackjack!")
    print("This is a text-based version that will get replaced by the GUI version")
    time.sleep(2)
    
    game = BlackjackGame()
    interface = TextInterface(game)
    
    try:
        interface.run()
    except KeyboardInterrupt:
        print("\n Byeeeeeeee!")    
    
    print("Game ended. Your final chip count: $" + str(game.player.chips))

main()