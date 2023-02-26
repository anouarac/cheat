import torch
import torch.nn as nn
import random
import os
import numpy as np
from copy import deepcopy
from hand import Hand
from state import State
from mid import Mid
from card import Card
from constants import *
from player import Player

MAX_MOVES = 50


class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()
        self.lstm1 = nn.LSTM(input_size, hidden_size).double()
        self.lstm2 = nn.LSTM(hidden_size, hidden_size).double()
        self.fc = nn.Linear(hidden_size, output_size).double()
        self.relu = nn.ReLU()

    def forward(self, x):
        out, _ = self.lstm1(x)
        out, _ = self.lstm2(out)
        out = self.fc(self.relu(out))
        return out

    def predict_move(self, state):
        features = state.rnnparams()
        X = torch.tensor(features, dtype=torch.float64).unsqueeze(0)
        with torch.no_grad():
            lstm_output = self.forward(X)
            _, predicted = torch.max(lstm_output.data[:3], 1)
        return predicted, lstm_output


def encode_params(model):
    genes = []
    for param in model.parameters():
        genes.extend(param.detach().numpy().flatten().tolist())
    return genes


def decode_params(model, genes):
    idx = 0
    for param in model.parameters():
        size = param.detach().numpy().shape
        if len(size) < 2:
            continue
        gene_array = np.array(genes[idx : idx + size[0] * size[1]])
        gene_array = gene_array.reshape(size)
        param.data.copy_(torch.from_numpy(gene_array))
        idx += size[0] * size[1]


def mutate_genes(genes, mutation_rate, mutation_sigma):
    for i in range(len(genes)):
        if random.random() < mutation_rate:
            genes[i] += random.gauss(0, mutation_sigma)


def crossover_genes(genes1, genes2):
    crossover_point = random.randint(0, len(genes1))
    return genes1[:crossover_point] + genes2[crossover_point:]


def create_individual(input_size, hidden_size, output_size):
    model = RNN(input_size, hidden_size, output_size)
    genes = encode_params(model)
    return (model, genes)


def create_population(
    population_size, input_size, hidden_size, output_size, best_model=None
):
    population = []
    if best_model != None:
        best_genes = encode_params(best_model)
        return [
            (deepcopy(best_model), deepcopy(best_genes)) for i in range(population_size)
        ]
    for i in range(population_size):
        population.append(create_individual(input_size, hidden_size, output_size))
    return population


def play_game(players):
    nbr_players = len(players)
    deck = [Card(c, nb) for nb in range(1, MAX_CARD_VALUE) for c in CARD_SUITS]
    random.shuffle(deck)
    hands = [Hand() for i in range(nbr_players)]
    for i in range(len(deck)):
        hands[i % nbr_players].add(deck[i])
    state = State(nbr_players, hands)
    score = [0 for i in range(nbr_players)]
    win_score = 256
    moves = 0
    while not state.ended and moves < MAX_MOVES:
        moves += 1
        state.text = "Player " + str(state.turn + 1) + "'s turn"
        idrep = 0
        selected_cards, call = Hand(), None

        cur_player = state.turn
        resp = idrep, selected_cards, call
        if not players[state.turn].response(state, resp):
            state.text = "Invalid play"
            # print(state.text)
            score[cur_player] -= 5
        elif state.mid.last_play != None and state.mid.last_play > 0:
            score[cur_player] += 5
        state.played = False
        state.call = None
        for card in state.cur_selected.cards:
            card.selected = False
        state.cur_selected = Hand()
        for player in players:
            player.register_move(state)
        if state.hands[cur_player].empty():
            score[cur_player] += win_score
            win_score = win_score // 2
    return score


def genetic_algorithm(
    population_size,
    input_size,
    hidden_size,
    output_size,
    mutation_rate,
    mutation_sigma,
    num_generations,
    best_model=None,
):
    population = create_population(
        population_size, input_size, hidden_size, output_size, best_model
    )
    for generation in range(num_generations):
        fitness_scores = [[i, 0] for i in range(population_size)]
        for i in range(200):
            players = [
                random.randint(0, population_size - 1)
                for k in range(random.randint(2, 6))
            ]
            nb_players = len(players)
            game_players = [Player(6) for i in range(nb_players)]
            for i in range(nb_players):
                game_players[i].set_rnn(population[players[i]][0])
            scores = play_game(game_players)
            for i in range(nb_players):
                fitness_scores[players[i]][1] += scores[i]

        fitness_scores.sort(key=lambda x: x[1], reverse=True)

        print("Generation", generation + 1, "best fitness:", fitness_scores[0][1])

        top_performers = [
            population[i] for i, _ in fitness_scores[: population_size // 2]
        ]

        new_population = top_performers[:]
        while len(new_population) < population_size:
            parent1 = random.choice(top_performers)
            parent2 = random.choice(top_performers)

            child_genes = crossover_genes(parent1[1], parent2[1])
            mutate_genes(child_genes, mutation_rate, mutation_sigma)

            child_model = RNN(input_size, hidden_size, output_size)
            decode_params(child_model, child_genes)
            new_population.append((child_model, child_genes))

        population = new_population

    return population[0][0], population[0][1]


input_size = 14
hidden_size = 20
output_size = 20
population_size = 50
mutation_rate = 0.1
mutation_sigma = 0.1
num_generations = 20


def train_rnn():

    best_model = RNN(input_size, hidden_size, output_size)
    if os.path.isfile("../data/best_model.pt"):
        best_model.load_state_dict(torch.load("../data/best_model.pt"))
        best_model, best_genes = genetic_algorithm(
            population_size,
            input_size,
            hidden_size,
            output_size,
            mutation_rate,
            mutation_sigma,
            num_generations,
            best_model,
        )
    else:
        best_model, best_genes = genetic_algorithm(
            population_size,
            input_size,
            hidden_size,
            output_size,
            mutation_rate,
            mutation_sigma,
            num_generations,
        )
    torch.save(best_model.state_dict(), "../data/best_model.pt")
