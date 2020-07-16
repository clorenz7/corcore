"""
Given a binary tree, find the maximum path sum.
The path may start and end at any node in the tree.
For example, given the below binary tree

       1
      / \
     2   3
the result is 6.
"""

# Stream of consciousness thought process:
# (0) Important points: not a search tree. Could have negative values?
#    Assuming no loops (e.g. why is 3-1-3 not a value path?)
# (1) Try to find node that is the parent of the maximum path
# (2) Could use recursion...
# Alternately, could use bellman-ford algorithm. Treat the tree as a graph.
#  but we don't know source and sink.. That is for min path
# I think recursion is the best way to do it.
#  for each node, calculate the max path through it...
#  it's a post order traversal.

import math

def calc_max_branch(node, result):

    if node is None:
        return 0

    left_path = calc_max_branch(node.left, result)
    right_path = calc_max_branch(node.right, result)

    # Record the left, right, and max paths
    node.left_path = left_path
    node.right_path = right_path
    node.max_path = node.key + max(left_path, 0) +  max(node.right_path, 0)

    # Give a clue as to how to reconstruct
    if left_path == right_path == 0:
        node.branch = 'stop'
    elif left_path >= right_path:
        node.branch = 'left'
    else:
        node.branch = 'right'

    # Record the single branch that is longest for later construction
    node.max_branch = node.key + max(max(node.left_path, node.right_path), 0)

    # Store the results
    if node.max_path > result['max_path']:
        result['max_path'] = node.max_path
        result['node'] = node

    return node.max_branch


def find_max_path(root):
    # Initialize the results
    result = {'max_path': -math.inf, 'node': None}

    # Do a post traversal on the tree
    calc_max_branch(root, result)

    return result['max_path']


#---- Unit Testing
class Node(object):
    def __init__(self, key, parent=None, left=None, right=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.key = key


def set_up():
    # Initialize a tree for testing
    nodes = [Node(i) for i in [-1, 2, 5, 7, 9]]
    nodes[1].left = nodes[0]
    nodes[1].right = nodes[2]
    nodes[2].left = nodes[3]
    nodes[2].right = nodes[4]
    return nodes


def test_max_path():

    # This is the example given in the problem
    nodes = [Node(i) for i in range(4)]
    nodes[1].left = nodes[2]
    nodes[1].right = nodes[3]

    max_path = find_max_path(nodes[1])

    assert max_path == 6, "obtained {} != expected 6".format(max_path)

    # Homebrewed example: subtree is best
    #    2
    #   / \
    # -1   5
    #     / \
    #    7   9

    nodes = set_up()
    max_path = find_max_path(nodes[1])

    assert max_path == 21, "obtained {} != expected 21".format(max_path)

    # Modified tree such that a single branch is the best
    #    2
    #   / \
    # -1   5
    #     / \
    #   -7   9
    nodes = set_up()
    nodes[3].key *= -1
    max_path = find_max_path(nodes[1])

    assert max_path == 16, "obtained {} != expected 16".format(max_path)


    # Make upper triangle the best
    # Turn the 7 to be negative, to get a single branch
    #       2
    #      / \
    #     1   5
    #    /   / \
    # -11  -7  -9
    nodes = set_up()
    nodes[0].key *= -1
    nodes[3].key *= -1
    nodes[4].key *= -1
    nodes.append(Node(-11))
    nodes[0].left = nodes[5]

    max_path = find_max_path(nodes[1])

    assert max_path == 8, "obtained {} != expected 8".format(max_path)


if __name__ == "__main__":
    test_max_path()



