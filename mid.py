from hand import Hand
from constants import *

class Mid:
    def __init__(self, value=0, hand=None, last_play=None):
        self.current_value = value
        self.hand = hand
        if not hand:
            self.hand = Hand()
        self.last_play = last_play

    def add_cards(self, cards):
        self.last_play = len(cards)
        self.hand.add_cards(cards)

    def show(self):
        print("Showing middle: " + str(self.hand))

    def size(self):
        return self.hand.size()

    def empty(self):
        return self.hand.empty()

    def match(self):
        for i in range(self.last_play):
            if self.hand.cards[-1-i].value != self.current_value:
                return False
        return True
    
    def __str__(self):
        output = str(self.hand)
        output += ", curv = " + MP[self.current_value]
        output += ", last_play = " + str(self.last_play)
        return output