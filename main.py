from card import Card
from hand import Hand
from game_state import State

c1 = Card("D", 8)
c2 = Card("C", 3)
c3 = Card("D", 7)
c4 = Card("C", 7)
c5 = Card("S", 7)
c6 = Card("H", 7)
state = State(2,[Hand([c1,c3,c4,c5,c6]),Hand([c2])])

print(state.hands[0])
state.hands[0].clear_sets()
state.play([c1],3)

h = Hand()

print(str(state))

state.play([c2],3)

state.call_bs()

print(str(state))