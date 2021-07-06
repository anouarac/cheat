from constants import CARD_TYPES, MAX_CARD_VALUE
import random
from card import Card
from hand import Hand
from game_state import State
from brain import Brain

deck = [Card(c,nb) for nb in range(1,MAX_CARD_VALUE) for c in CARD_TYPES]
random.shuffle(deck)
nbr_players = int(input("Number of players: "))
hands = [Hand() for i in range(nbr_players)]
for i in range(len(deck)):
    hands[i%nbr_players].add(deck[i])

state = State(nbr_players,hands)
print(state)

user, c1, c2, c3 = Brain(1), Brain(1), Brain(1), Brain(1)

while not state.ended:
    if state.turn == 0:
        user.response(state)
    elif state.turn == 1:
        c1.response(state)
    elif state.turn == 2:
        c2.response(state)
    else: c3.response(state)
