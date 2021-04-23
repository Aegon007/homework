#!/usr/bin python3.6
"""Entry point to evolving the neural network. Start here."""
import logging
from optimizer import Optimizer
from tqdm import tqdm
import pdb

import network as nk


# Setup logging.
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG,
    filename='log.txt'
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


def generate(generations, population_size, bit_len):
    """Generate a network with the genetic algorithm.
    Args:
        generations (int): Number of times to evole the population
        population (int): Number of networks in each generation
        nn_param_choices (dict): Parameter choices for networks
    """
    optimizer = Optimizer(bit_len, population_size)
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


def print_networks(networks):
    """Print a list of networks.
    Args:
        networks (list): The population of networks
    """
    logging.info('-'*80)
    for network in networks:
        network.print_network()


def main():
    """Evolve a network."""
    generations = 10  # Number of times to evole the population.
    population_size = 15  # Number of networks in each generation.
    bit_len = 6   # 2 bits for nb_neuron, 2 bits for nb_layer, 1 bit for activation, 1 bit for optimizer

    logging.info("***Evolving %d generations with population size %d***" % (generations, population_size))

    generate(generations, population_size, bit_len)


if __name__ == '__main__':
    main()
