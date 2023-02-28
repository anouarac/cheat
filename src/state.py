from types import prepare_class
from mid import Mid
from hand import Hand
from constants import *


class State:
    def __init__(
        self,
        nbr_players=6,
        hands=[],
        mid=None,
        turn=0,
        prev_player=None,
        text="Cheat",
        cur_selected=None,
        played=False,
        call=0,
        events=[],
        out=0,
    ):
        self.nbr_players = nbr_players
        self.hands = hands
        self.mid = mid
        self.prev_player = prev_player
        self.ended = False
        self.text = text
        self.cur_selected = cur_selected
        self.played = played
        self.call = call
        self.events = events
        self.out = out
        if not events:
            self.events = [list() for i in range(nbr_players)]
        if not cur_selected:
            self.cur_selected = Hand()
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
        self.text = "Player " + str(self.turn + 1) + " lost."

    def nbr_players_with_cards_left(self):
        cnt = 0
        for i in range(self.nbr_players):
            if not self.hands[i].empty():
                cnt += 1
        return cnt

    def next_turn(self):
        temp = self.prev_player
        self.prev_player = self.turn
        for card in self.cur_selected.cards:
            card.selected = False
        self.cur_selected = Hand()
        self.turn = (self.turn + 1) % self.nbr_players
        cnt = 0
        while self.hands[self.turn].empty() and cnt <= 6:
            if (
                isinstance(self.events[self.turn][-1], list)
                or self.events[self.turn][-1] < 0.3
            ):
                self.events[self.turn].append(1 - self.out / 10)
                self.out += 1
            self.turn = (self.turn + 1) % self.nbr_players
            cnt += 1
        if cnt > 6:
            self.turn = self.prev_player

        # If no other player has cards left, the game ends
        if self.turn == self.prev_player:
            self.events[self.turn].append(-0.2)
            self.events[temp].append(0.1)
            self.end_game()

    def play(self, cards, call):
        if self.mid.current_value != call and not self.mid.empty():
            self.events[self.turn].append(-1)
            return False
        if not call in range(1, MAX_CARD_VALUE):
            self.events[self.turn].append(-1)
            return False
        if cards.size() == 0:
            return False
        qparam = self.qagentparams()
        qparams = self.qagentparamssmall()
        if not self.hands[self.turn].delete_cards(cards.cards) or not cards:
            self.events[self.turn].append(-1)
            return False
        was_a_lie = not self.mid.empty() and not self.mid.match()
        self.mid.current_value = call
        self.mid.add_cards(cards.cards)
        cnt_call = cards.cnt_value(call)
        # self.events[self.turn].append([qparam, '_2_' + str(call) + '_' + str(hash(cards)), [2, call, cards.cards]])
        self.events[self.turn].append([qparams, "_2_" + str(cnt_call), [2, cnt_call]])
        if was_a_lie:
            self.events[self.turn].append(-0.0001)
            self.events[self.prev_player].append(0.0001)
        output = (
            "Player " + str(self.turn + 1) + " called " + str(cards.size()) + " card"
        )
        if cards.size() > 1:
            output += "s"
        output += " of value " + MP[call]
        self.text = output
        self.next_turn()
        return True

    def call_bs(self):
        if self.prev_player == None or self.mid.empty():
            self.text = "Invalid play"
            self.events[self.turn].append(-1)
            return False
        self.text = (
            "Player "
            + str(self.turn + 1)
            + " called BS on player "
            + str(self.prev_player + 1)
        )
        # self.events[self.turn].append([self.qagentparams(), '_1', (1,None,None)])
        self.events[self.turn].append([self.qagentparamssmall(), "_1", [1, None]])
        if self.mid.empty() or self.mid.match():
            self.text = "It was not a lie"
            self.events[self.turn].append(-0.005 * self.mid.size())
            self.events[self.prev_player].append(0.0025 * self.mid.size())
            self.mid.show()
            self.hands[self.turn].add_cards(self.mid.hand.cards)
            self.hands[self.turn].arrange()
            self.mid.hand.clear()
            self.next_turn()
            self.mid.current_value = None
            self.mid.last_play = None
            return False
        else:
            self.text = "It was a lie"
            self.events[self.turn].append(0.005 * self.mid.size())
            self.events[self.prev_player].append(-0.005 * self.mid.size())
            self.mid.show()
            self.hands[self.prev_player].add_cards(self.mid.hand.cards)
            self.hands[self.prev_player].arrange()
            self.mid.hand.clear()
            self.mid.current_value = None
            self.mid.last_play = None
            return True

    def __str__(self):
        output = ""
        for i in range(self.nbr_players):
            output += "Player " + str(i + 1) + ": " + str(self.hands[i]) + "\n"
        output += "Middle: " + str(self.mid)
        return output

    def qagentparams(self):
        ret = []
        ret.append(self.nbr_players)
        ret.append(self.turn)
        ret.append([self.hands[i].size() for i in range(self.nbr_players)])
        ret.append(self.mid.size())
        ret.append(self.prev_player)
        ret.append(self.call)
        ret.append(self.mid.value())
        ret.append(self.mid.last_play)
        ret.append(hash(self.hands[self.turn]))
        return "_".join([str(elem) for elem in ret])

    def qagentparamssmall(self):
        ret = []
        ret.append(self.nbr_players_with_cards_left())
        ret.append(self.mid.size())
        ret.append(self.mid.last_play)
        if self.prev_player:
            ret.append(self.hands[self.prev_player].size())
        else:
            ret.append(-1)
        ret.append(self.mid.value() != None and self.mid.value() != 0)
        ret.append(self.hands[self.turn].size())
        cnt_call = self.hands[self.turn].cnt_value(self.mid.value())
        ret.append(cnt_call)
        return "_".join([str(elem) for elem in ret])

    def rnnparams(self, public=True):
        ret = []
        ret.append(self.nbr_players)
        ret.append(self.turn)
        for i in range(self.nbr_players):
            ret.append(self.hands[i].size())
        for i in range(6 - self.nbr_players):
            ret.append(0)
        ret.append(self.mid.size())
        ret.append(self.prev_player)
        ret.append(self.call)
        ret.append(self.mid.value())
        ret.append(self.mid.last_play)
        h = hash(self.hands[self.turn])
        if public:
            h = 0
        for i in range(52):
            ret.append(((h >> i) & 1))
        for i in range(len(ret)):
            if ret[i] == None:
                ret[i] = 0
        return ret
