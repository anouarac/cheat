import json
import os
import numpy as np
from constants import *
from random import randint, shuffle, uniform
from state import State
from mid import Mid
from card import Card
from hand import Hand

LR = 0.1
gamma = 0.9
cur_nb_players = -1
data = [{} for i in range(7)]
score = [{} for i in range(7)]
occ = [{} for i in range(7)]
best_score = [{} for i in range(7)]
best_move = [{} for i in range(7)]

def qinit():
    if os.path.isfile('../data/qagent.json'):
        with open('../data/qagent.json') as json_file:
            data = json.load(json_file)
        score = data["score"]
        occ = data["occ"]
        best_score = data["best_score"]
        best_move = data["best_move"]

def qget_move(state):
    epsilon = 1
    h = state.qagentparams()
    if h in occ:
        epsilon = 0.999**occ[h]
    a = uniform(0, 1)
    if a <= epsilon:
        idrep, cards, call = None, None, None
        player = state.turn
        mini = 1
        call_bs = (np.random.binomial(1,0.2, 1) == [1])
        nbr_cards_played = randint(mini, state.hands[player].size())
        if call_bs and not state.mid.empty():
            idrep = 1
            return idrep, cards, call
        to_choose = list(range(0, state.hands[player].size()))
        shuffle(to_choose)
        cards = [state.hands[player].cards[to_choose[i]] for i in range(nbr_cards_played)]
        cards = Hand(cards)
        call = randint(1, 13)
        if not state.mid.empty():
            call = state.mid.current_value
        idrep = 2
        return idrep, cards, call
    else:
        [idrep, cards, call] = best_move[h]
        cards = Hand([Card(s[-1], revMP[s[:-1]]) for s in cards])
        return idrep, cards, call 

def qsave(events):
    events.reverse()
    q = 0
    for a in events:
        if not isinstance(a, list):
            q += a
        else:
            cur = a[0]
            trans = a[1]
            x = cur + trans
            if cur in occ:
                occ[cur] += 1
            else: occ[cur] = 1
            if not x in score:
                score[x] = 0
            score[x] += LR * (q - score[x])
            q *= gamma
            if not cur in best_score or score[x] > best_score[cur]:
                best_score[cur] = score[x]
                if a[2][2]:
                    a[2][2] = [str(token) for token in a[2][2]]
                best_move[cur] = a[2]
    data["score"] = score
    data["occ"] = occ
    data["best_score"] = best_score
    data["best_move"] = best_move

def qsavef():
    with open('../data/qagent.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


# less parameters

def qinits(nb_players):
    cur_nb_players = nb_players
    for i in range(7):
        if os.path.isfile('../data/qagents_' + str(i) + '.json'):
            with open('../data/qagents_' + str(i) + '.json') as json_file:
                data[i] = json.load(json_file)
            score[i] = data[i]["score"]
            occ[i] = data[i]["occ"]
            best_score[i] = data[i]["best_score"]
            best_move[i] = data[i]["best_move"]

def qget_moves(state):
    cur_nb_players = state.nbr_players_with_cards_left()
    epsilon = 1
    h = state.qagentparamssmall()
    if h in occ[cur_nb_players]:
        epsilon = 0.999**occ[cur_nb_players][h]
    a = uniform(0, 1)
    if a <= epsilon:
        idrep, cards, call = None, None, None
        player = state.turn
        mini = 1
        call_bs = (np.random.binomial(1,0.2, 1) == [1])
        nbr_cards_played = randint(mini, state.hands[player].size())
        if call_bs and not state.mid.empty():
            idrep = 1
            return idrep, cards, call
        to_choose = list(range(0, state.hands[player].size()))
        shuffle(to_choose)
        cards = [state.hands[player].cards[to_choose[i]] for i in range(nbr_cards_played)]
        cards = Hand(cards)
        call = randint(1, 13)
        if not state.mid.empty():
            call = state.mid.current_value
        idrep = 2
        return idrep, cards, call
    else:
        [idrep, nb_cards] = best_move[cur_nb_players][h]
        if idrep == 1:
            return idrep, None, None
        cur = state.mid.value()
        available = state.hands[state.turn]
        if cur:
            available = state.hands[state.turn].cards_of_value(cur)
        for k in range(nb_cards):
            for value in range(1, MAX_CARD_VALUE):
                if available.cnt_value(value) == nb_cards-k:
                    av = available.cards_of_value(value)
                    cards = Hand([c for c in av.cards][:nb_cards-k])
                    if cur and value != cur:
                        value = cur
                    return idrep, cards, value
        available = state.hands[state.turn]
        nb_cards = max(nb_cards, 1)
        for k in range(nb_cards):
            for value in range(1, MAX_CARD_VALUE):
                if available.cnt_value(value) >= nb_cards-k:
                    av = available.cards_of_value(value)
                    cards = Hand([c for c in av.cards][:nb_cards-k])
                    if cur and value != cur:
                        value = cur
                    return idrep, cards, value

def qsaves(events):
    events.reverse()
    global cur_nb_players
    q = 0
    for a in events:
        if not isinstance(a, list):
            q += a
        else:
            cur = a[0]
            trans = a[1]
            x = cur + trans
            cur_nb_players = int(a[0][0])
            if cur in occ[cur_nb_players]:
                occ[cur_nb_players][cur] += 1
            else: occ[cur_nb_players][cur] = 1
            if not x in score[cur_nb_players]:
                score[cur_nb_players][x] = 0
            score[cur_nb_players][x] += LR * (q - score[cur_nb_players][x])
            q *= gamma
            if not cur in best_score[cur_nb_players] or score[cur_nb_players][x] > best_score[cur_nb_players][cur]:
                best_score[cur_nb_players][cur] = score[cur_nb_players][x]
                best_move[cur_nb_players][cur] = a[2]
    
def qsavefs():
    for i in range(7):
        data[i]["score"] = score[i]
        data[i]["occ"] = occ[i]
        data[i]["best_score"] = best_score[i]
        data[i]["best_move"] = best_move[i]
        with open('../data/qagents_' + str(i) + '.json', 'w') as outfile:
            json.dump(data[i], outfile, indent=4)
