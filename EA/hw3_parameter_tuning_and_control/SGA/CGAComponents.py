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

Optimization of Rosenbrock:
    In brief, what I’m asking you to do is to modify your CGA to find values of x and y such that the following function is MINIMIZED:
        f(x, y) = (a - x)^2 + b(y - x^2), where a = 1 and b = 100
'''


def get_probability_list(fitness_list):
    total_fit = float(sum(fitness_list))
    relative_fitness = [f/total_fit for f in fitness_list]
    proportional_list = [sum(relative_fitness[:i+1]) for i in range(len(relative_fitness))]
    return proportional_list


def convert_2_int(binary_rep):
    # convert binary to decimal integer
    # the first bit is sign bit, 0 means positive, 1 means negative
    sign_bit = binary_rep[0]
    binary_rep = binary_rep[1:]
    bin_list = list(binary_rep)
    bin_list = [str(int(aaa)) for aaa in bin_list]
    bin_str = ''.join(bin_list)
    try:
        rtn = int(bin_str, 2)
        if 1 == sign_bit:
            rtn = rtn * -1
    except Exception:
        pdb.set_trace()
    return rtn, sign_bit


def convert_2_float(binary_rep, sign_bit):
    # convert binary to decimal fraction
    decimal = 0
    bit_len = len(binary_rep)
    for i in range(bit_len):
        decimal += 2 ** (-i - 1) * int(binary_rep[i])
    if 1 == sign_bit:
        decimal = decimal * -1
    return decimal


def convert_bin_2_deci(x_bin, int_bit_len):
    x_bin_int, x_bin_float = x_bin[:int_bit_len], x_bin[int_bit_len:]

    x_int, sign_bit = convert_2_int(x_bin_int)
    x_float = convert_2_float(x_bin_float, sign_bit)
    x_val = x_int + x_float
    return x_val


class Individual():
    def __init__(self, bit_len, float_bit_len, doInitialize=True):
        # set representation format
        # individual have 16 bits, 8 bits for x and 8 bits for y
        # 5 bits for integer part and 3 bits for fraction part
        self.bit_len = bit_len
        self.float_bit_len = float_bit_len
        self.__phenotype = 0
        self.value_range = [-5.12, 5.11]

        if doInitialize:
            self.value = (np.random.rand(bit_len) > 0.5) * 1
        else:
            self.value = None

        # evaluation and fitness
        self.evaluation = None
        self.fitness = None

    def calculate_phenotype(self):
        '''
        # x and y gene are fixed float binary representation
        # by default, each one is 10 bit, 7 bit for integer and
        # 3 bit for float
        '''
        # split bits_rep into x and y
        mid_point = self.bit_len // 2
        x, y = list(self.value[:mid_point]), list(self.value[mid_point:])

        # convert x and y from binary to decimal first
        int_bit_len = mid_point - self.float_bit_len
        x_val = convert_bin_2_deci(x, int_bit_len)
        y_val = convert_bin_2_deci(y, int_bit_len)

        # limit the x and y value to [-5.12, 5.11]
        x_val = np.clip(x_val, *self.value_range)
        y_val = np.clip(y_val, *self.value_range)

        # f(x, y) = (a - x)^2 + b(y - x^2)^2, where a = 1 and b = 100
        fx = (1 - x_val)**2 + 100 * (y_val - x_val**2)**2
        self.__phenotype = fx
        return self.__phenotype


class Population():
    '''collection of individuals'''
    def __init__(self, bit_len, float_bit_len, size=10):
        self.bit_len = bit_len
        self.float_bit_len = float_bit_len
        self.population_size = size

        self.individuals = np.array([])
        tmp_individual = Individual(bit_len, float_bit_len, doInitialize=False)
        self.IndvClass = tmp_individual.__class__

    def setIndividuals(self, individual_list):
        '''set individuals for the next generation'''
        IndvClass = self.IndvClass
        self.individuals = np.array(individual_list, dtype=IndvClass)

    def initialize(self):
        '''initialization random individuals for start point'''
        IndvClass = self.IndvClass
        tmp_list = [IndvClass(self.bit_len, self.float_bit_len) for i in range(self.population_size)]
        self.individuals = np.array(tmp_list, dtype=IndvClass)

    def fitness(self):
        '''calculate fitness score'''
        if 0 == self.individuals.size:
            raise ValueError('individuals has not been set')

        # calculate fitness, normalize the phenotype value
        pheno_val_list = []
        for indv in self.individuals:
            tmp_pheno_score = indv.calculate_phenotype()
            pheno_val_list.append(tmp_pheno_score)

        fit_list = []
        sum_pheno = sum(pheno_val_list)
        # and reverse it since we find the min
        for p_val in pheno_val_list:
            tmp_val = p_val/sum_pheno
            fit_list.append(tmp_val)

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


def test():
    print('now doing the test function')
    x_bin = [0, 1, 1, 1, 0, 1, 0]
    int_bit_len = 3
    deci_val = convert_bin_2_deci(x_bin, int_bit_len)
    print('calculated value is: ', deci_val, '\texpected to be: 3.625')

    x_bin = [1, 1, 1, 1, 1, 1, 0]
    int_bit_len = 3
    deci_val = convert_bin_2_deci(x_bin, int_bit_len)
    print('calculated value is: ', deci_val, '\texpected to be: -3.875')


if __name__ == "__main__":
    test()
