from constants import CARD_TYPES, MAX_CARD_VALUE
import random
from card import Card
from hand import Hand
from game_state import State

c1 = Card("D", 8)
c2 = Card("C", 3)
c3 = Card("D", 7)
c4 = Card("C", 7)
c5 = Card("S", 7)
c6 = Card("H", 7)

cards = [Card(c,nb) for nb in range(1,MAX_CARD_VALUE) for c in CARD_TYPES]
random.shuffle(cards)
hands = [Hand() for i in range(4)]
for i in range(len(cards)):
    hands[i%4].add(cards[i])
print(hands[0])
print(hands[1])
state = State(4,hands)

state.play([hands[0].cards[0]],hands[0].cards[0].value)

h = Hand()

print(str(state))

state.call_bs()

print(str(state))