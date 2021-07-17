from constants import *
from card import Card
from hand import Hand
from state import State
from player import Player
import sys, pygame
from pygame.locals import *

class Window:
    def __init__(self, state=None, clicked_bs=False, is_human=False):
        self.state = state
        self.clicked_bs = clicked_bs
        self.is_human = is_human

    def set_state(self, state):
        self.state = state

    def update_screen(self):
        clock = pygame.time.Clock()
        state = self.state
        SCREEN = pygame.display.set_mode(SIZE)
        def blit_centered(image, coords, sz):
            x, y = coords
            w, h = sz
            x -= w // 2
            y -= h // 2
            SCREEN.blit(image, (x, y))

        def button(position, text, selected):
            font = pygame.font.SysFont("profont", 24)
            color = WHITE
            if selected:
                color = BLACK
            text_render = font.render(text, 1, color)
            x, y, w , h = text_render.get_rect()
            x, y = position
            x -= w // 2
            pygame.draw.line(SCREEN, (150, 150, 150), (x, y), (x + w , y), 5)
            pygame.draw.line(SCREEN, (150, 150, 150), (x, y - 2), (x, y + h), 5)
            pygame.draw.line(SCREEN, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
            pygame.draw.line(SCREEN, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
            pygame.draw.rect(SCREEN, (100, 100, 100), (x, y, w , h))
            return SCREEN.blit(text_render, (x, y))

        # Adapting the dimensions of different components depending on the number of players
        global BACK
        hands_height = HEIGHT - 2 * CENTER_MID
        CARD_HEIGHT = min(INIT_CARD_HEIGHT, hands_height // state.nbr_players - VOFFSET)
        CARD_WIDTH = int(CARD_HEIGHT * WIDTH_HEIGHT_RATIO)
        CARD_SIZE = CARD_WIDTH, CARD_HEIGHT
        BACK = pygame.transform.smoothscale(CARD_BACK, CARD_SIZE)
        for i in range(1, 14):
            for j in range(4):
                NAME = MP[i] + CARD_SUITS[j]
                FILE_OF_CARD[NAME] = pygame.transform.smoothscale(FILE_OF_CARD[NAME], CARD_SIZE)

        def select(mouse_pos, card_pos):
            if mouse_pos != None:
                mouse_x, mouse_y = click_pos
                card_x, card_y = card_pos
                to_be_selected = False
                if not (mouse_x > card_x + CARD_WIDTH / 2
                        or mouse_x < card_x - CARD_WIDTH / 2
                        or mouse_y > card_y + CARD_HEIGHT / 2
                        or mouse_y < card_y - CARD_HEIGHT / 2):
                    to_be_selected = True
                return to_be_selected
            return False

        def display_cards(hand, y, is_players_turn, click_pos):
            sz = hand.size() + 1
            available_w = WIDTH - 2 * HORIZONTAL_MARGIN - CARD_WIDTH 
            i, step = 1, available_w / sz
            init_x = HORIZONTAL_MARGIN + CARD_WIDTH / 2

            # Selecting the card the user clicked on
            if is_players_turn:
                last_card_selected = None
                for card in hand.cards:
                    card_pos = init_x + i * step, y
                    init = card.selected
                    if select(click_pos, card_pos):
                        last_card_selected = card
                    card.selected = init
                    i += 1
                if last_card_selected != None:
                    last_card_selected.selected = not last_card_selected.selected
                    if last_card_selected.selected:
                        state.cur_selected.add(last_card_selected)
                    else: state.cur_selected.delete(last_card_selected)
                click_pos = None

            i = 1
            for card in hand.cards:
                select_offset = CARD_HEIGHT * 0.15
                if not card.selected:
                    select_offset = 0
                card_pos = init_x + i * step, y - select_offset
                if card.selected:
                    hx, hy = card_pos[0] - CARD_WIDTH / 2, y - CARD_HEIGHT / 2 - select_offset
                    highlight = Rect(hx, hy, CARD_WIDTH, CARD_HEIGHT)
                    pygame.draw.rect(SCREEN, YELLOW, highlight, 4)
                card_file = FILE_OF_CARD[str(card)]
                if not hand.public:
                    card_file = BACK
                blit_centered(card_file, card_pos, CARD_SIZE)
                i += 1

        def display_hand_border(ymid):
            w, h = WIDTH - HORIZONTAL_MARGIN * 2, CARD_HEIGHT + VOFFSET / 2
            x, y = HORIZONTAL_MARGIN, ymid - h / 2
            container = Rect(x, y, w, h)
            pygame.draw.rect(SCREEN, BLACK, container, BORDER_WIDTH, BORDER_RADIUS)

        pygame.display.set_caption('Cheat')
        pygame.display.set_icon(ICON)

        # Hardcoded coords shitcode
        pos_mid = CARD_HEIGHT * .8
        text_offset = 0
        play_offset = 20
        bs_offset = 0
        if state.nbr_players < 4:
            pos_mid -= CARD_HEIGHT * .2
            text_offset += 20
            bs_offset = 20
        if state.nbr_players == 4:
            pos_mid -= CARD_HEIGHT * .25
            text_offset += 10
            play_offset = 0
            bs_offset = 10
        if state.nbr_players >= 5:
            play_offset = -10
            bs_offset = 10
        
        play_button, bs_button, call_buttons = None, None, None

        while 1:
            clock.tick(60)
            SCREEN.blit(BACKGROUND, (0, 0))
            click_pos = None
            state = self.state
            if self.is_human:
                play_button = button((WIDTH * 0.9, CENTER_MID * 1.5 + play_offset), "Play", False)
                bs_button = button((WIDTH * 0.9, CENTER_MID * 1.5 + text_offset + bs_offset), "Call BS", False)
                call_buttons = [button((35 + (i - 1) * 20, CENTER_MID * 1.5 + text_offset * 1.5), MP[i], (state.call==i)) for i in range(1, MAX_CARD_VALUE)]
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    click_pos = event.pos
                    if self.is_human and play_button.collidepoint(click_pos) and (state.call != None or state.mid.current_value != None):
                        self.clicked_bs = False
                        state.played = True
                        if state.call == None:
                            state.call = state.mid.current_value
                    elif self.is_human and bs_button.collidepoint(click_pos):
                        self.clicked_bs = True
                        state.played = True
                    sz = 0
                    if call_buttons != None:
                        sz = len(call_buttons)
                    for i in range(sz):
                        butt = call_buttons[i]
                        if butt.collidepoint(click_pos):
                            state.call = i + 1

            display_cards(state.mid.hand, pos_mid, False, None)
            
            i, step = 0, CARD_HEIGHT + VOFFSET
            height_left = HEIGHT - CENTER_MID * 2 - step * state.nbr_players
            vertical_padding = max(0, height_left / 2)
            init_y = 2 * CENTER_MID + vertical_padding + CARD_HEIGHT / 2
            
            for k in range(state.nbr_players):
                y_coord = init_y + i * step
                display_hand_border(y_coord)
                display_cards(state.hands[k], y_coord, state.turn == k, click_pos)
                i += 1

            ARROW_Y = init_y -  ARROW_HEIGHT / 2 + state.turn * step
            ARROW_POS = ARROW_X, ARROW_Y
            SCREEN.blit(ARROW, ARROW_POS)
            text = SMALLFONT.render(state.text , True , WHITE)
            blit_centered(text, (WIDTH / 2, CENTER_MID * 2 - text.get_height() / 2 + text_offset), (text.get_width(), text.get_height()))
            font = pygame.font.SysFont("timesnewroman", 14)
            text = font.render("Table's value: " + MP[state.mid.current_value], True , WHITE)
            SCREEN.blit(text, (0, 0))
            play_button, bs_button, call_buttons = None, None, None
            pygame.display.update()
