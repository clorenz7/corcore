from unittest import TestCase

import numpy as np

from pycorcore.graph import Graph, DFS, BFS
from pycorcore.graph import strongly_connected_components
from pycorcore.graph import calc_min_spanning_tree
from pycorcore.graph import shortest_paths, NegativeCycleError
from pycorcore.graph import algs
from pycorcore.graph.objects import FlowGraph

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

class TestSpanTree(TestCase):
    def test_min_span_tree(self):
        vertices = range(5)
        edge_list = [
            (0,1,1), (0,4, 100), (0, 2, 102), (0,3, 103),
            (1,2,2), (1,4, 105),
            (2,3,3), (2,4, 106),
            (3,4,4), (3,1, 104),
        ]
        graph = Graph(vertices, edge_list)
        edge_list = calc_min_spanning_tree(graph)

        self.assertEqual(set(edge_list), {(0,1), (1,2), (2,3), (3,4)})

        self.assertTrue(graph.is_valid)


class TestShortestPaths(TestCase):
    def test_neg_cycle(self):
        vertices = range(4)
        edge_list = [
            (0,1,1), (0,3,1),
            (1,2,2),
            (2,0,-10),
            (3,1,3)
        ]

        graph = Graph(vertices, edge_list)

        with self.assertRaises(NegativeCycleError):
            min_path, parents = shortest_paths(graph, 0)

    def test_shortest_path(self):
        vertices = range(6)
        edge_list = [
            (0,1,1), (0,3,10),
            (1,2,2), (1,3,20),
            (2,3,3), (2,0,30),
            (3,4,4), (3,5,40),
            (4,5,5), (4,2,50),
            (5,1,-1),
        ]

        graph = Graph(vertices, edge_list)

        min_path, parents = shortest_paths(graph, 0)
        self.assertEqual(min_path, [0, 1, 3, 6, 10, 15])
        self.assertEqual(parents, [-6, 0, 1, 2, 3, 4])

class TestMaxFlow(TestCase):

    def test_single_source_sink(self):
        # Figure 27.4 from CLR
        vertices = range(6)
        edge_list = [
            (0,1,16), (0,2,13),
            (1,2,10), (1,3,12),
            (2,1,4),  (2,4,14),
            (3,2,9),  (3,5,20),
            (4,3,7),  (4,5,4),
        ]

        graph = FlowGraph(vertices, edge_list, source_idx=0, sink_idx=5)

        max_flow = algs.calc_max_flow(graph, source_idx=0, sink_idx=5)

        self.assertEqual(max_flow, 23)
