#!/usr/bin/python3

import os
import sys
import argparse
import pdb

import random
import math
import numpy as np
import copy

import CGAComponents_rosenBrock
import CGAOperator

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

def print_header_line(p_name, pop_size, bit_len, mu_rate, c_rate):
    # <problem name> <population size> <bitstring genome length> <mutation rate> <crossover rate>
    screen_line = '<problem name: {}> <population size: {}> <bitstring genome length: {}> <mutation rate: {}> <crossover rate: {}>'.format(p_name, pop_size, bit_len, mu_rate, c_rate)
    print(screen_line)


def print_runtime_line(gen_num, most_fit_score, avg_fit_score, identical_percentage):
    # <generation number> <fitness score of the most fit member of the population> <average fitness score> <precent of genomes in population that are identical>
    screen_line = []
    screen_line.append('<generation number: {}>'.format(gen_num))
    screen_line.append('<fitness score of the most fit member of the population: {:f}>'.format(most_fit_score))
    screen_line.append('<average fitness score: {:f}>'.format(avg_fit_score))
    screen_line.append('<precent of genomes in population that are identical: {:f}>'.format(identical_percentage))

    screen_line = '\n'.join(screen_line) + '\n'
    print(screen_line)


def print_termination_line(best_fit_flag):
    if best_fit_flag:
        termination_reason = 'population has converaged'
    else:
        termination_reason = 'exceed generation limit'
    print('termination reason is: {}'.format(termination_reason))


def stopCondition(fitness_score_list):
    # stop the algorithm if there is one individual's fitness socore is
    # equal to 1 or the total iteration number is greater than countlimit
    for fitness_score in fitness_score_list:
        if fitness_score == 1:
            return True
    return False


def run_rosenbrock(population_size, bit_len, mu_rate, c_rate, generation_limit, float_bit_len, qname):
    '''run Canonical Genetic Algorithm for rosen brock minimization problem'''
    print_header_line(qname, population_size, bit_len, mu_rate, c_rate)

    # setup all objects
    population = CGAComponents_rosenBrock.Population(bit_len, float_bit_len, population_size)
    selection = CGAOperator.Roulette_Wheel_Selection(bit_len)
    crossover = CGAOperator.Crossover(c_rate, bit_len, float_bit_len)
    mutation = CGAOperator.Mutation(mu_rate)

    # initialize population
    population.initialize()

    # solving process
    best_fit_flag = False
    for n in range(generation_limit):
        # evaluate
        proportional_list, fitness_list = population.fitness()
        most_fit_score = max(fitness_list)
        avg_fit_score = sum(fitness_list) / len(fitness_list)
        identical_percentage = population.compute_identical_percentage()
        print_runtime_line(n, most_fit_score, avg_fit_score, identical_percentage)

        # check stop condition
        if stopCondition(fitness_list):
            best_fit_flag = True
            break

        # select
        parents = selection.select(proportional_list, population)

        # crossover
        offspring = crossover.crossover(parents)

        # mutation
        population = mutation.mutation(offspring)

    # print termination line
    print_termination_line(best_fit_flag)

    # return the best individual
    return population.best(fitness_list)


def main():
    # setup parameters
    bit_len = 20    # Genome length
    population_size = 32
    c_rate = 0.5    # crossover rate
    mu_rate = 0.01   # mutation rate
    generation_limit = 100

    # for each genome 1st half bits are for value of x and last half bits are for value y,
    # and for both x and y, last float_bit_len bits are for the fraction part, the first part are for integer
    # e.g. [1,1,1,0,0,1,1,0], [1,1,1,0] are for the integer part, [0,1,1,0] are for the fraction part
    float_bit_len = 4

    run_rosenbrock(population_size, bit_len, mu_rate, c_rate, generation_limit, float_bit_len, 'rosen_brock')

    print('CGA run finished!')


if __name__ == "__main__":
    main()
