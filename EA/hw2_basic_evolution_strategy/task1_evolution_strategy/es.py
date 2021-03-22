#!/usr/bin python3.6
import os
import sys
import pdb
import argparse

import numpy as np

import es_component
import es_strategy

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

Output Specific:
When your code runs, it should print out a “one time” header that contains this info:

<problem name> <mu size> <lambda size> <mutation standard deviation> <crossover rate>

<generation number> <number of candidate evaluations done cumulative from the beginning of the
search> <fitness score of the most fit member of the population> <average fitness score>
<diversity score of the population>
'''


def print_header_line(p_name, mu_size, lamda_size, mu_dev, c_rate):
    # <problem name> <mu size> <lamda size> <mutation standard deviation> <crossover rate>
    screen_line = '<problem name: {}> <mu size: {}> <lamda size: {}>'.format(p_name, mu_size, lamda_size)
    screen_line += ' <mutation standard deviation: {}> <crossover rate: {}>'.format(mu_dev, c_rate)
    print(screen_line)


def print_runtime_line(gen_num, candidate_num_sum, most_fit_score, avg_fit_score, diversity_score):
    # <generation number> <number of candidate evaluations done cumulative from the beginning of the search>
    # <fitness score of the most fit member of the population> <average fitness score> <diversity score of the population>
    screen_line = []
    screen_line.append('<generation number: {}>'.format(gen_num))
    screen_line.append('<number of candidate evaluations done cumulative from the beginning of the search>: {}>'.format(candidate_num_sum))
    screen_line.append('<fitness score of the most fit member of the population: {:f}>'.format(most_fit_score))
    screen_line.append('<average fitness score: {:f}>'.format(avg_fit_score))
    screen_line.append('<diversity score of the population: {:f}>'.format(diversity_score))

    screen_line = '\n'.join(screen_line) + '\n'
    print(screen_line)


def print_termination_line(best_fit_flag):
    if best_fit_flag:
        termination_reason = 'population has converaged'
    else:
        termination_reason = 'exceed generation limit'
    print('termination reason is: {}'.format(termination_reason))


def stopCondition(fit_score_list):
    for fitness_score in fit_score_list:
        if fitness_score <= 0.3:
            return True
    return False


def run_es(mu_size, lamda_size, mu_dev, c_rate, bit_len, generation_limit, DNA_RANGE):
    '''run Evolution Strategy Algorithm for Himmelblau's function maximization problem'''
    p_name= 'Evolution Strategy for Himmelblaus\'s function'
    print_header_line(p_name, mu_size, lamda_size, mu_dev, c_rate)

    # setup all objects
    population = es_component.Population(bit_len, mu_size)
    selection = es_strategy.SurvivorSelection(mu_dev, mu_size)
    recombination = es_strategy.Recombination(lamda_size, bit_len)
    mutation = es_strategy.Mutation(learning_rate=mu_dev, bit_len=bit_len, DNA_RANGE=DNA_RANGE)

    # initialize population
    population.initialize()

    # solving process
    best_fit_flag = False
    candidate_num_sum = 0
    avg_fitness_list, most_fit_score_list, diversity_list = [], [], []
    for n in range(generation_limit):
        # recombination, here we set parents num == 3
        offspring = recombination.recombination(population, 3)

        # mutation
        population = mutation.mutation(offspring)

        # evaluate
        prob_list, fitness_list = population.fitness()
        most_fit_score = min(fitness_list)
        avg_fit_score = sum(fitness_list) / len(fitness_list)
        diversity_score = population.diversity_score()

        avg_fitness_list.append(avg_fit_score)
        most_fit_score_list.append(most_fit_score)
        diversity_list.append(diversity_score)

        # print the runtime line
        candidate_num_sum += len(fitness_list)
        print_runtime_line(n, candidate_num_sum, most_fit_score, avg_fit_score, diversity_score)

        # check stop condition, stop if most_fit_score did not change for 3 iters
        if stopCondition(fitness_list):
            best_fit_flag = True
            break

        # select
        population = selection.select(prob_list, population)

        # decrease learning rate
        mutation.decrease_lr(n)

    # print termination line
    print_termination_line(best_fit_flag)

    # return the data for plot the graph
    return avg_fitness_list, most_fit_score_list, diversity_list


def main():
    # setup parameters
    bit_len = 2    # Genome length
    mu_size = 15
    lamda_size = 100
    c_rate = 0.5    # crossover rate
    mu_dev = 0.5   # mutation rate
    generation_limit = 100
    DNA_RANGE = [-10, 10]

    avg_fitness_list, most_fitness_list, diversity_list = run_es(mu_size, lamda_size, mu_dev, c_rate, bit_len, generation_limit, DNA_RANGE)

    # save the data during the run, and plot the data with a standalone script
    avg_fitness_list, most_fitness_list, diversity_list = np.array(avg_fitness_list), np.array(most_fitness_list), np.array(diversity_list)
    this_file_path = os.path.realpath(__file__)
    current_dir = os.path.dirname(this_file_path)
    save_path = os.path.join(current_dir, 'run_stat.npz')
    np.savez(save_path, avg_data=avg_fitness_list, most_data=most_fitness_list, div_data=diversity_list)
    print('save the avg_fitness_list data to path: {}'.format(save_path))

    print('CGA run finished!')


if __name__ == "__main__":
    main()
