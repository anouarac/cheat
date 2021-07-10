from constants import *
import random
import time
from card import Card
from hand import Hand
from game_state import State
from brain import Brain
from threading import Thread
import sys, pygame
from pygame.locals import *

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

    # Adapting the dimensions of different components depending on the number of players
    global BACK
    hands_height = HEIGHT - 2 * CENTER_MID
    CARD_HEIGHT = min(INIT_CARD_HEIGHT, hands_height // state.nbr_players - VOFFSET)
    CARD_WIDTH = int(CARD_HEIGHT * WIDTH_HEIGHT_RATIO)
    CARD_SIZE = CARD_WIDTH, CARD_HEIGHT
    BACK = pygame.transform.smoothscale(BACK, CARD_SIZE)
    for i in range(1, 14):
        for j in range(4):
            NAME = MP[i] + CARD_SUITS[j]
            FILE_OF_CARD[NAME] = pygame.transform.smoothscale(FILE_OF_CARD[NAME], CARD_SIZE)

    def select(card, mouse_pos, card_pos):
        if mouse_pos != None:
            mouse_x, mouse_y = mouse_pos
            card_x, card_y = card_pos
            if not (mouse_x > card_x + CARD_WIDTH / 2
                    or mouse_x < card_x - CARD_WIDTH / 2
                    or mouse_y > card_y + CARD_HEIGHT / 2
                    or mouse_y < card_y - CARD_HEIGHT / 2):
                card.selected = True

    def display_cards(hand, y):
        sz = hand.size() + 1
        available_w = WIDTH - 2 * HORIZONTAL_MARGIN - CARD_WIDTH 
        i, step = 1, available_w / sz
        init_x = HORIZONTAL_MARGIN + CARD_WIDTH / 2
        for card in hand.cards:
            card_pos = init_x + i * step, y
            select(card, click_pos, card_pos)
            if card.selected == True:
                hx, hy = card_pos[0] - CARD_WIDTH / 2, y - CARD_HEIGHT / 2
                highlight = Rect(hx, hy, CARD_WIDTH, CARD_HEIGHT)
                pygame.draw.rect(SCREEN, YELLOW, highlight, 4)
            card_file = FILE_OF_CARD[str(card)]
            if not hand.public:
                card_file = BACK
            blit_centered(card_file, card_pos, CARD_SIZE)
            i += 1

    def display_hand(ymid):
        w, h = WIDTH - HORIZONTAL_MARGIN * 2, CARD_HEIGHT + VOFFSET / 2
        x, y = HORIZONTAL_MARGIN, ymid - h / 2
        container = Rect(x, y, w, h)
        pygame.draw.rect(SCREEN, BLACK, container, BORDER_WIDTH, BORDER_RADIUS)

    SCREEN.blit(BACKGROUND, (0, 0))

    pygame.display.update()
    while 1:
        click_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == MOUSEBUTTONDOWN: click_pos = event.pos

        SCREEN.blit(BACKGROUND, (0, 0))
        
        display_cards(state.mid.hand, CENTER_MID)
        
        i, step = 0, CARD_HEIGHT + VOFFSET
        height_left = HEIGHT - CENTER_MID * 2 - step * state.nbr_players
        vertical_padding = max(0, height_left / 2)
        init_y = 2 * CENTER_MID + vertical_padding + CARD_HEIGHT / 2
        for k in range(state.nbr_players):
            y_coord = init_y + i * step
            display_hand(y_coord)
            display_cards(state.hands[k], y_coord)
            i += 1
        ARROW_Y = init_y -  ARROW_HEIGHT / 2 + state.turn * step
        ARROW_POS = ARROW_X, ARROW_Y
        SCREEN.blit(ARROW, ARROW_POS)
        pygame.display.update()

# End graphics

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


t1 = Thread(target = update_screen)
t1.start()

t2 = Thread(target = play_game)
t2.start()