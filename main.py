from constants import *
import random
import time
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
    def blit_centered(image, coords, sz):
        x, y = coords
        w, h = sz
        x -= w // 2
        y -= h // 2
        SCREEN.blit(image, (x, y))

    def display_cards(hand, y):
        sz = hand.size() + 3
        i, step = 2, WIDTH / sz
        for card in hand.cards:
            card_file = FILE_OF_CARD[str(card)]
            if not hand.public:
                card_file = BACK
            blit_centered(card_file, (i * step, y), CARD_SIZE)
            i += 1

    SCREEN.fill(DARK_RED)
    SCREEN.blit(BACKGROUND, (0, 0))
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        SCREEN.fill(DARK_RED)
        SCREEN.blit(BACKGROUND, (0, 0))
        
        display_cards(state.mid.hand, CENTER_MID)
        
        height_left = HEIGHT - CENTER_MID * 2
        i, step = 1, HEIGHT / (state.nbr_players + 2)
        for k in range(state.nbr_players):
            display_cards(state.hands[k], CENTER_MID * 2 + i * step)
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

brains = [Brain(random.randint(1, 4)) for i in range(nbr_players)]
brains[1].set_type(4)
brains[0].set_type(1)
if brains[0].type == 0:
    state.hands[0].set_privacy(True)
for i in range(nbr_players):
    state.hands[i].set_privacy(True)

def play_game():
    while not state.ended:
        print("Player " + str(state.turn + 1) + "'s turn")
        brains[state.turn].response(state)
        time.sleep(SLEEP_TIME)

t2 = Thread(target = play_game)
t2.start()