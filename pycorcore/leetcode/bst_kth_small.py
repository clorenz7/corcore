"""
Given a binary search tree, write a function to find the kth smallest element in it.
(1 ≤ k ≤ BST's total elements)
"""

# Basic idea:
# (1) Do a DFS, prioritizing left.
# (2) keep a counter of the number of nodes you have "exited"
# (3) We "exit" after checking left, before going right.
# (3) The kth one you exit is the node.

# Alternately, could do k min value searches, and k-1 deletes.

from collections import defaultdict


def kth_smallest(root, k=1):
    """
    assume root node has .left, .right, .parent, ,key fields.
    """

    node_status = defaultdict(lambda: 'unvisited')

    count = 0
    stack = [root] # A list is a stack.

    while len(stack) != 0:
        do_increment = False
        current_node = stack[-1]  # ie peek

        node_status[current_node] = 'visited'

        if current_node.left is not None:

            left_status = node_status[current_node.left]
            if left_status == 'exited':
                stack.pop()
                do_increment = True

            elif left_status == 'unvisited':
                stack.append(current_node.left)
                continue
        else:
            stack.pop()
            do_increment = True

        if current_node.right is not None:
            stack.append(current_node.right)

        if do_increment:
            node_status[current_node] = 'exited'
            count += 1
            if count == k:
                return current_node.key

    raise IndexError("Tree is too small! Only found: {} nodes".format(count))


class Node(object):
    def __init__(self, key, parent=None, left=None, right=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.key = key


def test_kth():
    nodes = [Node(i) for i in range(10)]

    nodes[6].left = nodes[2]
    nodes[2].left = nodes[1]
    nodes[4].left = nodes[3]
    nodes[8].left = nodes[7]

    nodes[2].right = nodes[4]
    nodes[4].right = nodes[5]
    nodes[6].right = nodes[8]
    nodes[8].right = nodes[9]

    root = nodes[6]

    for k in range(9):
        key = kth_smallest(root, k+1)
        print(key)

if __name__ == "__main__":
    test_kth()


