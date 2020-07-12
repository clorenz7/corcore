"""
First, will create a quick object to hold adjacency list rep of graph

"""
from collections import deque


class Graph(object):

    def __init__(self, vertices, edge_list, undirected=False):
        """
        inputs:
            vertices: list of vertex objects, length is # of vertexes
            edge_list: list of edge tuples (u,v) for indexes u->v
            undirected: If True, will build an undirected graph
                default: False
        """

        self.vertices = vertices
        self._nv = len(vertices)
        self._ne = len(edge_list)
        self.weight_map = {}
        self._undirected = undirected
        self._has_neg_weights = False

        self.adj_list = [ [] for _ in range(self.n_vertices) ]

        for edge in edge_list:
            u,v = edge[:2]  # Will add weight later
            if len(edge) > 2:
                w = edge[2]
                self.weight_map[(u,v)] = w
                if w < 0:
                    self._has_neg_weights = True
            else:
                w = None
            self.adj_list[u].append(v)
            if undirected:
                self.adj_list[v].append(u)
                if w is not None:
                    self.weight_map[(v,u)] = w

    @property
    def n_vertices(self):
        return self._nv

    @property
    def has_negative_weights(self):
        return self._has_neg_weights

    def get_edges(self, v_idx):
        """
        inout: v_idx: int index of vertex
        output: list of vertex indexes which are connected
        """
        return self.adj_list[v_idx]

    def get_vertex(self, idx):
        return self.vertices[idx]

    def get_weight(self, v_from, v_to):
        return self.weight_map[(v_from, v_to)]

    def transpose(self):
        if self._undirected:
            raise ValueError("Transpose of undirected graph doesn't make sense!")

        t_edge_list = []
        for v_from, v_to_list in enumerate(self.adj_list):
            if len(v_to_list) > 0:
                t_edge_list.extend([ (v, v_from) for v in v_to_list ])

        t_graph = Graph(self.vertices, t_edge_list)

        return t_graph


    def T(self):
        return self.transpose()

class DFS(object):
    """
    Object to perform a depth first search.
    Stores results of enter and exit step for each vertex.
    """

    def __init__(self, graph):
        self.graph = graph
        self.state = ['unseen']*graph.n_vertices
        self.entered = [-1]*graph.n_vertices
        self.exited = [-1]*graph.n_vertices
        self.step = 1

    def visit(self, index):

        if self.state[index] == 'unseen':
            self.state[index] = 'visited'
            self.entered[index] = self.step
            self.step += 1

            next_verts = self.graph.get_edges(index)

            for v_idx in next_verts:
                    self.visit(v_idx)
            self.exit(index)

    def exit(self, index):
        if self.state[index] == 'unseen':
            raise RuntimeError("Trying to exit an unseen vertex")
        if self.state[index] == 'visited':
            self.state[index] = 'finished'
            self.exited[index] = self.step
            self.step += 1

    def search(self, visit_order=None):

        if visit_order is None:
            visit_order = range(self.graph.n_vertices)

        for v_idx in visit_order:
            self.visit(v_idx)

        return self


class BFS(object):
    """
    Object to perform a breadth first search.
    Stores results of depth and parent for each vertex.
    """

    def __init__(self, graph):
        self.graph = graph
        n_vert = graph.n_vertices
        self.state = ['unseen']*n_vert
        self.level = [-1]*n_vert
        self.parent = [-1]*n_vert
        self.vertex_queue = deque([])

    def search(self, source_index):

        self.vertex_queue.append(source_index)
        self.level[source_index] = 0

        while len(self.vertex_queue) != 0:
            index = self.vertex_queue.popleft()

            adj_indexes = self.graph.get_edges(index)
            for adj_index in adj_indexes:
                if self.state[adj_index] == "unseen":
                    self.state[adj_index] = 'visited'
                    self.parent[adj_index] = index
                    self.vertex_queue.append(adj_index)
                    self.level[adj_index] = self.level[index] + 1

            self.state[index] = 'exited'

        return self


