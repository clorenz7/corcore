"""
First, will create a quick object to hold adjacency list rep of graph

"""
from collections import deque


class VertexUnreachableError(KeyError):
    pass

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
                # self.weight_map[(u,v)] = w
                self.add_weight(u,v,w)
                if w < 0:
                    self._has_neg_weights = True
            else:
                w = None
            self.adj_list[u].append(v)
            if undirected:
                self.adj_list[v].append(u)
                if w is not None:
                    # self.weight_map[(v,u)] = w
                    self.add_weight(v,u,w)

    @property
    def n_vertices(self):
        return self._nv

    @property
    def has_negative_weights(self):
        return self._has_neg_weights


    def add_weight(self, from_idx, to_idx, weight):
        self.weight_map[(from_idx,to_idx)] = weight

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

    def search(self, source_index, target_idx=None):

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

                    # End early if we have found the node we are looking for
                    if adj_index == target_idx:
                        return self

            self.state[index] = 'exited'

        if target_idx is not None:
            raise VertexUnreachableError("Could not reach target vertex {}".format(target_idx))

        return self

class FlowGraph(Graph):

    def __init__(self, vertices, edge_list, source_idx, sink_idx):
        super(FlowGraph, self).__init__(vertices, edge_list, undirected=False)
        self.flow_map = {}
        self.source_idx = source_idx
        self.sink_idx = sink_idx
        self._max_flow = 0

    def add_weight(self, v_from, v_to, weight):
        self.weight_map[(v_from,v_to)] = [weight, 0]


    def get_weight(self, v_from, v_to):
        return self.weight_map[(v_from, v_to)][0]


    def add_flow(self, v_from, v_to, flow):
        flow_data = self.weight_map[(v_from, v_to)]

        if flow_data[0] < flow_data[1] + flow:
            raise ValueError("flow exceeds capacity!")
        flow_data[1] += flow

        if v_to == self.sink_idx:
            self._max_flow += flow


    @property
    def max_flow(self):
        # Calculate the sum of all flow in to the sink.
        return self._max_flow

    @property
    def is_valid(self):
        # Make sure the conservation and capacity properties are satisfied
        flow_in = [0]*self.n_vertices
        flow_out = [0]*self.n_vertices

        # Calculate the flow in and out of each vertex
        for edge, cap_flow in self.weight_map.items():

            # Along the way, make sure that flow is positive and less than capacity
            capacity, flow = cap_flow
            if capacity < flow or flow < 0:
                return False

            flow_in[edge[1]] += cap_flow[1]
            flow_out[edge[0]] += cap_flow[1]

        # Validate that in/out flows are the same except for sink/source
        flow_in[self.source_idx] = flow_out[self.source_idx]
        flow_out[self.sink_idx] = flow_in[self.sink_idx]

        return all(f_in == f_out for f_in, f_out in zip(flow_in, flow_out))

    def calc_residual_network(self):

        edge_list = []

        for edge, cap_and_flow in self.weight_map.items():
            # Calculate the residual capacity
            flow = cap_and_flow[1]
            res_cap = cap_and_flow[0] - flow

            # Add it to the edge list
            if res_cap > 0:
                edge_list.append([edge[0], edge[1], res_cap])

            # If flowing from u to v, there is capacity from v to u
            if flow > 0:
                edge_list.append([edge[1], edge[0], res_cap])


        res_graph = Graph(list(self.vertices), edge_list)

        return res_graph

