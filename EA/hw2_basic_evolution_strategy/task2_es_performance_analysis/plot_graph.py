#!/usr/bin python3.6
import os
import sys
import argparse
import pdb

import numpy as np
import matplotlib.pyplot as plt


def plot_graph(opts, x_data, y_data, x_label, y_label, title):
    plt.plot(x_data, y_data, color='r', marker='o')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    save_path = os.path.join(opts.output, '{}.jpg'.format(title))
    plt.savefig(save_path)
    plt.show()


def get_x_data(y_data):
    data_point_num = len(y_data)
    x_data = list(range(1, data_point_num+1))
    return x_data


def main(opts):
    '''we will plot 3 graph in this script: avg fitness performance, max fitness performance and diversity graph'''
    # make outdir
    os.makedirs(opts.output, exist_ok=True)

    # load data
    whole_pack = np.load(opts.input)
    avg_data, most_data, div_data = whole_pack['avg_data'], whole_pack['most_data'], whole_pack['div_data']

    x_avg_data = get_x_data(avg_data)
    x_most_data = get_x_data(most_data)
    x_div_data = get_x_data(div_data)

    # plot avg graph
    x_label = 'generation number'
    y_label = 'average fitness score'
    title = 'Average Fitness Graph'
    plot_graph(opts, x_avg_data, avg_data, x_label, y_label, title)

    # plot most graph
    x_label = 'generation number'
    y_label = 'most fitness score '
    title = 'Performance of Best Population Member'
    plot_graph(opts, x_most_data, most_data, x_label, y_label, title)

    # plot div graph
    x_label = 'generation number'
    y_label = 'diversity score'
    title = 'Diversity of Population'
    plot_graph(opts, x_div_data, div_data, x_label, y_label, title)

    print('all ploting job done!')


def parseArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='')
    parser.add_argument('-o', '--output', help='')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    opts = parseArgs(sys.argv)
    main(opts)
