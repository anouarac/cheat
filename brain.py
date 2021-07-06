from random import randint
from constants import *
from game_state import State
from mid import Mid
from card import Card
from hand import Hand

class Brain:
    def __init__(self, _type):
        self.type = _type
    
    # User's brain
    def response0(self, state):
        inp = input("Your turn: (BS/play/show) ")
        if inp == "show":
            print(state)
        elif inp == "BS":
            state.call_bs()
        else:
            while True:
                strings = list(input("Select your cards: (e.g. D1 C3 S12) ").split(" "))
                selected_cards = Hand()
                for s in strings:
                    card = Card(s[0], revMP[s[1:]])
                    selected_cards.add(card)
                call = input("Call: ")
                if state.play(selected_cards.cards, revMP[call]):
                    break
                print("Invalid play")

    # Never lies
    def response1(self, state):
        player = state.turn

        if state.mid.empty():
            value = state.hands[player].cards[randint(0, state.hands[player].size()-1)].value
            available = Hand()
            for t in CARD_TYPES:
                card = Card(t, value)
                if card in state.hands[player].cards:
                    available.add(card)
            nbr_called_cards = randint(1, available.size())
            state.play(available.cards[0:nbr_called_cards], value)

        elif state.hands[player].has(state.mid.current_value):
            available = Hand()
            for t in CARD_TYPES:
                card = Card(t, state.mid.current_value)
                if card in state.hands[player].cards:
                    available.add(card)
            nbr_called_cards = randint(1, available.size())
            state.play(available.cards[0:nbr_called_cards], state.mid.current_value)

        else:
            state.call_bs()
    
    def response(self, state):
        if self.type == 0:
            return self.response0(state)
        elif self.type == 1:
            return self.response1(state)