"""
Given n, how many structurally unique BST's (binary search trees) that store values 1 ... n?

Example:

Input: 3
Output: 5
Explanation:
Given n = 3, there are a total of 5 unique BST's:

   1         3     3      2      1
    \       /     /      / \      \
     3     2     1      1   3      2
    /     /       \                 \
   2     1         2                 3
"""

# Thought process:
# (1) Loop over which node is the root.
# (2) Dynamic programming problem?
# (3) Because it is a partition problem
# (4) Like, you can treat it as how many ways the left and right tree can be allocated
# (5) Recursion is: T(1) = 1, T(2) = 2,
#    T(3) = T(2) + T(1)*T(1) + T(2)
#    T(n) = \sum_{i=1}^{n-1} T(i)*T(n-i)

from unittest import TestCase

def unique_bsts(n):
    if n <= 2:
        return n

    n_unique = [0]*(n+1)
    n_unique[0] = n_unique[1] =1
    n_unique[2] = 2

    for i in range(3, n+1):
        for j in range(1, i+1):
            n_unique[i] += n_unique[j-1]*n_unique[i-j]
            #T(3) = T(0)*T(2) + T(1)*T(1) + T(2)*T(0)

    return n_unique[n]



class TestUniqueBST(TestCase):

    def test_unique(self):
        self.assertEqual(unique_bsts(1), 1)
        self.assertEqual(unique_bsts(2), 2)
        self.assertEqual(unique_bsts(3), 5)
        self.assertEqual(unique_bsts(4), 14)