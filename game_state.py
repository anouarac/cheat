from mid import Mid
from hand import Hand

class State:
    def __init__(self, nbr_players, hands=[], mid=None, turn=0, prev_player=-1):
        self.nbr_players = nbr_players
        self.hands = hands
        self.mid = mid
        self.prev_player = prev_player
        if not hands:
            self.hands = [Hand() for i in range(nbr_players)]
        if not mid:
            self.mid = Mid()
        self.turn = turn
        for i in range(nbr_players):
            self.hands[i].clear_sets()

    def end_game(self):
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
            self.mid.hand.clear()
            self.hands[self.turn].clear_sets()
            self.next_turn()
            return False
        else:
            self.hands[self.prev_player].add_cards(self.mid.hand.cards)
            self.hands[self.prev_player].clear_sets()
            self.mid.show()
            self.mid.hand.clear()
            return True
    
    def __str__(self):
        output = ""
        for i in range(self.nbr_players):
            output += "Player " + str(i) + ": "+ str(self.hands[i])+"\n"
        output += "Middle: " + str(self.mid)
        return output