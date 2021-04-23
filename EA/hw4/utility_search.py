#!/usr/bin python3.6
"""Entry point to evolving the neural network. Start here."""
import os
import logging
from optimizer import Optimizer
from tqdm import tqdm
import pdb
import matplotlib.pyplot as plt

import network as nk


# Setup logging.
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG,
    filename='utility_log.txt'
)

def train_networks(networks):
    """Train each network.
    Args:
        networks (list): Current population of networks
        dataset (str): Dataset to use for training/evaluating
    """
    pbar = tqdm(total=len(networks))
    for network in networks:
        network.train()
        pbar.update(1)
    pbar.close()


def get_probability_list(fit_list):
    total_fit = float(sum(fit_list))
    relative_fitness = [f/total_fit for f in fit_list]
    proportional_list = [sum(relative_fitness[:i+1]) for i in range(len(relative_fitness))]
    return proportional_list


def calculate_fitness(networks):
    if 0 == len(networks):
        raise ValueError('population size is 0!')

    fit_list = []
    for item in networks:
        tmp_fit_score = item.fitness()
        fit_list.append(tmp_fit_score)
    proportional_list = get_probability_list(fit_list)
    return proportional_list, fit_list


def generate(generations, population_size, bit_len, mu_rate, c_rate):
    """Generate a network with the genetic algorithm.
    Args:
        generations (int): Number of times to evole the population
        population (int): Number of networks in each generation
        nn_param_choices (dict): Parameter choices for networks
    """
    optimizer = Optimizer(bit_len, population_size, mu_rate, c_rate)
    networks = optimizer.create_population()

    # Evolve the generation.
    for i in range(generations):
        logging.info("***Doing generation %d of %d***" % (i + 1, generations))

        # Train and get accuracy for networks.
        train_networks(networks)

        # evaluate
        proportional_list, fitness_list = calculate_fitness(networks)
        most_fit_score = max(fitness_list)
        avg_fit_score = sum(fitness_list) / len(fitness_list)

        # Print out the average accuracy each generation.
        logging.info("most fit score is: {:f}\taverage fit score is: {:f}".format(most_fit_score, avg_fit_score))
        logging.info('-'*80)

        networks = optimizer.evolve(networks, proportional_list)

    # Sort our final population.
    networks = sorted(networks, key=lambda x: x.accuracy, reverse=True)

    # Print out the top 5 networks.
    print_networks(networks[:5])

    max_acc = networks[0].fitness()
    return max_acc


def print_networks(networks):
    """Print a list of networks.
    Args:
        networks (list): The population of networks
    """
    logging.info('-'*80)
    for network in networks:
        network.print_network()


def plot_graph(param_list, acc_list, save_path, utility_name):
    print('figure save to file: {}'.format(save_path))
    plt.title('Performance of ' + utility_name)
    plt.xlabel('utility param value')
    plt.ylabel('average accuracy')
    plt.grid(True)
    plt.plot(param_list, acc_list)
    plt.savefig(save_path)
    plt.show(block=False)
    plt.figure()


def main():
    """Evolve a network."""
    generations = 10  # Number of times to evole the population.
    population_size = 15  # Number of networks in each generation.
    bit_len = 6   # 2 bits for nb_neuron, 2 bits for nb_layer, 1 bit for activation, 1 bit for optimizer

    save_dir = 'fig_dir'
    os.makedirs(save_dir, exist_ok=True)

    mu_list = [0.01, 0.03, 0.05, 0.07, 0.09]
    acc_list = []
    c = 0.5
    for mu in mu_list:
        logging.info("***Evolving {} generations with population size {}, mutation rate is: {:f}, crossover rate is: {:f}***".format(generations, population_size, mu, c))
        max_acc = generate(generations, population_size, bit_len, mu_rate=mu, c_rate=0.5)
        acc_list.append(max_acc)
    save_path = os.path.join(save_dir, 'mu_search.png')
    plot_graph(mu_list, acc_list, save_path)

    c_list = [0.1, 0.2, 0.3, 0.4, 0.5]
    acc_list = []
    mu = 0.01
    for c in c_list:
        logging.info("***Evolving {} generations with population size {}, mutation rate is: {:f}, crossover rate is: {:f}***".format(generations, population_size, mu, c))
        max_acc = generate(generations, population_size, bit_len, mu_rate=mu, c_rate=c)
        acc_list.append(max_acc)
    save_path = os.path.join(save_dir, 'c_search.png')
    plot_graph(mu_list, acc_list, save_path)


if __name__ == '__main__':
    main()
