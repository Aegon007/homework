#!/usr/bin/python3

import os
import sys
import argparse
import pdb

import random
import math
import numpy as np
import numpy.random as np_rand
import copy


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


def get_probability_list(fitness_list):
    total_fit = float(sum(fitness_list))
    relative_fitness = [f/total_fit for f in fitness_list]
    proportional_list = [sum(relative_fitness[:i+1]) for i in range(len(relative_fitness))]
    return proportional_list


class Individual():
    def __init__(self, bit_len, doInitialize=True):
        # set representation format
        self.bit_len = bit_len
        if doInitialize:
            self.value = (np.random.rand(bit_len) > 0.5) * 1
        else:
            self.value = None

        # evaluation and fitness
        self.evaluation = None
        self.fitness = None


class Population():
    '''collection of individuals'''
    def __init__(self, bit_len, size=10):
        self.bit_len = bit_len
        self.population_size = size

        self.individuals = np.array([])
        tmp_individual = Individual(bit_len, doInitialize=False)
        self.IndvClass = tmp_individual.__class__

    def setIndividuals(self, individual_list):
        '''set individuals for the next generation'''
        IndvClass = self.IndvClass
        self.individuals = np.array(individual_list, dtype=IndvClass)

    def initialize(self):
        '''initialization random individuals for start point'''
        IndvClass = self.IndvClass
        tmp_list = [IndvClass(self.bit_len) for i in range(self.population_size)]
        self.individuals = np.array(tmp_list, dtype=IndvClass)

    def fitness(self):
        '''calculate fitness score'''
        # evaluation function
        def evaluate_one(individual):
            fitness_score = sum(individual.value)/len(individual.value)
            return fitness_score

        if 0 == self.individuals.size:
            raise ValueError('individuals has not been set')

        # calculate fitness
        sum_fitness = 0
        fit_list = []
        for indv in self.individuals:
            tmp_fit_score = evaluate_one(indv)
            sum_fitness = sum_fitness + tmp_fit_score
            fit_list.append(tmp_fit_score)

        proportional_list = get_probability_list(fit_list)
        return proportional_list, fit_list

    def compute_identical_percentage(self):
        '''compute identical individual percentage'''
        def notInPool(indv_val, identical_pool):
            if not identical_pool:
                return True
            for item in identical_pool:
                if (indv_val == item).all():
                    return False
            return True

        identical_pool = []
        for individual in self.individuals:
            indv_val = individual.value
            if notInPool(indv_val, identical_pool):
                identical_pool.append(indv_val)

        identical_percentage = len(identical_pool) / self.population_size
        return identical_percentage

    def best(self, fit_list):
        '''return the most fit object'''
        index = fit_list.index(max(fit_list))
        bestOne = self.individuals[index]
        print('best one has value: ', bestOne.value)
