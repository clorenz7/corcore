from unittest import TestCase
from binary_search_trees import Node, Tree


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
