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
players[0].set_type(0)
if players[0].type == 0:
    state.hands[0].set_privacy(True)
for i in range(nbr_players):
    state.hands[i].set_privacy(True)

def play_game():
    while not state.ended:
        print("Player " + str(state.turn + 1) + "'s turn")
        idrep = 0
        selected_cards, call = Hand(), None
        if players[state.turn].type == 0:
            inp = input("Your turn: (BS/play/show) ")
            if inp == "show":
                idrep = 0
            elif inp == "BS":
                idrep = 1
            else:
                idrep = 2
                strings = list(input("Select your cards: (e.g. 1D 3C KS) ").split(" "))
                for s in strings:
                    card = Card(s[-1], revMP[s[:-1]])
                    selected_cards.add(card)
                call = revMP[input("Call: ")]
        resp = idrep, selected_cards.cards, call
        is_human = players[state.turn].type == 0
        if not players[state.turn].response(state, resp) and is_human:
            print("Invalid play")
        time.sleep(SLEEP_TIME)


t1 = Thread(target = window.update_screen)
t1.start()

play_game()
