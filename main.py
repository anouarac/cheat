from constants import *
import random
from card import Card
from hand import Hand
from game_state import State
from brain import Brain

deck = [Card(c,nb) for nb in range(1,MAX_CARD_VALUE) for c in CARD_SUITS]
random.shuffle(deck)
nbr_players = int(input("Number of players: "))
hands = [Hand() for i in range(nbr_players)]
for i in range(len(deck)):
    hands[i%nbr_players].add(deck[i])

state = State(nbr_players,hands)
print(state)

brains = [Brain() for i in range(nbr_players)]
brains[1].set_type(4)
brains[0].set_type(0)

while not state.ended:
    brains[state.turn].response(state)
