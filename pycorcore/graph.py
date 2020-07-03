"""
First, will create a quick object to hold adjacency list rep of graph

"""

class Graph(object):

    def __init__(self, vertices, edge_list, undirected=False):
        """
        inputs:
            vertices: list of vertex objects, length is # of vertexes
            edge_list: list of edge tuples (u,v) for indexes u->v
            undirected: If True, will build an undirected graph
                default: False
        """

        self._vertices = vertices
        self._nv = len(vertices)
        self._ne = len(edge_list)

        self.adj_list = [ [] for _ in range(self.n_vertices) ]

        for edge in edge_list:
            u,v = edge[:2]  # Will add weight later
            self.adj_list[u].append(v)
            if undirected:
                self.adj_list[v].append(u)

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


class DFS(object):

    def __init__(self, graph):
        self.graph = graph
        self.state = ['unseen']*graph.n_vertices
        self.entered = [-1]*graph.n_vertices
        self.exited = [-1]*graph.n_vertices
        self.step = 1
        self.vertex_stack = []

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
