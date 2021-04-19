#!/usr/bin python3.6
import os
import sys
import argparse
import pdb

import random
import numpy as np
import copy
import math

import es_component

'''
Recombination: Discrete or Intermediate as you see fit. On of the two must be present and you
should explain, in comments to your code, why you choose one over the other.

Mutation: Gaussian Perturbation

Parent Selection: Uniform Random

Survivor Selection: (mu, lambda) OR (mu+lambda) as you see fit. One of the two must be present
and you should explain, in comments to your code, WHY you choose one over the other.

Self-Adaptation: Standard OR Correlated Mutations. There must be at LEAST ONE mutation parameter 
per allele. I.E. in Table 4.1 in the book, you may use either the second or first option in the
table, but NOT the first where theta_alpha = 1

Population Size: use mu = 15 and lamda = 100

Search Range /  Area of Space: You need only search the space of x in the range of [-10.0, ... , 10.0]
and y in the range of [-10.0, ... , 10.0]
'''


class Mutation():
    def __init__(self, learning_rate, bit_len, DNA_RANGE=[-10, 10]):
        self.learning_rate = learning_rate
        self.bit_len = bit_len
        self.DNA_RANGE = DNA_RANGE
    
    def mutation(self, population):
        '''
        apply self adaptation, mutate mutation parameters according learning rate
        using standard mutation with one mutation parameter per allele
        '''
        new_population = []
        pop_size = population.population_size

        # delta_new = delta * e^(tao*standard_norm)
        # x_new = x + delta_new * stabdard_norm
        # we may also need to clip x_new
        population = population.individuals
        for p in range(pop_size):
            individual = copy.deepcopy(population[p])
            for i in range(self.bit_len):
                # mutate the mutation parameters first
                standard_norm = np.random.normal(0, 1, 1)
                mutation_new = individual.mutations[i] * math.exp(self.learning_rate * standard_norm)
                individual.mutations[i] = mutation_new

                # mutate the allele based on new mutation allele
                standard_norm = np.random.normal(0, 1, 1)
                tmp = individual.gene[i] + mutation_new * standard_norm
                individual.gene[i] = np.clip(tmp, *self.DNA_RANGE)
            new_population.append(individual)

        next_generation = es_component.Population(self.bit_len, pop_size)
        next_generation.setIndividuals(new_population)
        return next_generation

    def decrease_lr(self, iter_num):
        if iter_num % 3 == 0:
            self.learning_rate = self.learning_rate * 0.5
            print('learning rate adjust to: {:f}'.format(self.learning_rate))


class ParentSelection():
    def __init__(self):
        pass
    
    def select(self, population, mu):
        pass


class SurvivorSelection():
    def __init__(self, bit_len, mu_size):
        self.bit_len = bit_len
        self.mu_size = mu_size

    def select(self, proportional_list, population):
        '''
        # (mu, lamda) is: where typically lamda > mu children are created from a population of mu parents,
          all the parents are discarded, The fitness component comes from the fact that the lamda offsprings
          are ranked according to the fitness, and the best mu form the next generation.
        # (mu+lamda) is: where the set of offsprings and parentsare merged and ranked according to fitness,
          then the top mu are kept to form the next generation.
        # In this code, we will choose (mu, lamda) survivor selection, for it generally performs better than
          (mu+lamda) 
        '''
        population_size = self.mu_size
        population = population.individuals
        chosen = []
        while len(chosen) < population_size:
            r = random.uniform(0, 0.1)
            for (i, individual) in enumerate(population):
                if r <= individual.choose_prob:
                    chosen.append(copy.deepcopy(individual))
                    break

        parents = es_component.Population(self.bit_len, population_size)
        parents.setIndividuals(chosen)
        print(len(chosen))
        return parents


class Recombination():
    def __init__(self, lamda, bit_len):
        self.lamda = lamda
        self.bit_len = bit_len

    def recombination(self, parents, parents_num):
        '''as suggest from the text book, our settings for recombination is:
                * we are using intermediate recombination for gene
                * we are using Intermediate recombination for mutation parameters
        '''
        def make_kid(parents):
            new_mutations = np.zeros(parents[0].mutations.shape)
            new_gene = np.zeros(parents[0].gene.shape)
            num_p = len(parents)
            for i in range(num_p):
                # recombine mutations
                new_mutations = new_mutations + parents[i].mutations
                # recombine gene
                new_gene = new_gene + parents[i].gene
            new_mutations = new_mutations / num_p
            new_gene = new_gene / num_p

            # form kids
            kid = es_component.Individual(self.bit_len, doInitialize=False)
            kid.set_individual(new_gene, new_mutations)
            return kid
        
        offSprings = []
        parents = parents.individuals
        parents = list(parents)
        for i in range(self.lamda):
            tmp_parents = random.sample(parents, parents_num)
            kid = make_kid(tmp_parents)
            offSprings.append(kid)
        
        next_generation = es_component.Population(self.bit_len, self.lamda)
        next_generation.setIndividuals(offSprings)
        return next_generation


def test():
    pass


if __name__ == '__main__':
    test()