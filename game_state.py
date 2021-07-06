from mid import Mid
from hand import Hand
from constants import *

class State:
    def __init__(self, nbr_players, hands=[], mid=None, turn=0, prev_player=None):
        self.nbr_players = nbr_players
        self.hands = hands
        self.mid = mid
        self.prev_player = prev_player
        self.ended = False
        if not hands:
            self.hands = [Hand() for i in range(nbr_players)]
        if not mid:
            self.mid = Mid()
        self.turn = turn
        for i in range(nbr_players):
            self.hands[i].clear_sets()
            self.hands[i].sort()

    def end_game(self):
        self.ended = True
        print("Player " + str(self.turn) + " lost.")

    def next_turn(self):
        self.prev_player = self.turn
        self.turn = (self.turn + 1) % self.nbr_players
        cnt = 0
        while self.hands[self.turn].empty() and cnt <= 6:
            self.turn = (self.turn + 1) % self.nbr_players
            cnt += 1
        if cnt > 6:
            self.turn = self.prev_player
        
        # If no other player has cards left, the game ends
        if self.turn == self.prev_player:
            self.end_game()

    def play(self, cards, call):
        if self.mid.current_value != call and not self.mid.empty():
            return False
        self.mid.current_value = call
        self.mid.add_cards(cards)
        if not self.hands[self.turn].delete_cards(cards):
            return False
        self.next_turn()
        if self.ended:
            return True
        
        output = "Player " + str(self.turn) + " called " + str(len(cards)) + " card"
        if len(cards) > 1:
            output += "s"
        output += " of value " + MP[call]
        print(output)

        return True

    def call_bs(self):
        print("Player " + str(self.turn) + " called BS on player " + str(self.prev_player))
        if self.mid.empty() or self.mid.match():
            print("It was not a lie")
            self.hands[self.turn].add_cards(self.mid.hand.cards)
            self.hands[self.turn].arrange()
            self.mid.show()
            self.mid.hand.clear()
            self.next_turn()
            return False
        else:
            print("It was a lie")
            self.hands[self.prev_player].add_cards(self.mid.hand.cards)
            self.hands[self.prev_player].arrange()
            self.mid.show()
            self.mid.hand.clear()
            return True
    
    def __str__(self):
        output = ""
        for i in range(self.nbr_players):
            output += "Player " + str(i) + ": "+ str(self.hands[i])+"\n"
        output += "Middle: " + str(self.mid)
        return output