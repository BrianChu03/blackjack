import pygame
import sys
import guiconstants as c
from gui import GUI
from deck import load_card_image
from CardClass import Card, Deck, Dealer, Hand, Player
from enum import Enum

class GameState(Enum):
    BETTING = 0
    PLAYER_TURN = 1
    DEALER_TURN = 2
    GAME_OVER = 3
class BlackjackGame:
    def __init__(self, num_decks: int = 6):
        #load card assets 
        # self.card_images = load_card_image()
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





    