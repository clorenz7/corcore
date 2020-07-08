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

        self.adj_list = [ [] for _ in range(self.n_vertices) ]

        for edge in edge_list:
            u,v = edge[:2]  # Will add weight later
            if len(edge) > 2:
                w = edge[2]
                self.weight_map[(u,v)] = w
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

def strongly_connected_components(graph):

    # Do a depth first search of the graph
    dfs_1 = DFS(graph).search()

    # Sort vertices by exit time
    visit_order = sorted(zip(graph.vertices, dfs_1.exited), key=lambda x:x[1], reverse=True)
    visit_order = [v[0] for v in visit_order]

    # Do a depth first search of the transposed graph
    trans_graph = graph.transpose()
    dfs_2 = DFS(trans_graph).search(visit_order)

    # Re-construct the DFS trees to get connected components
    # Initialize variables
    conn_comps = []
    root_vert = visit_order[0]
    exit_time = 0

    # O(n^2) worst case implementation, could probably do better by storing more data in DFS object
    enter_times = list(dfs_2.entered)
    while exit_time < graph.n_vertices*2:
        comps = []
        exit_time = dfs_2.exited[root_vert]
        for (ii, enter_time) in enumerate(enter_times):
            # All entrance times less than exit time are in the tree
            if enter_time < exit_time:
                comps.append(ii)
                enter_times[ii] = graph.n_vertices*100  # never select again
            # New root vertex discovered at next time step
            if enter_time == exit_time+1:
                root_vert = ii
        conn_comps.append(comps)
        exit_time += 1

    return conn_comps


