from graphics import *
import random
from qagent import *
import time, matplotlib.pyplot
from threading import Thread

MODE = int(input("Mode: (0: terminal, 1: UI) "))
TRAIN_MODE = input("Train mode: (y/n) ")[0] == "y"
iterations,cur = 1,1
if TRAIN_MODE:
    iterations = int(input("Number of games: "))

qinits(6)

while cur <= iterations:
    if cur%10 == 0 or cur == 1:
        print("Game number " + str(cur))
    cur += 1
    if not TRAIN_MODE:
    	nbr_players = int(input("Number of players: "))
    else: nbr_players = randint(2,6)
    deck = [Card(c,nb) for nb in range(1,MAX_CARD_VALUE) for c in CARD_SUITS]
    random.shuffle(deck)
    hands = [Hand() for i in range(nbr_players)]
    for i in range(len(deck)):
        hands[i%nbr_players].add(deck[i])
    state = State(nbr_players,hands)
    window = Window(state)
    players = [Player(random.randint(5, 5)) for i in range(nbr_players)]
    if TRAIN_MODE:
        for i in range(nbr_players//2):
            players[randint(0,nbr_players-1)] = Player(randint(5,5))
    else:
        players[randint(0,nbr_players-1)] = Player(0)
    # players[1].set_type(4)
    # players[0].set_type(0)
    for i in range(nbr_players):
        if players[i].type == 0:
            state.hands[i].set_privacy(True)

    def play_game():
        while not state.ended:
            state.text = "Player " + str(state.turn + 1) + "'s turn"
            if MODE == 0 and not TRAIN_MODE:
                print(state.text)
            idrep = 0
            selected_cards, call = Hand(), None
            if players[state.turn].type == 0 and MODE == 0:
                window.is_human = True
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
            elif players[state.turn].type == 0:
                window.is_human = True
                while not state.played:
                    pass
                selected_cards = state.cur_selected
                call = state.call
                if window.clicked_bs:
                    idrep = 1
                else: idrep = 2
            
            if players[state.turn].type == 5:
                idrep, selected_cards, call = qget_moves(state)
            
            resp = idrep, selected_cards, call
            is_human = players[state.turn].type == 0
            if not players[state.turn].response(state, resp) and is_human:
                if MODE == 0 and not TRAIN_MODE:
                    print(state.text)
                state.text = "Invalid play"
                if MODE == 0 and not TRAIN_MODE:
                    print(state.text)
            elif MODE == 0 and not TRAIN_MODE:
                print(state.text)
            state.played = False
            window.is_human = False
            state.call = None
            for card in state.cur_selected.cards:
                card.selected = False
            state.cur_selected = Hand()
        #     time.sleep(SLEEP_TIME)
        # time.sleep(5)
        for i in range(nbr_players):
            qsaves(state.events[i])


   # t1 = Thread(target = window.update_screen)
   # if MODE == 1:
   #     t1.start()
	
   # play_game()
    t1 = Thread(target = play_game)
    t1.start()

    if MODE == 1:
        window.update_screen()
    if cur%5000 == 0:
        qsavefs()
