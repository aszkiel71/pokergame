import random
from backend.card import Card
from backend.hand import Hand



class Deck:

    def __init__(self):
        self.deck = self.generate_full_deck()

    def generate_full_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
        return [Card(suit, rank) for suit in suits for rank in ranks]

    def generate_random_cards(self, n):
        if n > 52:   # Wiadomo. 52 kart w talii
            raise ValueError("You can't draw more cards than there are in the deck (52)")
        return random.sample(self.deck, n)

#deck = Deck()
#random_cards = deck.generate_random_cards(5)
#for card in random_cards:
#    print(card)