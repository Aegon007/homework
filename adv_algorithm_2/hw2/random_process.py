#!/usr/bin python3.6
import os
import sys
import pdb
import random
import time
import argparse

import numpy as np

import binary_tree
import queue


def process_one(TreeDepth):
    '''each unit of time, I send the identifier of a node chosen independently
    and uniformly at random from all of N nodes. Note that I might send you a
    node that is already marked'''
    test_tree = binary_tree.CompleteTree(TreeDepth)
    tree_root, node_index_list = test_tree.build_tree()

    send_node_list = []
    start = time.time()
    while 1:
        ran_idx = random.choice(node_index_list)
        send_node_list.append(ran_idx)
        tree_root = test_tree.mark_node(tree_root, ran_idx)
        mark_num, marked_list = test_tree.all_marked(tree_root)
        if 'all' == mark_num:
            break
    end = time.time()
    time_last = end - start
    return time_last, send_node_list


def process_two(TreeDepth):
    '''each unit of time, I send the identifier of a node chosen uniformly
    random from those nodes that I have not yet sent'''
    test_tree = binary_tree.CompleteTree(TreeDepth)
    tree_root, node_index_list = test_tree.build_tree()

    send_node_list = []
    start = time.time()
    while 1:
        ran_idx = np.random.choice(node_index_list, replace=False)
        send_node_list.append(ran_idx)
        tree_root = test_tree.mark_node(tree_root, ran_idx)
        mark_num, marked_list = test_tree.all_marked(tree_root)
        if 'all' == mark_num:
            break
    end = time.time()
    time_last = end - start
    return time_last, send_node_list


def process_three(TreeDepth):
    '''each unit of time I send the identifier of a node chosen uniformly
    random from those nodes that you have not yet marked'''
    test_tree = binary_tree.CompleteTree(TreeDepth)
    tree_root, node_index_list = test_tree.build_tree()

    send_node_list = []
    start = time.time()
    while 1:
        ran_idx = np.random.choice(node_index_list, replace=False)
        send_node_list.append(ran_idx)
        tree_root = test_tree.mark_node(tree_root, ran_idx)
        mark_num, marked_list = test_tree.all_marked(tree_root)
        if 'all' == mark_num:
            break
        for item in marked_list:
            if item in node_index_list:
                node_index_list.remove(item)
    end = time.time()
    time_last = end - start
    return time_last, send_node_list


def parseArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--method', help='choose from process_1/process_2/process_3')
    parser.add_argument('-o', '--output', help='file to output the results')
    opts = parser.parse_args()
    return opts

def main(opts):
    '''choose to run different processs'''
    f = open(opts.output, 'w')
    for n in range(10, 21):
        print('run with n = {}'.format(n), file=f, flush=True)
        print('run with n = {}'.format(n))
        total_time = 0
        TreeDepth = n
        for i in range(10):
            if opts.method == 'process_1':
                time_last, send_node_list = process_one(TreeDepth)
            elif opts.method == 'process_2':
                time_last, send_node_list = process_two(TreeDepth)
            elif opts.method == 'process_3':
                time_last, send_node_list = process_three(TreeDepth)
            else:
                raise NotImplementedError()
            total_time = total_time + time_last
        avg_time = total_time/10
        print('Process: {} run with n={} havs total running time: {:f}, and avg running time: {:f}'.format(opts.method, n, total_time, avg_time), file=f, flush=True)
        print('send node number = {}'.format(len(send_node_list)), file=f, flush=True)
        print('Process: {} run with n={} havs total running time: {:f}, and avg running time: {:f}'.format(opts.method, n, total_time, avg_time))
        print('send node number = {}'.format(len(send_node_list)))
    f.close()


if __name__ == "__main__":
    opts = parseArgs(sys.argv)
    main(opts)
