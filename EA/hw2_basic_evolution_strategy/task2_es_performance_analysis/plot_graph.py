#!/usr/bin python3.6
import os
import sys
import argparse
import pdb

import numpy as np
import matplotlib.pyplot as plt


def plot_graph(opts, inp_data):
    pass


def main(opts):
    '''we will plot 3 graph in this script: avg fitness performance, max fitness performance and diversity graph'''
    # load data
    whole_pack = np.load(opts.input)
    avg_data, max_data, div_data = whole_pack['avg_data'], whole_pack['max_data'], whole_pack['div_data']

    # plot avg graph
    plot_graph(avg_data)

    # plot max graph
    plot_graph(max_data)

    # plot div graph
    plot_graph(div_data)

    print('all ploting job done!')


def parseArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='')
    parser.add_argument('-o', '--output', help='')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    print(os.path.dirname(__file__))
    #opts = parseArgs(sys.argv)
    #main(opts)
