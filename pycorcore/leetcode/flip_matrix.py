"""
Given a m x n binary matrix mat. In one step, you can choose one cell and flip it and all the four neighbours of it if they exist (Flip is changing 1 to 0 and 0 to 1). A pair of cells are called neighboors if they share one edge.

Return the minimum number of steps required to convert mat to a zero matrix or -1 if you cannot.

Binary matrix is a matrix with all cells equal to 0 or 1 only.

Zero matrix is a matrix with all cells equal to 0.



Example 1:


Input: mat = [[0,0],[0,1]]
Output: 3
Explanation: One possible solution is to flip (1, 0) then (0, 1) and finally (1, 1) as shown.
Example 2:

Input: mat = [[0]]
Output: 0
Explanation: Given matrix is a zero matrix. We don't need to change it.
Example 3:

Input: mat = [[1,1,1],[1,0,1],[0,0,0]]
Output: 6
Example 4:

Input: mat = [[1,0,0],[1,0,0]]
Output: -1
Explanation: Given matrix can't be a zero matrix


Constraints:

m == mat.length
n == mat[0].length
1 <= m <= 3
1 <= n <= 3
mat[i][j] is 0 or 1.
"""

# Thought process:
# Treat the matrix like a binary number. [[0,1], [0,0]] -> 0100
# Treat these as numbered nodes in a graph
# We use the flip rule to construct edges...
# Do a breadth first search.

# Hard part seems in constructing the flip rule...
# For an m x n matrix, and flipping index i, you attempt to flip i, i-1, i+1, i-n, i+n, assuming that they exist.
# And those represent your edges, which you can compute on the fly as you do the search.
# You need to keep track of nodes you have already seen, best done with an integer rep in a set.
# When you add to the queue, you will want the flip length along with it.

from unittest import TestCase
import copy

def mat_to_int(mat):

    val = 0
    base = 1
    for row in mat:
        for col in row:
            if col:
                val += base
            base *=2
    return val


def min_flips(mat):

    n_rows = len(mat)
    n_cols = len(mat[0])
    n_array = n_rows*n_cols

    given_value = mat_to_int(mat)
    if given_value == 0:
        return 0

    queue = [(mat, 0)]

    # Keep track of which matrices we have seen
    visited = set([given_value])

    while len(queue) != 0:
        current_mat, n_flips = queue.pop(0)

        for cen_idx in range(n_array):

            r = int(cen_idx/n_cols)
            c = cen_idx % n_cols

            # Perform the flips
            next_mat = copy.deepcopy(current_mat)
            next_mat[r][c] = (next_mat[r][c]+1)%2
            if r-1 >=0:
                next_mat[r-1][c] = (next_mat[r-1][c]+1)%2
            if r+1 < n_rows:
                next_mat[r+1][c] = (next_mat[r+1][c]+1)%2
            if c-1 >=0:
                next_mat[r][c-1] = (next_mat[r][c-1]+1)%2
            if c+1 < n_cols:
                next_mat[r][c+1] = (next_mat[r][c+1]+1)%2

            array_val = mat_to_int(next_mat)

            # Check if we are done
            if array_val == 0:
                return n_flips+1
            elif array_val not in visited:
                queue.append((next_mat, n_flips+1))
                visited.add(array_val)

    return -1

class TestFlip(TestCase):

    def test_flip(self):

        self.assertEqual(min_flips([[0,0],[0,1]]), 3)
        self.assertEqual(min_flips([[0]]), 0)
        self.assertEqual(min_flips([[1,1,1],[1,0,1],[0,0,0]]), 6)
        self.assertEqual(min_flips([[1,0,0],[1,0,0]]), -1)
