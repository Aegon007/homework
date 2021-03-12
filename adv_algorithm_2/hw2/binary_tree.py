#!/usr/bin python3.6
# code for complete bianry tree
import pdb

import queue


class Node:
    def __init__(self, item):
        self.item = item
        self.left = None
        self.right = None
        self.parent = None
        self.marker = False


class CompleteTree():
    def __init__(self, depth):
        self.depth = depth
        self.nodeCount = 2 ** depth - 1
        self.count = 1

    # Count the number of nodes
    def count_nodes(self, root):
        if root is None:
            return 0
        return (1 + self.count_nodes(root.left) + self.count_nodes(root.right))

    # Check if the tree is complete binary tree
    def is_complete(self, root, index, numberNodes):
        # Check if the tree is empty
        if root is None:
            return True

        if index >= numberNodes:
            return False

        left_completeness = self.is_complete(root.left, 2 * index + 1, numberNodes)
        right_completeness = self.is_complete(root.right, 2 * index + 2, numberNodes)
        rtn = (left_completeness and right_completeness)
        return rtn

    def build_tree(self):
        '''BFS way to create the tree'''
        node_index_list = []
        if self.depth == 0:
            return None, node_index_list   # return empty tree if depth equals to 0

        root = Node(1)
        if self.depth == 1:
            node_index_list.append(root.item)
            return root, node_index_list

        nodeCount = self.nodeCount - 1
        count = 2
        travers_queue = queue.Queue()
        travers_queue.enqueue(root)
        node_index_list.append(root.item)
        while nodeCount:
            tmp_node = travers_queue.dequeue()
            tmp_node.left = Node(count)
            count = count + 1
            nodeCount = nodeCount - 1
            tmp_node.left.parent = tmp_node
            travers_queue.enqueue(tmp_node.left)
            node_index_list.append(tmp_node.left.item)

            if nodeCount == 0:
                break

            tmp_node.right = Node(count)
            tmp_node.right.parent = tmp_node
            count = count + 1
            nodeCount = nodeCount - 1
            travers_queue.enqueue(tmp_node.right)
            node_index_list.append(tmp_node.right.item)

        return root, node_index_list

    def create(self, root, depth):
        if 0 == depth:
            root = None
        else:
            root = Node(self.count)
            root.left = self.create(root.left)
            root.right = self.create(root.right)

    def mark_node(self, root, node_index):
        '''travers the tree, and mark the node along with two other rules:
            1: if a node and its sibling are marked, its parent is marked.
            2: if a node and its parent are marked, the other sibling is marked
        '''
        travers_queue = queue.Queue()
        travers_queue.enqueue(root)

        while travers_queue.notEmpty():
            elem = travers_queue.dequeue()
            left_child = elem.left
            right_child = elem.right
            if left_child:
                travers_queue.enqueue(left_child)
            if right_child:
                travers_queue.enqueue(right_child)

            # judge if elem.item == node_index
            if elem.item == node_index:
                elem.marker = True

                if elem.item == 1:
                    continue

                # apply rule 1
                if (elem.parent.left is None) or (elem.parent.right is None):
                    continue
                else:
                    if elem.parent.left.marker & elem.parent.right.marker:
                        elem.parent.marker = True

                # apply rule 2
                if (elem.parent.left is None) or (elem.parent.right is None):
                    continue
                else:
                    if elem.parent.marker:
                        elem.parent.left.marker = True
                        elem.parent.right.marker = True

        return root

    def all_marked(self, root):
        '''BFS travers the tree to see if all marked or not'''
        # put all node in a list
        node_list = []
        travers_queue = queue.Queue()
        travers_queue.enqueue(root)
        node_list.append(root)
        while travers_queue.notEmpty():
            item = travers_queue.dequeue()
            left_child = item.left
            right_child = item.right

            if left_child:
                travers_queue.enqueue(left_child)
                node_list.append(left_child)

            if right_child:
                travers_queue.enqueue(right_child)
                node_list.append(right_child)

        # go through the list see if how many item are markered
        marker_num = 0
        marked_list = []
        for elem in node_list:
            if elem.marker:
                marker_num += 1
                marked_list.append(elem.item)
        if marker_num == len(node_list):
            rtn = 'all'
        else:
            rtn = str(marker_num)
        return rtn, marked_list


def test():
    cTree = CompleteTree(4)
    root, node_index_list = cTree.build_tree()
    print('node_index_list is: ', node_index_list)
    node_count = cTree.count_nodes(root)

    index = 0
    if cTree.is_complete(root, index, node_count):
        print("The tree is a complete binary tree")
    else:
        print("The tree is not a complete binary tree")

    mark_num = cTree.all_marked(root)
    if 'all' == mark_num:
        print("All nodes of the tree is marked")
    else:
        print("{} nodes of the tree is not marked".format(mark_num))

    # test to make the tree fully marked
    send_list = [2, 3, 5, 6, 9, 10, 12, 15]
    for item in send_list:
        root = cTree.mark_node(root, item)
    mark_num, marked_list = cTree.all_marked(root)
    print("{} nodes of the tree is marked/should be all".format(mark_num))
    print('marked nodes are: ', marked_list)


if __name__ == "__main__":
    test()
