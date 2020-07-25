"""
Given a matrix of m x n elements (m rows, n columns),
return all elements of the matrix in spiral order.

For example, given the following matrix:

[
 [ 1, 2, 3 ],
 [ 4, 5, 6 ],
 [ 7, 8, 9 ]
]
You should return [1,2,3,6,9,8,7,4,5].
"""


# Thought process:
# (1) Walk through the array, flipping from row to col to row to col
# (2) Keep track of min valid row/col index and march along until you hit it, and then "turn"
# (3) If you hit max col, turn right (i.e. iterate increasing), if max row turn right (iterate decreasing)
# if hit min col, iterate decreasing, if hit min row, iterate increasing. Heh- You are always turning right.
# (4) tricky part is changing direction. Probably will use a while loop. Could do it with a for loop
# and modular arithmetic and change the multiplier

from unittest import TestCase

def flatten_spiral_matrix(matrix):

    m = len(matrix)
    n = len(matrix[0]) # assumes non degenrate
    n_added = 0
    min_row_idx = 1  # crucial since we start with first row.
    min_col_idx = 0
    max_row_idx = m-1
    max_col_idx = n-1

    increment = 1
    r_idx = c_idx = 0
    incr_row = False

    flat_array = []


    while n_added < (m*n):

        flat_array.append(matrix[r_idx][c_idx])
        n_added += 1

        if incr_row:
            if r_idx == max_row_idx and increment == 1:
                incr_row = False
                max_row_idx -= 1
                c_idx -= 1
                increment *= -1  # change direction
            elif r_idx == min_row_idx and increment == -1:
                incr_row = False
                min_row_idx += 1
                c_idx +=1
                increment *= -1  # change direction
            else:
                r_idx += increment
        else:
            if c_idx == max_col_idx and increment == 1:
                incr_row = True
                max_col_idx -= 1
                # Increment stays the same (+1)
                r_idx += 1
            elif c_idx == min_col_idx and increment == -1:
                incr_row = True
                min_col_idx += 1
                # Increment stays the same
                r_idx -= 1
            else:
                c_idx += increment

    return flat_array


class TestSpiral(TestCase):

    def test_spiral(self):
        matrix = [
            [ 1, 2, 3 ],
            [ 4, 5, 6 ],
            [ 7, 8, 9 ]
        ]

        flat_array = flatten_spiral_matrix(matrix)
        self.assertEqual(flat_array, [1,2,3,6,9,8,7,4,5])

        matrix = [
            [ 1,  2,  3,  4 ],
            [ 5,  6,  7,  8 ],
            [ 9,  10, 11, 12],
            [ 13, 14, 15, 16]
        ]

        flat_array = flatten_spiral_matrix(matrix)
        self.assertEqual(flat_array, [1,2,3,4,8,12,16,15,14,13,9,5,6,7,11,10])

