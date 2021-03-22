#!/usr/bin python3.6
import os
import sys
import argparse
import pdb

import numpy as np

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


class Individual():
    def __init__(self, bit_len, doInitialize=True):
        # set representation format
        self.bit_len = bit_len
        self.__phenotype = 0

        if doInitialize:
            self.gene = []
            for bit in range(bit_len):
                tmp = np.random.rand() * np.random.choice([-10, 10])
                self.gene.append(tmp)
            self.gene = np.array(self.gene)

            self.mutations = np.random.rand(bit_len)
        else:
            self.gene = None
            self.mutations = None

        # evaluation and fitness
        self.fitness = 0
        self.choose_prob = 0

    def get_pheotype(self):
        return self.__phenotype

    def set_individual(self, gene, mutations):
        self.gene = gene
        self.mutations = mutations

    def calculate_phenotype(self):
        '''used to solve Himmelblau's function
        Himmelblau's function is a multi-model function, used to test the
        performance of optimization algorithms. The function is defined by:
        f(x, y) = (x^2 + y - 11)^2 + (x + y^2 -7)^2
        '''
        # split bits_rep into x and y
        x, y = self.gene[0], self.gene[1]
        fxy = (x**2 + y - 11)**2 + (x + y**2 - 7)**2
        self.__phenotype = fxy
        return self.__phenotype


class Population():
    '''collection of individuals'''
    def __init__(self, bit_len, mu_size=10):
        self.bit_len = bit_len
        self.population_size = mu_size

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
        '''calculate fitness score for the whole population
        # Selection Method:
            In this assignment, we will use the ranking selection, and we are trying
            to minimize the given problem, so we want the phenotype value to be small.
        '''
        # evaluation function
        if 0 == self.individuals.size:
            raise ValueError('individuals has not been set')

        # calculate phenotype
        pheno_val_list = []
        for indv in self.individuals:
            tmp_pheno_score = indv.calculate_phenotype()
            pheno_val_list.append(tmp_pheno_score)
            indv.fitness = tmp_pheno_score

        # calculate ranking and then use the ranking to get the fitness
        # calculate the selection prob is according the function:
        #   P(i) = (2-s)/mu + (2*rank_i*(s-1))/(mu*(mu-1))
        #   note the best have rank mu-1, while the worst have rank 0
        def rank_population(pheno_val_list):
            rtn = np.argsort(pheno_val_list)[::-1]   # samllest value have the highest rank
            return list(rtn)

        s = 1.5
        prob_list = []
        mu_size = self.population_size
        rank_list = rank_population(pheno_val_list)
        for rank_i, indv in zip(rank_list, self.individuals):
            prob = (2-s)/mu_size + (2*rank_i*(s-1))/(mu_size*(mu_size-1))
            prob_list.append(prob)
            indv.choose_prob = prob

        return prob_list, pheno_val_list

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
            indv_val = individual.gene
            if notInPool(indv_val, identical_pool):
                identical_pool.append(indv_val)

        identical_percentage = len(identical_pool) / self.population_size
        return identical_percentage

    def diversity_score(self):
        '''Diversity of Population measured as the euclidian distance
        between the members of the population that furthest apart in
        Genome space'''
        def compute_distance(individual_a, individual_b):
            gene_a, gene_b = individual_a.gene, individual_b.gene
            vec1, vec2 = np.array(gene_a), np.array(gene_b)
            dist = np.linalg.norm(vec1-vec2)
            return dist

        largest_distance = 0
        population = self.individuals
        for i in range(self.population_size):
            for j in range(i, self.population_size):
                item_a, item_b = population[i], population[j]
                tmp_dis = compute_distance(item_a, item_b)
                if tmp_dis > largest_distance:
                    largest_distance = tmp_dis
        return largest_distance

    def best(self, fit_list):
        '''return the most fit object'''
        index = fit_list.index(max(fit_list))
        bestOne = self.individuals[index]
        print('best one has value: ', bestOne.value)
        print('best one has fitness score: ', bestOne.fitness)


def test():
    pass


if __name__ == '__main__':
    test()