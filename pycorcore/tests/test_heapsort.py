from unittest import TestCase
from pycorcore.heapsort import heapsort


class TestHeap(TestCase):

    def test_heap(self):
        data = [1, 6, 3, 9, 8, 13, 4, 2, 5, 7, 0]
        sorted_data, heap = heapsort(data)
        self.assertEqual(sorted_data, sorted(data, reverse=True))
