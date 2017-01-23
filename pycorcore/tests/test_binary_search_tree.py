from unittest import TestCase
from pycorcore.bst import Node, Tree


class TestBst(TestCase):

    def setUp(self):
        tree = Tree(Node(15, None))
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


class TestDepth(TestCase):

    def test_balanced_depth(self):
        tree = Tree(Node(5, None))
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
