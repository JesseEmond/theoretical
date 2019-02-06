import unittest
from array_utils import is_sorted
from merge import (_point_to_kth_biggest, _move_k_biggest_elements_to_end,
                   _move_last_elements_to_end, SubarrayPointers)


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


if __name__ == "__main__":
    unittest.main()
