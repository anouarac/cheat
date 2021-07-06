from constants import *
class Card:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

    def __str__(self):
        return self.type + MP[self.value]

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        if self.value != other.value:
            return self.value < other.value
        return self.type < other.type

    #TODO: define getters and setters