"""
Finding the longest palindromic substring is a classic problem of coding interview.
"""

# My thoughts:
# (1) Dynamic programming?
# (2) Can walk back from end and build up the solution?
# (3) Need to identify the recursion...
# (4) Or do you just assume that the palindrome starts
#     at the center and attempt to build it out?
# (5) You can decide even or odd right away..
# (pick right char to define even, picking left is same as moving to left 1)
# (6) Start in center of string
# (7) Keep track of max value, can stop as reach the edge where no more room to go.
# (8) Easier to read if just do in one for loop

from unittest import TestCase

def longest_palindromic_substring(string):

    n_chars = len(string)
    longest = 1
    # Edge cases
    if n_chars <= 1:
        return n_chars
    elif n_chars == 2:
        return 2 if string[0] == string[1] else 1

    for idx in range(1, n_chars-1):
        # Initialize the "kernel": 2 chars or 3?
        if string[idx+1] == string[idx-1]:
            l_idx = idx-1
            r_idx = idx+1
            length = 3
        elif string[idx-1] == string[idx]:
            l_idx = idx-1
            r_idx = idx
            length = 2
        else:
            continue  # This is a 1 char palidrome
        # Loop to attempt adding chars to end
        valid = True
        while valid:
            # Check that we have not hit the end of the array
            if r_idx == n_chars or l_idx == 0:
                valid = False
            # Check that the strings match
            elif string[r_idx+1] == string[l_idx-1]:
                l_idx -= 1
                r_idx += 1
                length += 2
            else:
                valid = False

        if length > longest:
            longest = length

    return longest


class TestPalin(TestCase):

    def test_longest(self):
        self.assertEqual(7, longest_palindromic_substring('tacocat'))
        self.assertEqual(7, longest_palindromic_substring('atacocatdude'))
        self.assertEqual(4, longest_palindromic_substring('eatthepeepcandy'))
        self.assertEqual(2, longest_palindromic_substring('aa'))
        self.assertEqual(1, longest_palindromic_substring('ab'))


