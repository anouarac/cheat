from mid import Mid
from hand import Hand
from constants import *

class State:
    def __init__(self, nbr_players=6, hands=[], mid=None, turn=0, prev_player=None, text=""):
        self.nbr_players = nbr_players
        self.hands = hands
        self.mid = mid
        self.prev_player = prev_player
        self.ended = False
        self.text = text
        if not hands:
            self.hands = [Hand() for i in range(nbr_players)]
        if not mid:
            self.mid = Mid()
        self.turn = turn
        for i in range(nbr_players):
            self.hands[i].clear_sets()
            self.hands[i].sort()

    def set_text(self, text):
        self.text = text
    
    def end_game(self):
        self.ended = True
        print("Player " + str(self.turn + 1) + " lost.")

    def nbr_players_with_cards_left(self):
        cnt = 0
        for i in range(self.nbr_players):
            if not self.hands[i].empty():
                cnt += 1
        return cnt

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
        output = "Player " + str(self.turn + 1) + " called " + str(len(cards)) + " card"
        if len(cards) > 1:
            output += "s"
        output += " of value " + MP[call]
        print(output)
        self.next_turn()
        return True

    def call_bs(self):
        if self.prev_player == None:
            print("Invalid play")
            return False
        print("Player " + str(self.turn + 1) + " called BS on player " + str(self.prev_player + 1))
        if self.mid.empty() or self.mid.match():
            print("It was not a lie")
            self.mid.show()
            self.hands[self.turn].add_cards(self.mid.hand.cards)
            self.hands[self.turn].arrange()
            self.mid.hand.clear()
            self.next_turn()
            return False
        else:
            print("It was a lie")
            self.mid.show()
            self.hands[self.prev_player].add_cards(self.mid.hand.cards)
            self.hands[self.prev_player].arrange()
            self.mid.hand.clear()
            return True
    
    def __str__(self):
        output = ""
        for i in range(self.nbr_players):
            output += "Player " + str(i + 1) + ": "+ str(self.hands[i])+"\n"
        output += "Middle: " + str(self.mid)
        return output