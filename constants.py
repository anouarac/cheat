import pygame
SLEEP_TIME = 2 # seconds
MAX_CARD_VALUE = 14
CARD_SUITS = ["C","D","H","S"]
CARD_SUITS_LONG = ["clubs", "diamonds", "hearts", "spades"]
MP = {
    0 : "None", 1 : "1", 2 : "2", 3 : "3", 4 : "4", 5 : "5", 6 : "6", 
    7 : "7", 8 : "8", 9 : "9", 10 : "10", 11 : "J", 12 : "Q", 13 : "K"
}

MP_LONG = {
    0 : "None", 1 : "ace", 2 : "2", 3 : "3", 4 : "4", 5 : "5", 6 : "6", 
    7 : "7", 8 : "8", 9 : "9", 10 : "10", 11 : "jack", 12 : "queen", 13 : "king"
}

revMP = {}
for i in range(1, 14):
    revMP[MP[i]] = i

SIZE = WIDTH, HEIGHT = 800, 600
DARK_RED = (139,0,0)
CARD_SIZE = CARD_WITH, CARD_HEIGHT = 83, 120
BACKGROUND = pygame.image.load("./Assets/Fabric.jpg")
BACKGROUND = pygame.transform.scale(BACKGROUND, SIZE)
BACK = pygame.transform.scale(pygame.image.load("./Assets/Cards/back.png"), CARD_SIZE)
CENTER_MID = 70

FILE_OF_CARD = {}
for i in range(1, 14):
    for j in range(4):
        NAME = MP_LONG[i] + "_of_" + CARD_SUITS_LONG[j]
        FILE_OF_CARD[MP[i] + CARD_SUITS[j]] = pygame.transform.scale(pygame.image.load("./Assets/Cards/" + NAME + ".png"), CARD_SIZE)