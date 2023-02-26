import numpy as np
import torch
from random import randint, shuffle
from constants import *
from state import State
from mid import Mid
from card import Card
from hand import Hand


class Player:
    def __init__(self, type=0, probability=0.5):
        self.set_type(type)
        self.set_probability(probability)

    def set_type(self, type):
        self.type = type

    def set_probability(self, p):
        self.p = p
        if p > 1 or p < 0:
            self.p = 0.5

    def set_rnn(self, model=None):
        self.model = model

    def register_move(self, state):
        if self.type == 6:
            self.model.predict_move(state)

    # 0 User input
    def play_user(self, state, resp):
        idrep, cards, call = resp
        player = state.turn
        if idrep == 0:
            print(state.hands[player])
            return True
        elif idrep == 1:
            state.call_bs()
            return True
        else:
            return state.play(cards, call)

    # 1 Never lies
    def play_honest(self, state):
        if state.mid.last_play != None and state.mid.last_play > 3:
            state.call_bs()
            return
        if state.nbr_players_with_cards_left() == 1:
            state.call_bs()
            return
        player = state.turn

        if state.mid.empty():
            value = (
                state.hands[player]
                .cards[randint(0, state.hands[player].size() - 1)]
                .value
            )
            available = state.hands[player].cards_of_value(value)
            nbr_called_cards = randint(1, available.size())
            state.play(Hand(available.cards[0:nbr_called_cards]), value)

        elif state.hands[player].has(state.mid.current_value):
            available = state.hands[player].cards_of_value(state.mid.current_value)
            nbr_called_cards = randint(1, available.size())
            state.play(
                Hand(available.cards[0:nbr_called_cards]), state.mid.current_value
            )

        else:
            state.call_bs()

    # 2 Calls BS with probability self.p if mid is empty,
    # or plays randomly (uniformly distributed decisions where a decision is a pair (cards, call))
    def play_random(self, state):
        if state.mid.last_play != None and state.mid.last_play > 3:
            state.call_bs()
            return
        if state.nbr_players_with_cards_left() == 1:
            state.call_bs()
            return
        player = state.turn
        mini = 1
        call_bs = np.random.binomial(1, self.p, 1) == [1]
        nbr_cards_played = randint(mini, min(3, state.hands[player].size()))
        if call_bs and not state.mid.empty():
            state.call_bs()
            return
        to_choose = list(range(0, state.hands[player].size()))
        shuffle(to_choose)
        cards = [
            state.hands[player].cards[to_choose[i]] for i in range(nbr_cards_played)
        ]
        call = (
            state.hands[player].cards[randint(0, state.hands[player].size() - 1)].value
        )
        if not state.mid.empty():
            call = state.mid.current_value
        state.play(Hand(cards), call)

    # 3 Always calls BS or plays randomly if the middle is empty
    def play_skeptic(self, state):
        if state.mid.empty():
            self.play_random(state)
        else:
            state.call_bs()

    # 4 Honest with probability self.p, plays randomly otherwise
    def play_moderate(self, state):
        if state.mid.last_play != None and state.mid.last_play > 3:
            state.call_bs()
            return
        honest = np.random.binomial(1, self.p, 1) == [1]
        if honest:
            self.play_honest(state)
        else:
            self.play_random(state)

    def get_num_cards_to_play(self, lstm_output):
        # get the number of cards to play from the LSTM output
        num_cards = int(lstm_output[0][0])

        # make sure the number of cards is within the allowed range
        if num_cards < 1:
            num_cards = 1
        elif num_cards > self.hands[self.turn].size():
            num_cards = self.hands[self.turn].size()

        return num_cards

    def get_card_indices_to_play(self, lstm_output):
        # get the indices of the cards to play from the LSTM output
        card_indices = []
        for i in range(len(lstm_output[0][1:])):
            if (
                lstm_output[0][1:][i] > 0.5
            ):  # use a threshold of 0.5 to determine which cards to play
                card_indices.append(i)

        # make sure at least one card is played
        if len(card_indices) == 0:
            card_indices.append(0)

        return card_indices

    def choose_card_value(self, output):
        return int(output[-1][-1])

    # 5 RNN
    def play_rnn(self, state):
        predicted, lstm_output = self.model.predict_move(state)
        if predicted == 0:
            return state.call_bs()
        elif predicted == 1:
            num_cards = self.get_num_cards_to_play(lstm_output)
            card_indices = self.get_card_indices_to_play(lstm_output)
            card_value = self.choose_card_value(lstm_output)
            if not state.mid.empty():
                card_value = state.mid.current_value
            player = state.turn
            cards = [
                state.hands[player].cards[card_indices[i]] for i in range(num_cards)
            ]
            return state.play(Hand(cards), card_value)
        else:
            self.play_honest(state)
            return True

    def response(self, state, resp=None):
        if self.type == 0:
            return self.play_user(state, resp)
        elif self.type == 1:
            self.play_honest(state)
        elif self.type == 2:
            self.play_random(state)
        elif self.type == 3:
            self.play_skeptic(state)
        elif self.type == 4:
            self.play_moderate(state)
        elif self.type == 5:  # Q-agent
            return self.play_user(state, resp)
        elif self.type == 6:  # RNN
            return self.play_rnn(state)
        return True
