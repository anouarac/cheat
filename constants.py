import pygame
MAX_CARD_VALUE = 14
CARD_SUITS = ["C","D","H","S"]
MP = {
    0 : "None",
    1 : "1",
    2 : "2",
    3 : "3",
    4 : "4",
    5 : "5",
    6 : "6",
    7 : "7",
    8 : "8",
    9 : "9",
    10 : "10",
    11 : "J",
    12 : "Q",
    13 : "K"
}

revMP = {}
for i in range(1,14):
    revMP[MP[i]] = i

SIZE = 800, 600
DARK_RED = (139,0,0)

BACK = pygame.transform.scale(pygame.image.load("./Assets/Cards/back.png"), (100, 160))