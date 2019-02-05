import unittest
from array_utils import is_sorted
from merge import (_point_to_kth_biggest, _move_k_biggest_elements_to_end,
                   SubarrayPointers)


def pointers_for(xs, ys, buffer_=None):
    """Creates pointers within A for the given 'xs' and 'ys'."""
    buffer_ = buffer_ or []
    return SubarrayPointers(xs_start=0, xs_length=len(xs), ys_start=len(xs),
                            ys_length=len(ys), buffer_start=len(xs)+len(ys),
                            buffer_length=len(buffer_))



class PointToKthBiggestTests(unittest.TestCase):
    def test_kth_biggest_in_xs(self):
        xs = [5, 7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        A = xs + ys
        self.assertEqual((1, 8),
                         _point_to_kth_biggest(A, pointers_for(xs, ys), k=4))
    def test_kth_biggest_in_ys(self):
        xs = [5, 7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        A = xs + ys
        self.assertEqual((1, 7),
                         _point_to_kth_biggest(A, pointers_for(xs, ys), k=5))
    def test_kth_xs_exhausted(self):
        xs = [7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        A = xs + ys
        self.assertEqual((0, 6),
                         _point_to_kth_biggest(A, pointers_for(xs, ys), k=5))
    def test_kth_ys_exhausted(self):
        xs = [1, 7, 10]
        ys = [8]
        A = xs + ys
        self.assertEqual((1, 3),
                         _point_to_kth_biggest(A, pointers_for(xs, ys), k=3))
    def test_kth_no_large_in_xs(self):
        xs = [1, 2, 3]
        ys = [4, 6, 8]
        A = xs + ys
        self.assertEqual((3, 4),
                         _point_to_kth_biggest(A, pointers_for(xs, ys), k=2))
    def test_kth_no_large_in_ys(self):
        xs = [4, 6, 8]
        ys = [1, 2, 3]
        A = xs + ys
        self.assertEqual((1, 6),
                         _point_to_kth_biggest(A, pointers_for(xs, ys), k=2))


# TODO: move most of these to MoveLastElementsToEndTests
class MoveKBiggestElementsToEndTests(unittest.TestCase):
    # TODO: move to explicit tests instead
    def _check_guarantees(self, A, xs, ys, new_pointers, k):
        biggest_k = list(sorted(A))[-k:][:k]  # :k to handle k=0
        buf = A[new_pointers.buffer_start:
                new_pointers.buffer_start+new_pointers.buffer_length]
        self.assertCountEqual(buf, biggest_k)  # end contains k biggest elems
        new_xs = A[new_pointers.xs_start:
                   new_pointers.xs_start+new_pointers.xs_length]
        new_ys = A[new_pointers.ys_start:
                   new_pointers.ys_start+new_pointers.ys_length]
        self.assertEqual(len(new_xs)+len(new_ys), len(A)-k)
        self.assertEqual(len(buf), k)
        self.assertTrue(is_sorted(new_xs, 0, len(new_xs)),
                        "xs not sorted: %s" % new_xs)
        self.assertTrue(is_sorted(new_ys, 0, len(new_ys)),
                        "ys not sorted: %s" % new_ys)
    def test_normal(self):
        xs = [5, 7, 9, 10]
        ys = [1, 3, 4, 6, 8]
        A = xs + ys
        new_pointers = _move_k_biggest_elements_to_end(A, pointers_for(xs, ys),
                                                       k=3)
        self._check_guarantees(A, xs, ys, new_pointers, k=3)
        self.assertEqual(SubarrayPointers(xs_start=0, xs_length=2,
                                          ys_start=2, ys_length=4,
                                          buffer_start=6, buffer_length=3),
                         new_pointers)
    def test_biggest_all_in_xs(self):
        xs = [5, 8, 9, 10]
        ys = [1, 3, 4, 6, 7]
        A = xs + ys
        new_pointers = _move_k_biggest_elements_to_end(A, pointers_for(xs, ys),
                                                       k=3)
        self._check_guarantees(A, xs, ys, new_pointers, k=3)
        self.assertEqual(SubarrayPointers(xs_start=0, xs_length=1,
                                          ys_start=1, ys_length=5,
                                          buffer_start=6, buffer_length=3),
                         new_pointers)
    def test_biggest_all_in_ys(self):
        xs = [4, 5, 6, 7]
        ys = [1, 3, 8, 9, 10]
        A = xs + ys
        new_pointers = _move_k_biggest_elements_to_end(A, pointers_for(xs, ys),
                                                       k=3)
        self._check_guarantees(A, xs, ys, new_pointers, k=3)
        self.assertEqual(SubarrayPointers(xs_start=0, xs_length=4,
                                          ys_start=4, ys_length=2,
                                          buffer_start=6, buffer_length=3),
                         new_pointers)
    def test_xs_less_than_k_elements(self):
        xs = [4, 5, 6, 7]
        ys = [1, 3, 8, 9, 10]
        A = xs + ys
        new_pointers = _move_k_biggest_elements_to_end(A, pointers_for(xs, ys),
                                                       k=5)
        self._check_guarantees(A, xs, ys, new_pointers, k=5)
        self.assertEqual(SubarrayPointers(xs_start=0, xs_length=2,
                                          ys_start=2, ys_length=2,
                                          buffer_start=4, buffer_length=5),
                         new_pointers)
    def test_ys_less_than_k_elements(self):
        xs = [4, 5, 6, 7, 11, 12, 13]
        ys = [1, 3, 8, 9, 10]
        A = xs + ys
        new_pointers = _move_k_biggest_elements_to_end(A, pointers_for(xs, ys),
                                                       k=6)
        self._check_guarantees(A, xs, ys, new_pointers, k=6)
        self.assertEqual(SubarrayPointers(xs_start=0, xs_length=4,
                                          ys_start=4, ys_length=2,
                                          buffer_start=6, buffer_length=6),
                         new_pointers)
    def test_xs_exhausted(self):
        xs = [4, 5, 6, 7]
        ys = [1, 2, 3]
        A = xs + ys
        new_pointers = _move_k_biggest_elements_to_end(A, pointers_for(xs, ys),
                                                       k=5)
        self._check_guarantees(A, xs, ys, new_pointers, k=5)
        self.assertEqual(SubarrayPointers(xs_start=0, xs_length=0,
                                          ys_start=0, ys_length=2,
                                          buffer_start=2, buffer_length=5),
                         new_pointers)
    def test_ys_exhausted(self):
        xs = [1, 2, 3]
        ys = [4, 5, 6, 7]
        A = xs + ys
        new_pointers = _move_k_biggest_elements_to_end(A, pointers_for(xs, ys),
                                                       k=5)
        self._check_guarantees(A, xs, ys, new_pointers, k=5)
        self.assertEqual(SubarrayPointers(xs_start=0, xs_length=2,
                                          ys_start=2, ys_length=0,
                                          buffer_start=2, buffer_length=5),
                         new_pointers)
    def test_k_0(self):
        xs = [4, 5, 6, 7]
        ys = [1, 3, 8, 9, 10]
        A = xs + ys
        new_pointers = _move_k_biggest_elements_to_end(A, pointers_for(xs, ys),
                                                       k=0)
        self._check_guarantees(A, xs, ys, new_pointers, k=0)
        self.assertEqual(SubarrayPointers(xs_start=0, xs_length=4,
                                          ys_start=4, ys_length=5,
                                          buffer_start=9,
                                          buffer_length=0),
                         new_pointers)


if __name__ == "__main__":
    unittest.main()
