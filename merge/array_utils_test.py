import unittest
from array_utils import (find_first_unsorted_index, swap_k_elements,
                         rotate_k_left, invert, selection_sort, is_sorted)


class FindFirstUnsortedIndexTests(unittest.TestCase):
    def test_unordered(self):
        A = [0, 3, 6, 1, 2, 4, 5, 7, 8]
        self.assertEqual(find_first_unsorted_index(A, 0, len(A)), 3)
    def test_all_sorted(self):
        A = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.assertEqual(find_first_unsorted_index(A, 0, len(A)), len(A))
    def test_unordered_middle(self):
        A = [0, 3, 6, 1, 2, 4, 5, 7, 8]
        self.assertEqual(find_first_unsorted_index(A, start=1, length=5), 3)
    def test_sorted_middle(self):
        A = [1, 0, 2, 3, 4, 5, 6, 7, 8]
        self.assertEqual(find_first_unsorted_index(A, start=1, length=5), 6)

class SwapKElementsTests(unittest.TestCase):
    def test_swap_middle(self):
        A = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        swap_k_elements(A, start=2, target=6, k=3)
        self.assertEqual(A, [0, 1, 6, 7, 8, 5, 2, 3, 4, 9])
    def test_swap_self(self):
        A = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        swap_k_elements(A, 0, target=0, k=len(A))
        self.assertEqual(A, [0, 1, 2, 3, 4, 5, 6, 7, 8])

class RotateKLeftTests(unittest.TestCase):
    def test_rotate_0_identity(self):
        A = [0, 1, 2, 3, 4, 5]
        rotate_k_left(A, 0, len(A), k=0)
        self.assertEqual(A, [0, 1, 2, 3, 4, 5])
    def test_rotate_n_identity(self):
        A = [0, 1, 2, 3, 4, 5]
        rotate_k_left(A, 0, len(A), k=len(A))
        self.assertEqual(A, [0, 1, 2, 3, 4, 5])
    def test_rotate_1(self):
        A = [0, 1, 2, 3, 4, 5]
        rotate_k_left(A, 0, len(A), k=1)
        self.assertEqual(A, [1, 2, 3, 4, 5, 0])
    def test_rotate_3(self):
        A = [0, 1, 2, 3, 4, 5]
        rotate_k_left(A, 0, len(A), k=3)
        self.assertEqual(A, [3, 4, 5, 0, 1, 2])
    def test_rotate_1_middle(self):
        A = [0, 1, 2, 3, 4, 5, 6]
        rotate_k_left(A, start=2, length=3, k=1)
        self.assertEqual(A, [0, 1, 3, 4, 2, 5, 6])

class InvertTests(unittest.TestCase):
    def test_invert_full_array(self):
        A = [0, 1, 2, 3, 4, 5]
        invert(A, 0, len(A))
        self.assertEqual(A, [5, 4, 3, 2, 1, 0])
    def test_invert_middle(self):
        A = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        invert(A, start=3, length=3)
        self.assertEqual(A, [0, 1, 2, 5, 4, 3, 6, 7, 8, 9])

class SelectionSortTests(unittest.TestCase):
    def test_sort_all(self):
        A = [5, 4, 3, 2, 1, 0]
        compare_fn = lambda i, j: A[i] < A[j]
        def swap(i, j):
            A[i], A[j] = A[j], A[i]
        selection_sort(len(A), compare_fn, swap)
        self.assertEqual(A, [0, 1, 2, 3, 4, 5])
    def test_sort_middle(self):
        start=1
        A = [5, 4, 3, 2, 1, 0]
        def swap_fn(i, j): A[start+i], A[start+j] = A[start+j], A[start+i]
        compare_fn = lambda i, j: A[start+i] < A[start+j]
        selection_sort(length=4, compare_fn=compare_fn, swap_fn=swap_fn)
        self.assertEqual(A, [5, 1, 2, 3, 4, 0])

class IsSortedTests(unittest.TestCase):
    def test_sorted(self):
        A = [0, 1, 2, 3, 4, 5]
        self.assertTrue(is_sorted(A, 0, len(A)))
    def test_unsorted(self):
        A = [0, 1, 2, 5, 4, 3]
        self.assertFalse(is_sorted(A, 0, len(A)))
    def test_sorted_middle(self):
        A = [5, 1, 2, 3, 4, 0]
        self.assertTrue(is_sorted(A, start=1, length=4))
    def test_unsorted_middle(self):
        A = [0, 1, 2, 4, 3, 5]
        self.assertFalse(is_sorted(A, start=1, length=4))
    def test_empty(self):
        A = []
        self.assertTrue(is_sorted(A, 0, len(A)))


if __name__ == "__main__":
    unittest.main()
