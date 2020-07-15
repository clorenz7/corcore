"""
Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has properties:

1) Integers in each row are sorted from left to right.
2) The first integer of each row is greater than the last integer of the previous row.

For example, consider the following matrix:

[
  [1,   3,  5,  7],
  [10, 11, 16, 20],
  [23, 30, 34, 50]
]
Given target = 3, return true.
"""

# Basic strategy:
# Do a dual binary search:
#   (1) over the last entry in each row to pick the row
#        go in factors of 2: if less than last entry, check if greater than first value
#        if less than first value, pick row halfway between start and current row.
#   (2) binary search over the row to find the value once selected the row
#   (3) Overall should be O(lg n + lg m) since the Binary search is O(lg N) and we effectively do it twice


def search_sorted_matrix(matrix, value):

    # Assumes valid matrix...
    m = len(matrix)
    n = len(matrix[0])

    #---- Search for the correct row
    # Initial setup
    min_idx, max_idx = 0, m
    row_idx = int(m/2)
    idx_delta = max(int(m/4), 1)
    found_row_idx = None

    # Binary search for the row
    while found_row_idx is None:

        row = matrix[row_idx]
        # Do a binary search
        if value <= row[n-1]:
            if value >= row[0]:
                found_row_idx = row_idx
                break
            else:
                max_idx = row_idx
                row_idx -= idx_delta
                idx_delta = max(int(round(idx_delta/2)), 1)

        else: #  value > row[n-1]
            min_idx = row_idx +1
            row_idx += idx_delta
            idx_delta = max(int(round(idx_delta/2)), 1)

        # If we run out of room, return false
        if row_idx < min_idx or row_idx >= max_idx:
            return False

    #---- Search within the row
    # Initial setup
    min_idx, max_idx = 0, n
    col_idx = int(n/2)
    idx_delta = max(int(col_idx/4), 1)

    # Binary search for the value within the row
    while min_idx <= col_idx < max_idx:
        col_value = row[col_idx]
        if col_value == value:
            return True
        elif value < col_value:
            max_idx = col_idx
            col_idx -= idx_delta
        else:
            min_idx = row_idx+1
            col_idx += idx_delta

        idx_delta = max(int(round(col_idx/2)), 1)

    # If we get here, we failed to find the value
    return False


def test_search():

    matrix = [
        [1,   3,  5,  7],
        [10, 11, 16, 20],
        [23, 30, 34, 50]
    ]


    test_vals = [1, 3, 16, 20,  23, 80, 27, -1, 2, 15, 8]

    for val in test_vals:
        found = search_sorted_matrix(matrix, val)
        if found:
            print('Value {} was found!'.format(val))
        else:
            print('Value {} was not found!'.format(val))


if __name__ == "__main__":
    test_search()
