from constants import *
import random
from card import Card
from hand import Hand
from game_state import State
from brain import Brain
from threading import Thread
import sys, pygame

state = State()

# Graphics

def update_screen():
    SCREEN = pygame.display.set_mode(SIZE)
    BACKGROUND = pygame.image.load("./Assets/Fabric0.jpg")
    BACKGROUND = pygame.transform.scale(BACKGROUND, SIZE)
    SCREEN.fill(DARK_RED)
    SCREEN.blit(BACKGROUND, (0, 0))
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        SCREEN.fill(DARK_RED)
        SCREEN.blit(BACKGROUND, (0, 0))
        sz = state.mid.size() + 1
        i, step = 1, 600 / sz
        for card in state.mid.hand.cards:
            SCREEN.blit(BACK, (i*step, 200))
            i += 1
        pygame.display.update()

# End graphics

t1 = Thread(target = update_screen)
t1.start()

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

def play_game():
    while not state.ended:
        print("Player " + str(state.turn + 1) + "'s turn")
        brains[state.turn].response(state)

t2 = Thread(target = play_game)
t2.start()