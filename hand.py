from constants import *
from card import Card

class Hand:
    def __init__(self, cards=None):
        self.cards = cards
        if not cards:
            self.cards = []

    def has(self, value):
        for card in self.cards:
            if card.value == value:
                return True
        return False

    # Returns the subset of cards of a certain value from hand
    def cards_of_value(self, value):
        available = Hand()
        for t in CARD_SUITS:
            card = Card(t, value)
            if card in self.cards:
                available.add(card)
        return available

    def add(self, card):
        self.cards.append(card)

    def add_cards(self, cards):
        for card in cards:
            self.add(card)

    def delete(self, card):
        self.cards.remove(card)

    def delete_cards(self, cards):
        for card in cards:
            if not card in self.cards:
                return False
        for card in cards:
            self.delete(card)
        return True
    
    def clear_sets(self):
        counter = [0 for i in range(MAX_CARD_VALUE)]
        for card in self.cards:
            counter[card.value] += 1
        for i in range(1, MAX_CARD_VALUE):
            if counter[i] == 4:
                for c in CARD_SUITS:
                    self.delete(Card(c,i))
    
    def arrange(self):
        self.cards.sort()
        self.clear_sets()
    
    def sort(self):
        self.cards.sort()

    def size(self):
        return len(self.cards)

    def empty(self):
        return not self.cards
    
    def clear(self):
        self.cards = []

    def __str__(self):
        return "[ " + ", ".join([str(card) for card in self.cards]) + " ]"