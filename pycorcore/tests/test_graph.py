from unittest import TestCase

import numpy as np

from pycorcore.graph import Graph, DFS, BFS, strongly_connected_components

class TestDFS(TestCase):

    def setUp(self):
        pass

    def test_dfs(self):
        """
        Random DFS I made up
        """
        vertices = range(10)
        edge_list = [
            (0, 1), (0, 4), (0, 6), (0, 9),
            (1, 0), (1, 2), (1, 3), (1,4), (1,5),
            (2, 5), (2,9),
            (3, 3), (3,6), (3,9),
            (4, 5), (4, 6), (4, 8),
            (5, 1), (5, 2), (5, 4),
            (6, 1), (6,7),
            (7, 8), (7, 9),
            (8, 9),
            (9, 0), (9, 8),
        ]

        graph = Graph(vertices, edge_list)
        dfs = DFS(graph)
        dfs.search()

        # Check that all vertexes are entered before exiting
        self.assertTrue(np.all(np.array(dfs.entered) < np.array(dfs.exited)))

        self.assertEqual(
            dfs.entered,
            [1, 2, 3, 17, 5, 4, 6, 7, 8, 9]
        )
        self.assertEqual(
            dfs.exited,
            [20, 19, 16, 18, 14, 15, 13, 12, 11, 10]
        )


    def test_dfs_clr(self):
        """
        Example from Intro To Algorithms Fig 23.4
        """
        vertices = range(6)
        edge_list = [
            (0,1), (0,3),
            (1,4),
            (2,4), (2,5),
            (3,1),
            (4,3),
            (5,5)
        ]
        graph = Graph(vertices, edge_list)
        dfs = DFS(graph)
        dfs.search()

        self.assertTrue(np.all(np.array(dfs.entered) < np.array(dfs.exited)))

        self.assertEqual(dfs.entered, [1,2,9,4,3,10])
        self.assertEqual(dfs.exited,  [8,7,12,5,6,11])



class TestBFS(TestCase):

    def test_full_tree(self):
        vertices = range(7)
        edge_list = [
            (0,1), (0,2),
            (1,3), (1,4),
            (2,5), (2,6),
        ]
        graph = Graph(vertices, edge_list)
        bfs = BFS(graph)
        bfs.search(0)

        self.assertEqual(bfs.level,   [0,1,1,2,2,2,2])
        self.assertEqual(bfs.parent, [-1,0,0,1,1,2,2])

    def test_bfs_clr(self):
        """
        Example from Intro To Algorithms Figure 23.3
        """
        vertices = range(8)
        edge_list = [
            (0,1), (0,4),
            (1,5),
            (2,3), (2,5), (2,6),
            (3,7),
            (5,6),
            (6,7)
        ]
        graph = Graph(vertices, edge_list, undirected=True)
        bfs = BFS(graph)
        bfs.search(1)

        self.assertEqual(len(bfs.vertex_queue), 0)
        self.assertEqual(bfs.level,  [1,  0, 2, 3, 2, 1, 2, 3])
        self.assertEqual(bfs.parent, [1, -1, 5, 2, 0, 1, 5, 6])


class TestConComps(TestCase):

    def test_transpose(self):
        vertices = range(5)
        edge_list = [
            (0,1),
            (1,2),
            (2,3),
            (3,0),
            (4,3)
        ]
        graph = Graph(vertices, edge_list)

        trans_graph = graph.transpose()

        self.assertEqual(trans_graph.get_edges(0), [3])
        self.assertEqual(trans_graph.get_edges(1), [0])
        self.assertEqual(trans_graph.get_edges(2), [1])
        self.assertEqual(trans_graph.get_edges(3), [2,4])

    def test_strong_conn_comps(self):
        vertices = range(10)
        edge_list = [
            (0,1),
            (1,2),
            (2,3),
            (3,0), (3,4),
            (4,5),
            (5,6),
            (6,4), (6,7),
            (7,8),
            (8,7), (8,9)
        ]
        graph = Graph(vertices, edge_list)

        comps = strongly_connected_components(graph)

        self.assertEqual(comps, [[0, 1, 2, 3], [4, 5, 6], [7, 8], [9]])
