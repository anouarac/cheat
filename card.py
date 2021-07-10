from constants import *

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.selected = False
        

    def __str__(self):
        return MP[self.value] + self.suit

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        if self.value != other.value:
            return self.value < other.value
        return self.suit < other.suit

    #TODO: define getters and setters