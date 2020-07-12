import warnings
import math

from .objects import DFS
from .objects import BFS, VertexUnreachableError
from .objects import FlowGraph

class NegativeCycleError(ValueError):
    pass


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


def calc_min_spanning_tree(graph):
    """
    Implementation of Kruskal's algorithm for finding a minimum spanning tree
    """

    vertex_set = set([])
    edge_set = []

    # Make each child its own root
    root = list(range(graph.n_vertices))

    # Sort the edges by weight
    sorted_edges = sorted(
        [ (graph.weight_map[key], key) for key in graph.weight_map ],
        key=lambda x: x[0]
    )

    for weight, edge in sorted_edges:
        u,v = edge
        # If the two edges have different roots, they are different trees
        if root[u] != root[v]:
            # The edge goes from u to v, so the root of u is the new root of v
            root[v] = root[u]

            vertex_set.union(edge)
            edge_set.append(edge)

    return edge_set


def relax(from_idx, to_idx, weight, shortest_paths, parents):
    """
    Performs path relaxation for an edge between two vertices

    The lists shortest_paths and parents are modified in-place.
    """
    new_path_length = shortest_paths[from_idx] + weight
    if new_path_length < shortest_paths[to_idx]:
        parents[to_idx] = from_idx
        shortest_paths[to_idx] = new_path_length


def shortest_paths(graph, source_idx):
    """
    input:
        graph: [Graph] object holding graph definition
        source_idx: [int] index of source vertex to find paths from
    output:
        shortest_paths: lengths of shortest path
        parents: index of parent vertex along shortest path

    raises: NegativeCycleError if a negative cycle is detected
    """
    use_dijkstra = not graph.has_negative_weights

    if use_dijkstra:
        warnings.warn("Dijkstra's algorithm not yet implemented! Using less efficient alg!")
        use_dijkstra = False

    if use_dijkstra:
        pass # Placeholder for when implemented
    else:
        # Initialize the placeholder arrays
        shortest_paths = [math.inf]*graph.n_vertices
        shortest_paths[source_idx] = 0
        parents = [graph.n_vertices]*graph.n_vertices
        parents[source_idx] = -graph.n_vertices

        # Use Bellman-Ford Algorithm
        n_passes = graph.n_vertices - 1

        # Run relax on each edge n_passes times...
        for _ in range(n_passes):
            # Loop over all edges
            for from_idx in range(graph.n_vertices):
                for to_idx in graph.get_edges(from_idx):
                    weight = graph.get_weight(from_idx, to_idx)

                    relax(from_idx, to_idx, weight, shortest_paths, parents)

        # Check for the existence of negative cycles by looping over each edge
        #  and seeing if you can reduce the path length
        for from_idx in range(graph.n_vertices):
            from_dist = shortest_paths[from_idx]
            for to_idx in graph.get_edges(from_idx):
                weight = graph.get_weight(from_idx, to_idx)
                if shortest_paths[to_idx] > from_dist + weight:
                    err_msg = f"Negative cycle detected on edge from {from_idx} to {to_idx}"
                    raise NegativeCycleError(err_msg)

    return shortest_paths, parents


def calc_max_flow(graph, source_idx, sink_idx):
    """
    Uses the Edmonds-Karp algorithm to find the max flow through a graph
    """

    res_graph = graph
    found_new_path = True

    while found_new_path:
        # Use BFS to find an augmenting path from source to sink.
        try:
            bfs = BFS(res_graph).search(source_idx, sink_idx)
        except VertexUnreachableError:
            found_new_path = False
            break

        # Calculate the flow along the path
        max_flow, path = _calc_flow(res_graph, bfs, source_idx, sink_idx)

        # Update the flow graph
        _add_flow_to_path(graph, path, max_flow)

        # Calculate the new residual network
        res_graph = graph.calc_residual_network()

    return graph.max_flow


def _calc_flow(flow_graph, bfs_result, source_idx, sink_idx):

    # Calculate the maximum possible flow
    parent = sink_idx
    current_idx = sink_idx
    path = [sink_idx]  # will reverse at end
    max_flow = math.inf

    while current_idx != source_idx:
        parent = bfs_result.parent[current_idx]
        path.append(parent)
        capacity = flow_graph.get_weight(parent, current_idx)
        max_flow = min(max_flow, capacity)
        current_idx = parent

    path.reverse()

    return max_flow, path

def _add_flow_to_path(graph, path, flow):

    for idx in range(len(path)-1):
        v_from = path[idx]
        v_to = path[idx+1]
        graph.add_flow(v_from, v_to, flow)







