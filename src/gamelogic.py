import pygame
import sys
import guiconstants as c
from deck import load_card_image
from CardClass import Card, Deck, Dealer, Hand, Player
from enum import Enum

class GameState(Enum):
    BETTING = 0
    PLAYER_TURN = 1
    DEALER_TURN = 2
    GAME_OVER = 3
class BlackjackGame:
    def __init__(self, num_players: int = 1, num_decks: int = 6):
        self.deck = Deck(num_decks)
        # Added multiple players
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.num_players = num_players
        self.current_player_index = 0
        self.dealer = Dealer()
        self.state = GameState.BETTING
        self.message = f"{self.get_current_player().name}, place your bet!" if self.players else "Place your bet!"
        # Flag to check if all players have placed their bets
        self.all_bets_placed = False 

    # Get the current player based on the index
    def get_current_player(self) -> Player | None:
        if 0 <= self.current_player_index < len(self.players):
            return self.players[self.current_player_index]
        return None
    
    #!!!!removed old start_round method because I need to handle multiple players now. I created two new internal methods to handle the player and dealer turns separately.
    '''
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
    '''
    # removed old start_round method because I need to handle multiple players now. I created two new internal methods to handle the player and dealer turns separately.
    def accept_player_bet(self, bet_amount: int) -> bool:
        if self.state != GameState.BETTING or self.all_bets_placed:
            self.message = "Not in betting phase or all bets already placed."
            return False

        current_player = self.get_current_player()
        if not current_player:
            self.message = "Error: No current player to accept bet."
            return False

         # place_bet already handles hand_index 0 and stores in player.bets[0]
        if not current_player.place_bet(bet_amount):
            self.message = f"{current_player.name}: Not enough chips for ${bet_amount} bet!"
            return False # Bet failed
        
        # Bet successfully placed for current_player
        print(f"{current_player.name} bet ${bet_amount}. Chips left: ${current_player.chips}")

        self.current_player_index += 1
        if self.current_player_index < self.num_players:
            next_player = self.get_current_player()
            self.message = f"{next_player.name}, place your bet!"
            return True # Bet accepted, moved to next player for betting
        else:
            # All players have placed their bets
            self.all_bets_placed = True
            self.current_player_index = 0
            self.message = "All bets placed. Dealing cards..."
            self._deal_initial_cards_and_setup_play()
            return True # All bets placed, cards dealt
        
    def _deal_initial_cards_and_setup_play(self):
        # Reset hands for all players and dealer (bets are already placed and stored)
        for player in self.players:
            player.hands = [Hand()]
            player.current_hand_index = 0

        self.dealer.hand.clear()
        
        # Reshuffle if running low on cards
        if len(self.deck) < (self.num_players + 1) * 5: # Adjusted threshold
            self.deck = Deck(6) # Or your configured num_decks
        
        # Dealing sequence
        # One card to each player, face up.
        for player in self.players:
            player.hands[0].add_card(self.deck.deal()) # Add to the first hand

        # Dealer's first card, face up.
        self.dealer.hand.add_card(self.deck.deal())
        
        # Second card to each player, face up.
        for player in self.players:
            player.hands[0].add_card(self.deck.deal())

        # Dealer's second card, face down.
        dealer_second_card = self.deck.deal()
        dealer_second_card.face_up = False
        self.dealer.hand.add_card(dealer_second_card)

        # Transition to the first player's turn
        self.state = GameState.PLAYER_TURN
        self.current_player_index = -1 # Will be incremented by next_player_or_dealer first
        self.next_player_or_dealer() # This will set message and handle initial BJs

    def hit(self) -> None:
        current_player = self.get_current_player()
        #take another card
        if self.state != GameState.PLAYER_TURN or not current_player:
            self.message = "Cannot hit right now!"
            return
        
        current_hand = current_player.current_hand
        current_hand.add_card(self.deck.deal())
        
        if current_hand.value > 21:
            self.message = f"{current_player.name} busts! Hand value: {current_hand.value}"
            # move to next hand or player or dealer's turn
            self.next_hand_or_player()
        else:
            self.message = f"{current_player.name} hits. Hand value: {current_hand.value}"

    def stand(self) -> None:
        # stop taking cards and move to the next hand or dealer's turn
        current_player = self.get_current_player()
        if self.state != GameState.PLAYER_TURN or not current_player:
            self.message = "Cannot stand right now!"
            return
        
        # move to next hand or dealer's turn
        self.message = f"{current_player.name} stands."
        self.next_hand_or_player()
    
    def double_down(self) -> None:
        #double your bet and take one final car
        current_player = self.get_current_player()
        if self.state != GameState.PLAYER_TURN or not current_player:
            self.message = "Cannot double down right now!"
            return
        
        current_hand = current_player.current_hand
        current_hand_index = current_player.current_hand_index
        
        if len(current_hand.cards) != 2:
            self.message = "Can only double down on the initial two cards!"
            return
        
        current_bet = current_player.bets[current_hand_index]
        if not current_player.place_bet(current_bet, current_hand_index): # place_bet doubles the bet on that hand
            self.message = f"{current_player.name}: Not enough chips to double down!"
            return
        
        # take one final card and end turn
        current_hand.add_card(self.deck.deal())
        
        if current_hand.value > 21:
            self.message = f"{current_player.name} busts on double down! Hand value: {current_hand.value}"
        else:
            self.message = f"{current_player.name} doubled down. Hand value: {current_hand.value}"
        
        # move to next hand or dealer's turn
        self.next_hand_or_player()
    
    def split(self) -> None:
        #split the current hand into two hands if possible
        current_player = self.get_current_player()
        if self.state != GameState.PLAYER_TURN or not current_player:
            self.message = "Cannot split right now!"
            return
        
        # This method in Player class should handle placing the additional bet
        if current_player.split_hand(): 
            # Deal to first split hand
            current_player.hands[current_player.current_hand_index].add_card(self.deck.deal())
            # Deal to the second split hand (now the next hand in the list for that player)
            current_player.hands[current_player.current_hand_index + 1].add_card(self.deck.deal())
            self.message = f"{current_player.name} split. Playing hand {current_player.current_hand_index + 1}. Value: {current_player.current_hand.value}"
            # Player continues playing the current hand. next_hand_or_player will handle moving to the second split hand.
        else:
            self.message = "Cannot split this hand!"
    
    def next_hand_or_player(self) -> None:
        # move to the next hand if we have one, otherwise dealer's turn
        # check if we have more hands to play
        current_player = self.get_current_player()
        if not current_player: return

        if len(current_player.current_hand.cards) == 1:
            current_player.current_hand.add_card(self.deck.deal())

        # Check if current player has more hands to play (due to splitting)
        if current_player.current_hand_index < len(current_player.hands) - 1:
            current_player.current_hand_index += 1
            # Deal one card to the new current hand if it's a result of a split and only has one card
            if len(current_player.current_hand.cards) == 1:
                 current_player.current_hand.add_card(self.deck.deal())
            self.message = f"{current_player.name}, playing hand {current_player.current_hand_index + 1}. Value: {current_player.current_hand.value}"
        else:
            # Current player has finished all their hands, move to the next player
            self.next_player_or_dealer()
    
    def next_player_or_dealer(self) -> None:
        self.current_player_index += 1
        if self.current_player_index < self.num_players:
            current_player = self.get_current_player()
            self.message = f"{current_player.name}'s turn. Hit, Stand, Double, or Split?"
            # Check for Blackjack for the new current player
            if current_player.current_hand.is_blackjack():
                self.message = f"{current_player.name} has Blackjack!"
                # Recursively move if next player also has BJ
                self.next_player_or_dealer() 
        else:
            # All players have played, dealer's turn now
            self.start_dealer_turn()

    def start_dealer_turn(self) -> None:
        self.state = GameState.DEALER_TURN
        self.message = "Dealer's turn."
        if not self.dealer.hand.cards or len(self.dealer.hand.cards) < 2: # Should not happen !!!
            self.end_round()
            return
        self.dealer.hand.cards[1].face_up = True
        
        all_players_busted_or_blackjack = True
        for player in self.players:
            player_has_active_hand = False
            for hand in player.hands:
                if hand.value <= 21 and not hand.is_blackjack(): # Only consider hands that need dealer to play
                    player_has_active_hand = True
                    break
            if player_has_active_hand:
                all_players_busted_or_blackjack = False
                break
        
        if all_players_busted_or_blackjack:
            self.message = "All player hands are Busted or Blackjack. Resolving bets."
            self.end_round()
            return
        
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
        is_dealer_blackjack = self.dealer.hand.is_blackjack()
        
        round_summary_parts = []

        # have to loop through all players and their hands to resolve bets
        for player in self.players:
            player_chips_change = 0 # To summarize total win/loss for the player this round
            player_specific_messages = []
            for i, hand in enumerate(player.hands):
                bet = player.bets[i]
                hand_label = f"{player.name} Hand {i+1}" if len(player.hands) > 1 else player.name

                if hand.is_blackjack():
                    if is_dealer_blackjack:
                        player_specific_messages.append(f"{hand_label}: Push (Both Blackjack)")
                        player.add_chips(bet) # Return bet
                    else:
                        blackjack_payout = int(bet * 2.5)
                        player.add_chips(blackjack_payout)
                        player_chips_change += (blackjack_payout - bet)
                        player_specific_messages.append(f"{hand_label}: Blackjack! Wins ${blackjack_payout - bet}")
                elif hand.value > 21:
                    player_specific_messages.append(f"{hand_label}: Bust! Loses ${bet}")
                    player_chips_change -= bet # Already deducted by place_bet, so this is for summary if needed. Chips are already gone.
                elif is_dealer_blackjack: # Player no BJ, Dealer has BJ
                    player_specific_messages.append(f"{hand_label}: Loses ${bet} (Dealer Blackjack)")
                    player_chips_change -= bet
                elif dealer_busted:
                    player.add_chips(bet * 2)
                    player_chips_change += bet
                    player_specific_messages.append(f"{hand_label}: Wins ${bet} (Dealer Busts)")
                elif hand.value > dealer_value:
                    player.add_chips(bet * 2)
                    player_chips_change += bet
                    player_specific_messages.append(f"{hand_label}: Wins ${bet}")
                elif hand.value < dealer_value:
                    player_specific_messages.append(f"{hand_label}: Loses ${bet}")
                    player_chips_change -= bet
                else: # Push (hand.value == dealer_value, neither has BJ if we reached here, or both non-BJ with same value)
                    player.add_chips(bet)
                    player_specific_messages.append(f"{hand_label}: Push")
            
            if player_specific_messages:
                 round_summary_parts.append(". ".join(player_specific_messages) + f". {player.name} Chips: ${player.chips}")

        self.message = "Round Over: " + " | ".join(round_summary_parts) if round_summary_parts else "Round Over. No bets resolved."
    
    def new_round(self) -> None:
        # reset everything
        self.state = GameState.BETTING
        self.all_bets_placed = False
        self.current_player_index = 0
        for player in self.players:
            player.clear_hands()

        self.dealer.hand.clear()
        if self.players:
            self.message = f"{self.players[0].name}, place your bet!"
        else:
            self.message = "No players to start a new round."
