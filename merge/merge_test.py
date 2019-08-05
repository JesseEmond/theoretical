import unittest
from array_utils import is_sorted
from merge import (_point_to_kth_biggest, _merge_into_target,
                   _move_k_biggest_elements_to_end, _move_last_elements_to_end,
                   merge_inplace, SubarrayPointers)


class PointToKthBiggestTests(unittest.TestCase):
    def test_kth_biggest_in_xs(self):
        xs = [5, 7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=5,
                                    buffer_start=11, buffer_length=0)
        self.assertEqual(_point_to_kth_biggest(A, pointers, k=4), (3, 10))
    def test_kth_biggest_in_ys(self):
        xs = [5, 7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=5,
                                    buffer_start=11, buffer_length=0)
        self.assertEqual(_point_to_kth_biggest(A, pointers, k=5), (3, 9))
                         
    def test_kth_xs_exhausted(self):
        xs = [7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=3,
                                    ys_start=5, ys_length=5,
                                    buffer_start=10, buffer_length=0)
        self.assertEqual(_point_to_kth_biggest(A, pointers, k=5), (2, 8))
    def test_kth_ys_exhausted(self):
        xs = [1, 7, 10]
        ys = [8]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=3,
                                    ys_start=5, ys_length=1,
                                    buffer_start=6, buffer_length=0)
        self.assertEqual(_point_to_kth_biggest(A, pointers, k=3), (3, 5))
    def test_kth_no_large_in_xs(self):
        xs = [1, 2, 3]
        ys = [4, 6, 8]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=3,
                                    ys_start=5, ys_length=3,
                                    buffer_start=8, buffer_length=0)
        self.assertEqual(_point_to_kth_biggest(A, pointers, k=2), (5, 6))
    def test_kth_no_large_in_ys(self):
        xs = [4, 6, 8]
        ys = [1, 2, 3]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=3,
                                    ys_start=5, ys_length=3,
                                    buffer_start=8, buffer_length=0)
        self.assertEqual(_point_to_kth_biggest(A, pointers, k=2), (3, 8))

class MoveLastElementsToEndTests(unittest.TestCase):
    def test_move_both_xs_ys(self):
        xs = [5, 7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=5,
                                    buffer_start=11, buffer_length=0)
        new_pointers = _move_last_elements_to_end(A, pointers,
                                                  xs_to_move=2, ys_to_move=3)
        self.assertEqual(A, [100, 101, 5, 7, 1, 3, 9, 10, 4, 6, 8, 30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=2,
                                          ys_start=4, ys_length=2,
                                          buffer_start=6, buffer_length=5))
    def test_move_only_xs(self):
        xs = [5, 7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=5,
                                    buffer_start=11, buffer_length=0)
        new_pointers = _move_last_elements_to_end(A, pointers,
                                                  xs_to_move=2, ys_to_move=0)
        self.assertEqual(A, [100, 101, 5, 7, 1, 3, 4, 6, 8, 9, 10, 30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=2,
                                          ys_start=4, ys_length=5,
                                          buffer_start=9, buffer_length=2))
    def test_move_only_ys(self):
        xs = [5, 7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=5,
                                    buffer_start=11, buffer_length=0)
        new_pointers = _move_last_elements_to_end(A, pointers,
                                                  xs_to_move=0, ys_to_move=3)
        self.assertEqual(A, [100, 101, 5, 7, 9, 10, 1, 3, 4, 6, 8, 30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=4,
                                          ys_start=6, ys_length=2,
                                          buffer_start=8, buffer_length=3))
    def test_move_all(self):
        xs = [5, 7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=5,
                                    buffer_start=11, buffer_length=0)
        new_pointers = _move_last_elements_to_end(A, pointers,
                                                  xs_to_move=4, ys_to_move=5)
        self.assertEqual(A, [100, 101, 5, 7, 9, 10, 1, 3, 4, 6, 8, 30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=0,
                                          ys_start=2, ys_length=0,
                                          buffer_start=2, buffer_length=9))
    def test_move_nothing(self):
        xs = [5, 7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=5,
                                    buffer_start=11, buffer_length=0)
        new_pointers = _move_last_elements_to_end(A, pointers,
                                                  xs_to_move=0, ys_to_move=0)
        self.assertEqual(A, [100, 101, 5, 7, 9, 10, 1, 3, 4, 6, 8, 30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=4,
                                          ys_start=6, ys_length=5,
                                          buffer_start=11, buffer_length=0))
    def test_move_both_with_existing_buffer(self):
        xs = [5, 7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        buffer_ = [15, 16]
        A = [100, 101] + xs + ys + buffer_ + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=5,
                                    buffer_start=11, buffer_length=2)
        new_pointers = _move_last_elements_to_end(A, pointers,
                                                  xs_to_move=2, ys_to_move=3)
        self.assertEqual(A, [100, 101, 5, 7, 1, 3, 9, 10, 4, 6, 8, 15, 16,
                             30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=2,
                                          ys_start=4, ys_length=2,
                                          buffer_start=6, buffer_length=7))


class MoveKBiggestElementsToEndTests(unittest.TestCase):
    def test_normal(self):
        xs = [5, 7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=5,
                                    buffer_start=11, buffer_length=0)
        new_pointers = _move_k_biggest_elements_to_end(A, pointers, k=3)
        self.assertEqual(A, [100, 101, 5, 7, 1, 3, 4, 6, 9, 10, 8, 30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=2,
                                          ys_start=4, ys_length=4,
                                          buffer_start=8, buffer_length=3))
    def test_biggest_all_in_xs(self):
        xs = [5, 8, 9, 10]
        ys = [1, 3, 4, 6, 7]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=5,
                                    buffer_start=11, buffer_length=0)
        new_pointers = _move_k_biggest_elements_to_end(A, pointers, k=3)
        self.assertEqual(A, [100, 101, 5, 1, 3, 4, 6, 7, 8, 9, 10, 30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=1,
                                          ys_start=3, ys_length=5,
                                          buffer_start=8, buffer_length=3))
    def test_biggest_all_in_ys(self):
        xs = [4, 5, 6, 7]
        ys = [1, 3, 8, 9, 10]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=5,
                                    buffer_start=11, buffer_length=0)
        new_pointers = _move_k_biggest_elements_to_end(A, pointers, k=3)
        self.assertEqual(A, [100, 101, 4, 5, 6, 7, 1, 3, 8, 9, 10, 30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=4,
                                          ys_start=6, ys_length=2,
                                          buffer_start=8, buffer_length=3))
    def test_xs_less_than_k_elements(self):
        xs = [4, 5, 6, 7]
        ys = [1, 3, 8, 9, 10]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=5,
                                    buffer_start=11, buffer_length=0)
        new_pointers = _move_k_biggest_elements_to_end(A, pointers, k=5)
        self.assertEqual(A, [100, 101, 4, 5, 1, 3, 6, 7, 8, 9, 10, 30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=2,
                                          ys_start=4, ys_length=2,
                                          buffer_start=6, buffer_length=5))
    def test_ys_less_than_k_elements(self):
        xs = [4, 5, 6, 7, 11, 12, 13]
        ys = [1, 3, 8, 9, 10]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=7,
                                    ys_start=9, ys_length=5,
                                    buffer_start=14, buffer_length=0)
        new_pointers = _move_k_biggest_elements_to_end(A, pointers, k=6)
        self.assertEqual(A, [100, 101, 4, 5, 6, 7, 1, 3, 11, 12, 13, 8, 9, 10,
                             30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=4,
                                          ys_start=6, ys_length=2,
                                          buffer_start=8, buffer_length=6))
    def test_xs_exhausted(self):
        xs = [4, 5, 6, 7]
        ys = [1, 2, 3]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=3,
                                    buffer_start=9, buffer_length=0)
        new_pointers = _move_k_biggest_elements_to_end(A, pointers, k=5)
        self.assertEqual(A, [100, 101, 1, 2, 4, 5, 6, 7, 3, 30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=0,
                                          ys_start=2, ys_length=2,
                                          buffer_start=4, buffer_length=5))
    def test_ys_exhausted(self):
        xs = [1, 2, 3]
        ys = [4, 5, 6, 7]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=3,
                                    ys_start=5, ys_length=4,
                                    buffer_start=9, buffer_length=0)
        new_pointers = _move_k_biggest_elements_to_end(A, pointers, k=5)
        self.assertEqual(A, [100, 101, 1, 2, 3, 4, 5, 6, 7, 30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=2,
                                          ys_start=4, ys_length=0,
                                          buffer_start=4, buffer_length=5))
    def test_k_0(self):
        xs = [4, 5, 6, 7]
        ys = [1, 3, 8, 9, 10]
        A = [100, 101] + xs + ys + [30, 31, 32]
        pointers = SubarrayPointers(xs_start=2, xs_length=4,
                                    ys_start=6, ys_length=5,
                                    buffer_start=11, buffer_length=0)
        new_pointers = _move_k_biggest_elements_to_end(A, pointers, k=0)
        self.assertEqual(A, [100, 101, 4, 5, 6, 7, 1, 3, 8, 9, 10, 30, 31, 32])
        self.assertEqual(new_pointers,
                         SubarrayPointers(xs_start=2, xs_length=4,
                                          ys_start=6, ys_length=5,
                                          buffer_start=11, buffer_length=0))

class MergeIntoTargetTests(unittest.TestCase):
    def test_sorted(self):
        A = [99] * 8 + [1, 2, 3, 4] + [5, 6, 7, 8]
        _merge_into_target(A, xs_start=8, ys_start=12, length=4, target=0)
        self.assertEqual(A, [1, 2, 3, 4, 5, 6, 7, 8] + [99] * 8)
    def test_sorted_swapped(self):
        A = [99] * 8 + [5, 6, 7, 8] + [1, 2, 3, 4]
        _merge_into_target(A, xs_start=8, ys_start=12, length=4, target=0)
        self.assertEqual(A, [1, 2, 3, 4, 5, 6, 7, 8] + [99] * 8)
    def test_interleaved(self):
        A = [1, 3, 5, 7] + [2, 4, 6, 8] + [99] * 8 
        _merge_into_target(A, xs_start=0, ys_start=4, length=4, target=8)
        self.assertEqual(A, [99] * 8 + [1, 2, 3, 4, 5, 6, 7, 8])
    def test_target_ys_half_overlap(self):
        A = [99] * 4 + [1, 3, 5, 7] + [2, 4, 6, 8]
        _merge_into_target(A, xs_start=8, ys_start=4, length=4, target=0)
        self.assertEqual(A, [1, 2, 3, 4, 5, 6, 7, 8] + [99] * 4)

class MergeInplaceTests(unittest.TestCase):
    def test_evens_left_odds_right(self):
        A = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
        merge_inplace(A)
        self.assertEqual(A, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_already_sorted(self):
        A = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        merge_inplace(A)
        self.assertEqual(A, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_evens_right_odds_left(self):
        A = [1, 3, 5, 7, 9, 0, 2, 4, 6, 8]
        merge_inplace(A)
        self.assertEqual(A, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_one_big_elem_left(self):
        A = [9, 0, 1, 2, 3, 4, 5, 6, 7, 8]
        merge_inplace(A)
        self.assertEqual(A, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_one_small_elem_right(self):
        A = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        merge_inplace(A)
        self.assertEqual(A, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_one_small_elem_left(self):
        A = [4, 0, 1, 2, 3, 5, 6, 7, 8, 9]
        merge_inplace(A)
        self.assertEqual(A, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_empty_array(self):
        A = []
        merge_inplace(A)
        self.assertEqual(A, [])
    def test_odds_left_evens_right_many_sizes(self):
        N = 50
        for left_length in range(N):
            for right_length in range(N):
                left = list(range(1, left_length * 2, 2))
                right = list(range(0, right_length * 2, 2))
                A = list(left + right)
                merge_inplace(A)
                self.assertEqual(A, sorted(left + right))


if __name__ == "__main__":
    unittest.main()
