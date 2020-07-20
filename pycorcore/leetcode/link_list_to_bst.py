"""
Given a singly linked list where elements are sorted in ascending order,
convert it to a height balanced BST.
"""

# Questions I would have had:
# (1) am I get the number of elements?

# Thoughts:
# (1) Use a Red-black tree?
# (2) Do insert, followed by a tree rotation?
# (3) Track length when I insert, then rotate as needed..
#   CAn keep track of # of elements in the tree, Keep rotating left until root is correct?
# Track ideal root
# rotate left on parent of ideal root while it is not ideal rool.
# Keep track of longest path. If root in correct spot, rotate GGP left?


# I was attempting a solution which was too difficult (in-place construction)
# A simpler strategy I looke dup was to get the number of nodes, and to use recursion.
# Because you can divide and conquer off of the root node.
# So I am coding that up.

import math

class Element(object):

    def __init__(self, key, next_elem=None):
        self.key = key
        self.next_elem = next_elem


class Node(object):

    def __init__(self, key, parent=None, left=None, right=None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right


def linked_to_bst(list_head):

    pointer_array = [list_head]
    element = list_head

    # Traverse the linked list, construct an array of pointers, and get the length.
    while element.next_elem is not None:
        pointer_array.append(element.next_elem)  # Basically python version of pointer..
        element = element.next_elem


    # Call a recursive function which takes the n/2the element as the root,
    # and recursively constructs the left and right subtrees
    bst_root = construct_bst(pointer_array)

    return bst_root

def construct_bst(pointer_array):

    n_nodes = len(pointer_array)
    root_idx = math.floor(n_nodes/2)

    # Termination conditions: Empty array, size 1 array
    if n_nodes == 0:
        return None

    # Construct root node
    root_node = Node(pointer_array[root_idx].key)

    if n_nodes == 1:
        return root_node

    # Construct left subtree
    left_root = construct_bst(pointer_array[:root_idx])
    # Construct right subtree
    right_root = construct_bst(pointer_array[(root_idx+1):])

    root_node.left = left_root
    if left_root is not None:
        left_root.parent = root_node

    root_node.right = right_root
    if right_root is not None:
        right_root.parent = root_node

    return root_node


def test_bst_constuct():
    print("Unit Testing Linked List to BST Constructor...")

    # Create the linked list
    elements = [Element(i+1) for i in range(7)]
    for i,e in enumerate(elements):
        if i != len(elements)-1:
            e.next_elem = elements[i+1]


    bst = linked_to_bst(elements[0])

    assert bst.key == 4, "Root is incorrect!"
    assert bst.left.key == 2, "Root Left Child is incorrect!"
    assert bst.right.key == 6, "Root Right Child is incorrect!"
    assert bst.left.parent.key == 4, "Root Left Child Parent is incorrect!"
    assert bst.right.parent.key == 4, "Root Right Child Parent is incorrect!"

    assert bst.left.left.key == 1, "Leaf node is incorrect!"
    assert bst.left.right.key == 3, "Leaf node is incorrect!"
    assert bst.right.left.key == 5, "Leaf node is incorrect!"
    assert bst.right.right.key == 7, "Leaf node is incorrect!"


    new_elem = Element(8)
    elements[-1].next_elem = new_elem
    elements.append(new_elem)

    bst = linked_to_bst(elements[0])

    assert bst.key == 5, "Inbalanced Root is incorrect"
    assert bst.left.left.left is not None, "Inbalanced leaf incorrect"
    assert bst.left.left.left.key == 1, "Inbalanced leaf incorrect"
    print("All Passed!")


if __name__ == "__main__":
    test_bst_constuct()