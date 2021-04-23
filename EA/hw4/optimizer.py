#!/usr/bin python3.6
from functools import reduce
from operator import add
import random
from network import Network
import network as nk
import copy
import numpy as np


class Optimizer():
    """Class that implements genetic algorithm for MLP optimization."""

    def __init__(self, bit_len, population_size):
        """Create an optimizer"""
        self.population_size = population_size
        self.mutate_rate = 0.01
        self.crossover_rate = 0.5
        self.bit_len = bit_len
        self.nn_param_choices = nk.get_nn_param_dict()

    def create_population(self):
        """Create a population of random networks"""
        pop = []
        for _ in range(0, self.population_size):
            # Create a random network.
            network = Network()
            network.create_random()

            # Add the network to our population.
            pop.append(network)

        return pop

    @staticmethod
    def fitness(network):
        """Return the accuracy, which is our fitness function."""
        return network.accuracy

    def mutate(self, population):
        """Randomly mutate one part of the network"""
        # support function mutate one
        def mutate_one(network):
            network_param_bin = network.get_param()
            new_network_param_bin = copy.deepcopy(network_param_bin)

            for i in range(len(network_param_bin)):
                if np.random.rand() < self.mutate_rate:
                    new_network_param_bin[i] = 1 - network_param_bin[i]

            new_network = Network(new_network_param_bin)
            return new_network

        new_population = []
        for p in range(self.population_size):
            network = population[p]
            new_network = mutate_one(network)
            new_population.append(new_network)

        return new_population

    def crossover(self, parents):
        def crossover_one_pair(pa, pb):
            bit_len = self.bit_len
            c_point = np.random.randint(bit_len)

            pa_param_bin = pa.get_param()
            pb_param_bin = pb.get_param()

            childa_val = np.zeros(shape=pa_param_bin.shape)
            childb_val = np.zeros(shape=pa_param_bin.shape)

            childa_val[:c_point] = pa_param_bin[:c_point]
            childa_val[c_point:] = pb_param_bin[c_point:]

            childb_val[:c_point] = pb_param_bin[:c_point]
            childb_val[c_point:] = pa_param_bin[c_point:]

            childa_network = Network(childa_val)
            childb_network = Network(childb_val)

            offsprings = [childa_network, childb_network]
            return offsprings

        count = 0
        children_pool = []
        while count < self.population_size:
            mates = np.random.choice(parents)
            parent_a, parent_b = mates
            if np.random.rand() < self.crossover_rate:
                childs = crossover_one_pair(parent_a, parent_b)
            else:
                childs = [copy.deepcopy(parent_a), copy.deepcopy(parent_b)]
            children_pool.extend(childs)
            count += 2
        next_generation = children_pool[:self.population_size]
        return next_generation

    def select(self, proportional_list, population):
        population_size = self.population_size
        chosen = []
        for n in range(population_size):
            r = random.random()
            for (i, individual) in enumerate(population):
                if r <= proportional_list[i]:
                    chosen.append(copy.deepcopy(individual))
                    break
        return chosen

    def evolve(self, population, proportional_list):
        """Evolve a population of networks"""
        # select
        parents = self.select(proportional_list, population)

        # crossover
        offsprings = self.crossover(parents)

        # mutation
        population = self.mutate(offsprings)

        return parents
