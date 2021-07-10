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
    def user(self, state):
        inp = input("Your turn: (BS/play/show) ")
        if inp == "show":
            print(state)
        elif inp == "BS":
            state.call_bs()
        else:
            while True:
                strings = list(input("Select your cards: (e.g. 1D 3C KS) ").split(" "))
                selected_cards = Hand()
                for s in strings:
                    card = Card(s[-1], revMP[s[:-1]])
                    selected_cards.add(card)
                call = input("Call: ")
                if state.play(selected_cards.cards, revMP[call]):
                    break
                print("Invalid play")

    # 1 Never lies
    def honest(self, state):
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
    def random(self, state):
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
    def call_lie(self, state):
        player = state.turn
        if state.mid.empty():
            self.random(state)
        else: state.call_bs()

    # 4 Honest with probability self.p, plays randomly otherwise
    def moderate(self, state):
        honest = (np.random.binomial(1, self.p, 1) == [1])
        if honest:
            self.honest(state)
        else: self.random(state)

    def response(self, state):
        if self.type == 0:
            self.user(state)
        elif self.type == 1:
            self.honest(state)
        elif self.type == 2:
            self.random(state)
        elif self.type == 3:
            self.call_lie(state)
        elif self.type == 4:
            self.moderate(state)