from constants import CARD_TYPES, MAX_CARD_VALUE
from card import Card

class Hand:
    def __init__(self, cards=None):
        self.cards = cards
        if not cards:
            self.cards = []

    def add(self, card):
        self.cards.append(card)

    def add_cards(self, cards):
        for card in cards:
            self.add(card)

    def delete(self, card):
        self.cards.remove(card)

    def delete_cards(self, cards):
        for card in cards:
            self.delete(card)
    
    def clear_sets(self):
        counter = [0 for i in range(MAX_CARD_VALUE)]
        for card in self.cards:
            counter[card.value] += 1
        for i in range(1, MAX_CARD_VALUE):
            if counter[i] == 4:
                for c in CARD_TYPES:
                    self.delete(Card(c,i))

    def size(self):
        return len(self.cards)

    def empty(self):
        return not self.cards
    
    def clear(self):
        self.cards = []

    def __str__(self):
        return "[ " + ", ".join([str(card) for card in self.cards]) + " ]"