#!/usr/bin python3.6
import pdb
import random
import time

import binary_tree
import queue


def process_one(TreeDepth, node_index_list):
    '''each unit of time, I send the identifier of a node chosen independently
    and uniformly at random from all of N nodes. Note that I might send you a
    node that is already marked'''
    test_tree = binary_tree.CompleteTree(TreeDepth)
    tree_root = test_tree.build_tree()

    start = time.time()
    while 1:
        ran_idx = random.choice(node_index_list, replace=False)
        tree_root = test_tree.mark_node(tree_root, ran_idx)
        mark_num = test_tree.all_marked(tree_root)
        if 'all' == mark_num:
            break
    end = time.time()
    time_last = end - start
    return time_last


def process_two(TreeDepth, node_index_list):
    '''each unit of time, I send the identifier of a node chosen uniformly
    random from those nodes that I have not yet sent'''
    pass


def process_three(TreeDepth, node_index_list):
    '''each unit of time I send the identifier of a node chosen uniformly
    random from those nodes that you have not yet marked'''
    pass


def main():
    TreeDepth = 5
    total_nodes = 2**TreeDepth - 1
    node_index_list = list(range(1, total_nodes+1))


if __name__ == "__main__":
    main()
