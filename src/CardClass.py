import random
from typing import Optional

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