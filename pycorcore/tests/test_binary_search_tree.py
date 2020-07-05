from unittest import TestCase
from pycorcore.bst import Node, BinarySearchTree


class TestBst(TestCase):

    def setUp(self):
        tree = BinarySearchTree(Node(15, None))
        self.vals = (6, 18, 3, 7, 17, 20, 2, 4, 13, 9)
        for val in self.vals:
            tree.add_node(Node(val, None))
        self.tree = tree

    def test_bst(self):

        node_9 = self.tree.query(9)
        self.assertEqual(node_9.key, 9)

        self.assertEqual(self.tree.root_node.max_child(),
                         max(self.vals))

        pred = node_9.predecessor()
        self.assertEqual(pred, 7)

        single_node = Node(1, None)
        self.assertIsNone(single_node.predecessor())

        node_2 = self.tree.query(2)
        self.assertEqual(node_2.key, 2)
        self.assertIsNone(node_2.predecessor())

        with self.assertRaises(KeyError):
            self.tree.query(sum(self.vals))  # assuming non-neg ints

class TestRotate(TestCase):
    def test_rotate_right(self):
        tree = BinarySearchTree(Node(12))
        tree.add_node(Node(13))
        tree.add_node(Node(10))
        tree.add_node(Node(11))
        other_node = Node(9)
        tree.add_node(other_node)
        tree.add_node(Node(8))
        tree.add_node(Node(7))

        tree.rotate_right(tree.root_node)
        tree.rotate_right(other_node)

        self.assertEqual(tree.root_node.key, 10)
        self.assertEqual(tree.root_node.right.key, 12)
        self.assertEqual(tree.root_node.right.left.key, 11)
        self.assertEqual(tree.root_node.right.right.key, 13)

        self.assertEqual(tree.root_node.left.key, 8)
        self.assertEqual(tree.root_node.left.right.key, 9)
        self.assertEqual(tree.root_node.left.left.key, 7)

    def test_rotate_left(self):
        tree = BinarySearchTree(Node(0))
        rotate_node = Node(1)
        tree.add_node(rotate_node)
        tree.add_node(Node(3))
        tree.add_node(Node(2))
        tree.add_node(Node(4))

        tree.rotate_left(tree.root_node)
        tree.rotate_left(rotate_node)

        self.assertEqual(tree.root_node.key, 3)
        self.assertEqual(tree.root_node.left.key, 1)
        self.assertEqual(tree.root_node.right.key, 4)
        self.assertEqual(tree.root_node.left.right.key, 2)
        self.assertEqual(tree.root_node.left.left.key, 0)


class TestDepth(TestCase):

    def test_balanced_depth(self):
        tree = BinarySearchTree(Node(5, None))
        # Test degenerate case: 1 node
        depth, deepest_node = tree.get_deepest_node()
        self.assertEqual(depth, 0)
        self.assertEqual(deepest_node.key, 5)

        # Add more keys on left side so it is the longest
        self.vals = (4, 3, 2, 1, 0, 6, 7, 8)
        for val in self.vals:
            tree.add_node(Node(val, None))

        depth, deepest_node = tree.get_deepest_node()
        self.assertEqual(depth, 5)
        self.assertEqual(deepest_node.key, 0)

        # Add additional keys to the right so it is longest
        for val in (9, 10, 11):
            tree.add_node(Node(val, None))

        depth, deepest_node = tree.get_deepest_node()
        self.assertEqual(depth, 6)
        self.assertEqual(deepest_node.key, 11)
