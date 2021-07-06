from mid import Mid
from hand import Hand

class State:
    def __init__(self, nbr_players, hands=[], mid=None, turn=0):
        self.nbr_players = nbr_players
        self.hands = hands
        self.mid = mid
        if not hands:
            self.hands = [Hand() for i in range(nbr_players)]
        if not mid:
            self.mid = Mid()
        self.turn = turn

    def next_turn(self):
        self.turn = (self.turn + 1) % self.nbr_players

    def play(self, cards, call):
        if self.mid.current_value != call and not self.mid.empty():
            return -1
        self.mid.current_value = call
        self.mid.add_cards(cards)
        self.hands[self.turn].delete_cards(cards)
        self.next_turn()
        return 0

    def call_bs(self):
        if self.mid.match():
            self.hands[self.turn].add_cards(self.mid.hand.cards)
            self.mid.show()
            self.mid.hand.cards = []
            self.next_turn()
            return False
        else:
            prev_player = (self.turn - 1) % self.nbr_players
            self.hands[prev_player].add_cards(self.mid.hand.cards)
            self.mid.show()
            self.mid.hand.cards = []
            return True
    
    def __str__(self):
        output = ""
        for i in range(self.nbr_players):
            output += "Player " + str(i) + ": "+ str(self.hands[i])+"\n"
        output += "Middle: " + str(self.mid)
        return output
