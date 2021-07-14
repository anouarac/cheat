import numpy as np
from random import randint, shuffle
from constants import *
from state import State
from mid import Mid
from card import Card
from hand import Hand

class Player:
    def __init__(self, type=0, probability=0.5):
        self.set_type(type)
        self.set_probability(probability)

    def set_type(self, type):
        self.type = type
    
    def set_probability(self, p):
        self.p = p
        if p > 1 or p < 0:
            self.p = 0.5

    # 0 User input
    def play_user(self, state, resp):
        idrep, cards, call = resp
        player = state.turn
        if idrep == 0:
            print(state.hands[player])
            return True
        elif idrep == 1:
            state.call_bs()
            return True
        else:
            return state.play(cards, call)


    # 1 Never lies
    def play_honest(self, state):
        if state.nbr_players_with_cards_left() == 1:
            state.call_bs()
            return
        player = state.turn

        if state.mid.empty():
            value = state.hands[player].cards[randint(0, state.hands[player].size()-1)].value
            available = state.hands[player].cards_of_value(value)
            nbr_called_cards = randint(1, available.size())
            state.play(available.cards[0:nbr_called_cards], value)

        elif state.hands[player].has(state.mid.current_value):
            available = state.hands[player].cards_of_value(state.mid.current_value)
            nbr_called_cards = randint(1, available.size())
            state.play(available.cards[0:nbr_called_cards], state.mid.current_value)

        else:
            state.call_bs()
        
    # 2 Calls BS with probability self.p if mid is empty,
    # or plays randomly (uniformly distributed decisions where a decision is a pair (cards, call)) 
    def play_random(self, state):
        if state.nbr_players_with_cards_left() == 1:
            state.call_bs()
            return
        player = state.turn
        mini = 1
        call_bs = (np.random.binomial(1, self.p, 1) == [1])
        nbr_cards_played = randint(mini, min(3, state.hands[player].size()))
        if call_bs and not state.mid.empty():
            state.call_bs()
            return
        to_choose = list(range(0, state.hands[player].size()))
        shuffle(to_choose)
        cards = [state.hands[player].cards[to_choose[i]] for i in range(nbr_cards_played)]
        call = state.hands[player].cards[randint(0, state.hands[player].size()-1)].value
        if not state.mid.empty():
            call = state.mid.current_value
        state.play(cards, call)

    # 3 Always calls BS or plays randomly if the middle is empty
    def play_skeptic(self, state):
        player = state.turn
        if state.mid.empty():
            self.play_random(state)
        else: state.call_bs()

    # 4 Honest with probability self.p, plays randomly otherwise
    def play_moderate(self, state):
        honest = (np.random.binomial(1, self.p, 1) == [1])
        if honest:
            self.play_honest(state)
        else: self.play_random(state)

    def response(self, state, resp=None):
        if self.type == 0:
            self.play_user(state, resp)
        elif self.type == 1:
            self.play_honest(state)
        elif self.type == 2:
            self.play_random(state)
        elif self.type == 3:
            self.play_skeptic(state)
        elif self.type == 4:
            self.play_moderate(state)