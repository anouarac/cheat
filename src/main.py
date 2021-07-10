from graphics import *
import random
import time
from threading import Thread

deck = [Card(c,nb) for nb in range(1,MAX_CARD_VALUE) for c in CARD_SUITS]
random.shuffle(deck)
nbr_players = int(input("Number of players: "))
hands = [Hand() for i in range(nbr_players)]
for i in range(len(deck)):
    hands[i%nbr_players].add(deck[i])

state = State(nbr_players,hands)
window = Window(state)
print(state)
players = [Player(random.randint(1, 4)) for i in range(nbr_players)]
players[1].set_type(4)
players[0].set_type(1)
if players[0].type == 0:
    state.hands[0].set_privacy(True)
for i in range(nbr_players):
    state.hands[i].set_privacy(True)

def play_game():
    while not state.ended:
        print("Player " + str(state.turn + 1) + "'s turn")
        players[state.turn].response(state)
        time.sleep(SLEEP_TIME)


t1 = Thread(target = window.update_screen)
t1.start()

t2 = Thread(target = play_game)
t2.start()