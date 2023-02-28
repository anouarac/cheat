import pygame
import sys

pygame.init()
SLEEP_TIME = 2  # seconds
MAX_CARD_VALUE = 14
CARD_SUITS = ["C", "D", "H", "S"]
CARD_SUITS_LONG = ["clubs", "diamonds", "hearts", "spades"]
MP = {
    None: "None",
    0: "None",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "J",
    12: "Q",
    13: "K",
}

MP_LONG = {
    0: "None",
    1: "ace",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "jack",
    12: "queen",
    13: "king",
}

revMP = {"A": 1}
for i in range(1, 14):
    revMP[MP[i]] = i

ASSETS_DIR = "../assets/"
SIZE = WIDTH, HEIGHT = 1024, 660
DARK_RED = (139, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
CARD_SIZE = INIT_CARD_WIDTH, INIT_CARD_HEIGHT = 69, 100
WIDTH_HEIGHT_RATIO = 500 / 726
HORIZONTAL_MARGIN = 30
BACKGROUND = pygame.image.load(ASSETS_DIR + "fabric.jpg")
BACKGROUND = pygame.transform.smoothscale(BACKGROUND, SIZE)
ICON = pygame.image.load(ASSETS_DIR + "cards/king_of_spades.png")
CARD_BACK = pygame.image.load(ASSETS_DIR + "cards/back.png")
ARROW_SIZE = ARROW_WIDTH, ARROW_HEIGHT = (25, 15)
ARROW = pygame.transform.scale(pygame.image.load(ASSETS_DIR + "arrow.png"), ARROW_SIZE)
ARROW_POS = ARROW_X, ARROW_Y = 4, None
VOFFSET = 25
CENTER_MID = 70
click_pos = None
BORDER_WIDTH = 3
BORDER_RADIUS = 3
SMALLFONT = pygame.font.SysFont("timesnewroman", 35)

FILE_OF_CARD = {}
for i in range(1, 14):
    for j in range(4):
        NAME = MP_LONG[i] + "_of_" + CARD_SUITS_LONG[j]
        FILE_OF_CARD[MP[i] + CARD_SUITS[j]] = pygame.image.load(
            ASSETS_DIR + "cards/" + NAME + ".png"
        )
