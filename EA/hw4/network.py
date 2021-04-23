#!/usr/bin python3.6
import random
import logging
from train import train_and_score
import pdb


def bin2str(bin_list):
    bin_list = [str(aaa) for aaa in bin_list]
    rtn = ''.join(bin_list)
    return rtn


def map_bin2deci(binary_rep):
    nn_param_bin = binary_rep
    pdb.set_trace()
    nb_neurons = nn_param_bin[:2]
    nb_layers = nn_param_bin[2:4]
    activation = nn_param_bin[4:5]
    optimizer = nn_param_bin[5:]

    nb_neurons_str = bin2str(nb_neurons)
    nb_layers_str = bin2str(nb_layers)
    activation_str = bin2str(activation)
    optimizer_str = bin2str(optimizer)

    nb_neurons_deci = int(nb_neurons_str, 2)
    nb_layers_deci = int(nb_layers_str, 2)
    activation_deci = int(activation_str, 2)
    optimizer_deci = int(optimizer_str, 2)

    return nb_neurons_deci, nb_layers_deci, activation_deci, optimizer_deci


def map_deci2bin(deci_dict):
    nb_neurons_bin = bin(deci_dict['nb_neurons'])[2:]
    nb_layers_bin = bin(deci_dict['nb_layers'])[2:]
    activation_bin = bin(deci_dict['activation'])[2:]
    optimizer_bin = bin(deci_dict['optimizer'])[2:]

    tmp = [nb_neurons_bin, nb_layers_bin, activation_bin, optimizer_bin]
    binary_rep = ''.join(tmp)
    return binary_rep


def get_nn_param_dict():
    nn_param_dict = {
                'nb_neurons': [32, 64, 128, 256],
                'nb_layers': [1, 2, 3, 4],
                'activation': ['relu', 'elu'],
                'optimizer': ['rmsprop', 'adam']
            }
    return nn_param_dict


class Network():
    """Represent a network and let us operate on it"""
    def __init__(self, nn_param_bin=None):
        """Initialize our network.
        Args:
            nn_param_choices (dict): Parameters for the network, includes:
                nb_neurons (list): [32, 64, 128, 256]
                nb_layers (list): [1, 2, 3, 4]
                activation (list): ['relu', 'elu']
                optimizer (list): ['rmsprop', 'adam']

        # total binary representation is 6 bits
        # 2 bits for nb_neurons, 2 bits for nb_layers
        # 1 bit for activation, 1 bit for optimizer
        """
        self.accuracy = 0
        self.network = {}  # (dic): represents MLP network parameters
        self.nn_param_bin = nn_param_bin

        # Set network properties
        if nn_param_bin:
            self.network = self.get_deci_dict(nn_param_bin)

    def create_random(self):
        """Create a random network."""
        nn_param_choices = get_nn_param_dict()
        for key in nn_param_choices:
            self.network[key] = random.choice(nn_param_choices[key])

    def get_binary_rep(self):
        deci_dict = []
        for key in self.network.keys():
            deci_dict[key] = self.nn_param_choices[key].index(self.network[key])
        binary_rep = map_deci2bin(deci_dict)
        return binary_rep

    def get_deci_dict(self, nn_param_bin):
        nn_param_deci = map_bin2deci(nn_param_bin)
        network = {}
        for key in nn_param_deci.keys():
            network[key] = self.nn_param_choices[nn_param_deci[key]]
        return network

    def get_param(self):
        return self.nn_param_bin

    def fitness(self):
        return self.accuracy

    def train(self):
        """Train the network and record the accuracy"""
        if self.accuracy == 0:
            self.accuracy = train_and_score(self.network)

    def print_network(self):
        """Print out a network."""
        logging.info(self.network)
        logging.info("Network accuracy: %.2f%%" % (self.accuracy * 100))
