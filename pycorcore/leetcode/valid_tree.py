"""
Given n nodes labeled from 0 to n - 1 and a list of undirected edges (each edge is a pair of nodes),
check if these edges form a valid tree.
"""


# Thought process:
# Properties of a valid tree:
# (1) No loops.
# (2) All of the nodes are found.
# (3) No self loops.
# (4) Only one edge into each node.

# Basic strategy:
# (1) loop over all edges (from, to)
# (2) check if a self loop - retun False
# (3) Check if "to" vertex has already been found. - if so return False
#    - Add the "to" vertex to a set
# (4) We need to have n-1 in our "to" set at the end, since one of them is the root.

def is_valid_tree(n_nodes, edge_list):

    found_nodes = set([])

    for (v_from, v_to) in edge_list:
        # Detect a self-loop
        if v_from == v_to:
            return False

        # If this node was previously found, there is a loop or it has multiple parents
        if v_to in found_nodes:
            return False

        found_nodes.add(v_to)

    # Every node must have something pointing to it, except the root.
    return len(found_nodes) == (n_nodes-1)


def test_valid():
    print("Unit Testing Tree Validator...")

    n_nodes = 7
    edge_list = [(4,2), (4,6), (2,1), (2,3), (6, 5), (6, 7)]
    is_valid = is_valid_tree(n_nodes, edge_list)
    assert is_valid, "Called valid tree invalid!"

    edge_list = [(4,2), (4,6), (2,1), (2,3), (6, 5), (6, 7), (7,4)]
    is_valid = is_valid_tree(n_nodes, edge_list)
    assert not(is_valid), "Called cyclic graph a valid tree!"

    edge_list = [(4,2), (4,6), (2,1), (2,3), (6, 5), (6, 7), (6,6)]
    is_valid = is_valid_tree(n_nodes, edge_list)
    assert not(is_valid), "Called self-edge node a valid tree!"

    edge_list = [(4,2), (4,6), (2,1), (2,3), (6, 5)]
    is_valid = is_valid_tree(n_nodes, edge_list)
    assert not(is_valid), "Called incomplete tree valid"

    edge_list = [(4,2), (4,6), (2,1), (2,3), (6, 5), (6, 7), (2, 7)]
    is_valid = is_valid_tree(n_nodes, edge_list)
    assert not(is_valid), "Called multiple parent node a valid tree!"

    edge_list = [(4,2), (4,6), (2,1), (2,3), (6, 5), (6, 7), (7, 6)]
    is_valid = is_valid_tree(n_nodes, edge_list)
    assert not(is_valid), "Called interior cycle a valid tree!"

    print("All Passed!")

if __name__ == "__main__":
    test_valid()


