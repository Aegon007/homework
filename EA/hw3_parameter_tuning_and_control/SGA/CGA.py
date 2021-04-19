#!/usr/bin/python3

import os
import sys
import argparse
import pdb

import random
import math
import numpy as np
import copy
import matplotlib.pyplot as plt

import CGAComponents
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


def run(population_size, bit_len, mu_rate, c_rate, generation_limit, float_bit_len, qname):
    '''run Canonical Genetic Algorithm for rosen brock minimization problem'''
    print_header_line(qname, population_size, bit_len, mu_rate, c_rate)

    # setup all objects
    population = CGAComponents.Population(bit_len, float_bit_len, population_size)
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

    if most_fit_score < 0.2:
        return True
    else:
        return False


def one_test(param):
    # setup parameters
    bit_len = 16    # Total Genome length, two variables, each have 8 bit, 1 for sign bit, 3 for integer, 4 for float point
    population_size = 64
    c_rate = 0.5    # crossover rate
    # mu_rate = 0.01   # mutation rate
    mu_rate = param
    generation_limit = 150

    # for each genome 1st half bits are for value of x and last half bits are for value y,
    # and for both x and y, last float_bit_len bits are for the fraction part, the first part are for integer
    # e.g. [1,1,1,0,0,1,1,0], [1,1,1,0] are for the integer part, [0,1,1,0] are for the fraction part
    # and the first bit of the integer part is for the sign bit, 0 indicate positive and 1 for negative 
    float_bit_len = 4

    qname = 'DeJong\'s_Test_Suite_Function_2'
    flag = run(population_size, bit_len, mu_rate, c_rate, generation_limit, float_bit_len, qname)

    print('CGA run finished!')

    return flag


def plot_graph(param_with_success_rate, file_path):
    '''rendering the graph with the given data'''
    x, y = [], []
    for elem in param_with_success_rate:
        tmp_x, tmp_y = elem[0], elem[1]
        x.append(tmp_x)
        y.append(tmp_y)

    plt.title('Utility landscape of the SGA model')
    plt.xlabel('mutation rate')
    plt.ylabel('Performance')
    plt.grid(True)
    plt.plot(x, y)
    plt.savefig(file_path)
    plt.show()
    plt.figure()


def find_highest(tuple_list):
    sorted_list = sorted(tuple_list, key=lambda x: x[1], reverse=True)
    highest_tuple = sorted_list[0]
    return highest_tuple[0], highest_tuple[1]


def tune_params(opts):
    ''''''
    param_with_success_rate = []
    params = np.arange(0, 0.3, 0.02)
    for param in params:
        count, success = 0, 0
        for i in range(10):
            flag = one_test(param)
            count += 1
            if flag:
                success += 1

        success_rate = success / count
        print('The success rate for the SGA is: {}'.format(success_rate))
        tmp_tuple = (param, success_rate)
        param_with_success_rate.append(tmp_tuple)

    highest_param, highest_success_rate = find_highest(param_with_success_rate)
    print('The highest success rate is: {:f}, the corresponding params is: {}'.format(success_rate, highest_param))

    os.makedirs(opts.output, exist_ok=True)
    file2save = os.path.join(opts.output, 'utility_performance.jpg')
    plot_graph(param_with_success_rate, file2save)


def parserArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tune', action='store_true', help='')
    parser.add_argument('-o', '--output', default='resDir', help='')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    opts = parserArgs(sys.argv)
    if opts.tune:
        tune_params(opts)
    else:
        one_test(0.01)
