#!/usr/bin/python3

import os
import sys
import argparse
import pdb

import random
import math
import numpy as np
import copy

import CGAComponents

'''
Canonical Genetic Algorithm (CGA)
Representation:     Fixed-length bit string
Population:         Fixed-size
Initialization:     Random drawn from linear probability distributions
Parent Selection:   Roulette Wheel Selection (Fitneww Proportional)
Crossover:          Single-Point Crossover. CGA generally uses large crossover rates
Mutation:           Bitwise (each bit has a probability of flipping its state). CGA generally uses small mutation rates
Survivor Selection: Everyone passes this. ALL SELECTION is done in the parent selection phase in CGA
Termination:        Various, but most often convergence of the bitstrings. When ALL genomes in the population become
                    identical, or when some defined large number of them do, then you consider the population "converged"
                    and stop the process. For our purposes, use genome convergence combined with a fixed stopping point.
                    Really, for harder problems you may not actually see "hard convergence".

Output specific:
    When your code runs, it should print out a "one time" header that contains this info:
        <problem name> <population size> <bitstring genome length> <mutation rate> <crossover rate>

    After that initial line, for every generation that is completed, you should print an additional line that contains
    this info:
        <generation number> <fitness score of the most fit member of the population> <average fitness score>
        <precent of genomes in population that are identical>

    When your algorithm terminates, you should print a final line that gives the reason for termination, which should be
    either the population has converged OR you went over some finite "safty limit" that bounded how many generations you
    were willing to run.

Max One Problem:
    let's create a toy evolutionary algorithm where we want to evolve a population of individuals
    (where each individual is a list of N integer numbers) until one of them is exactly comprised
    of N ones (i.e. 1,1,....,1).
'''


class Roulette_Wheel_Selection():
    def __init__(self, bit_len):
        self.bit_len = bit_len

    def select(self, proportional_list, population):
        population_size = population.population_size
        population = population.individuals
        chosen = []
        for n in range(population_size):
            r = random.random()
            for (i, individual) in enumerate(population):
                if r <= proportional_list[i]:
                    chosen.append(copy.deepcopy(individual))
                    break

        parents = CGAComponents.Population(self.bit_len, population_size)
        parents.setIndividuals(chosen)
        return parents


class Crossover():
    def __init__(self, c_rate, bit_len, float_bit_len):
        self.c_rate = c_rate
        self.bit_len = bit_len
        self.float_bit_len = float_bit_len

    def crossover_one_pair(self, pa, pb):
        bit_len = self.bit_len
        float_bit_len = self.float_bit_len
        childa = CGAComponents.Individual(bit_len, float_bit_len)
        childb = CGAComponents.Individual(bit_len, float_bit_len)

        # set cross over point
        mu_point = np.random.randint(bit_len)
        pa_value, pb_value = pa.value, pb.value

        # cross over and generation children
        childa_value = np.zeros(shape=pa_value.shape)
        childb_value = np.zeros(shape=pa_value.shape)

        childa_value[:mu_point] = pa_value[:mu_point]
        childa_value[mu_point:] = pb_value[mu_point:]

        childb_value[:mu_point] = pb_value[:mu_point]
        childb_value[mu_point:] = pa_value[mu_point:]

        childa.value = childa_value
        childb.value = childb_value

        offsprings = [childa, childb]
        return offsprings

    def crossover(self, parents):
        crossover_rate = self.c_rate
        # one-point cross-over
        parents_size = parents.population_size
        bit_len = self.bit_len
        parents = parents.individuals

        count = 0
        children_pool = []
        while count < parents_size:
            mates = np.random.choice(parents, size=2)
            parent_a, parent_b = mates
            if np.random.rand() < crossover_rate:
                childs = self.crossover_one_pair(parent_a, parent_b)
            else:
                childs = [copy.deepcopy(parent_a), copy.deepcopy(parent_b)]
            children_pool.extend(childs)
            count = count + 2
        children_pool = children_pool[:parents_size]

        next_generation = CGAComponents.Population(bit_len, parents_size)
        next_generation.setIndividuals(children_pool)
        return next_generation


class Mutation():
    def __init__(self, mu_rate):
        self.mu_rate = mu_rate

    def mutation(self, population):
        '''
        # Mutation: Bitwise (each bit has a probability of flipping its state).
        # CGA generally uses small mutation rates
        '''
        mutation_rate = self.mu_rate
        pop_size = population.population_size
        totalBits = population.bit_len
        population = population.individuals

        # choose mutation position number
        new_population = []
        for p in range(pop_size):
            individual = copy.deepcopy(population[p])
            for i in range(totalBits):
                if np.random.rand() < mutation_rate:
                    individual.value[i] = 1 - individual.value[i]
            new_population.append(individual)

        next_generation = CGAComponents.Population(totalBits, pop_size)
        next_generation.setIndividuals(new_population)
        return next_generation
