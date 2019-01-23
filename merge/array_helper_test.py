import unittest
from array_helper import (find_first_unsorted_index, swap_k_elements,
                          rotate_k_left, invert, selection_sort)


class FindFirstUnsortedIndex(unittest.TestCase):
    def test_unordered(self):
        X = [0, 3, 6, 1, 2, 4, 5, 7, 8]
        self.assertEqual(find_first_unsorted_index(X), 3)
    def test_all_sorted(self):
        X = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.assertEqual(find_first_unsorted_index(X), len(X))

class SwapKElements(unittest.TestCase):
    def test_swap_middle(self):
        X = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        swap_k_elements(X, start=2, k=3, target=6)
        self.assertEqual(X, [0, 1, 6, 7, 8, 5, 2, 3, 4, 9])
    def test_swap_self(self):
        X = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        swap_k_elements(X, 0, len(X), target=0)
        self.assertEqual(X, [0, 1, 2, 3, 4, 5, 6, 7, 8])

class RotateKLeftTests(unittest.TestCase):
    def test_rotate_0_identity(self):
        X = [0, 1, 2, 3, 4, 5]
        rotate_k_left(X, 0, len(X), k=0)
        self.assertEqual(X, [0, 1, 2, 3, 4, 5])
    def test_rotate_n_identity(self):
        X = [0, 1, 2, 3, 4, 5]
        rotate_k_left(X, 0, len(X), k=len(X))
        self.assertEqual(X, [0, 1, 2, 3, 4, 5])
    def test_rotate_1(self):
        X = [0, 1, 2, 3, 4, 5]
        rotate_k_left(X, 0, len(X), k=1)
        self.assertEqual(X, [1, 2, 3, 4, 5, 0])
    def test_rotate_3(self):
        X = [0, 1, 2, 3, 4, 5]
        rotate_k_left(X, 0, len(X), k=3)
        self.assertEqual(X, [3, 4, 5, 0, 1, 2])
    def test_rotate_1_middle(self):
        X = [0, 1, 2, 3, 4, 5, 6]
        rotate_k_left(X, start=2, length=3, k=1)
        self.assertEqual(X, [0, 1, 3, 4, 2, 5, 6])

class InvertTests(unittest.TestCase):
    def test_invert_full_array(self):
        X = [0, 1, 2, 3, 4, 5]
        invert(X, 0, len(X))
        self.assertEqual(X, [5, 4, 3, 2, 1, 0])
    def test_invert_middle(self):
        X = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        invert(X, start=3, length=3)
        self.assertEqual(X, [0, 1, 2, 5, 4, 3, 6, 7, 8, 9])

class SelectionSortTests(unittest.TestCase):
    def test_sort_all(self):
        X = [5, 4, 3, 2, 1, 0]
        selection_sort(X, 0, len(X))
        self.assertEqual(X, [0, 1, 2, 3, 4, 5])
    def test_sort_middle(self):
        X = [5, 4, 3, 2, 1, 0]
        selection_sort(X, start=1, length=4)
        self.assertEqual(X, [5, 1, 2, 3, 4, 0])


if __name__ == "__main__":
    unittest.main()
