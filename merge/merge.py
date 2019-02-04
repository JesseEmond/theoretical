"""
Merge function and related helpers to sort an array that has two sorted
subarrays in-place.

General notation:
    A: array to merge
    xs: first sorted subarray of A
    ys: second sorted subarray of A
    n: length of xs
    m: length of ys
    N: length of A (N=n+m)
    Z: floor(sqrt(N))
    O(1) memory: really means O(lg N) to allow constant amount of pointers
"""

import array_utils
import math


class SubarrayPointers:
    """Indices to both sorted subarrays within A, 'xs' and 'ys'.
    When set, also contains the indices to the unsorted buffer that we keep in
    the array."""
    def __init__(self, xs_start, xs_length, ys_start, ys_length,
                 buffer_start=None, buffer_length=None):
        assert xs_length >= 0 and ys_length >= 0 and \
            (buffer_length is None or buffer_length >= 0)
        self.xs_start = xs_start
        self.xs_length = xs_length
        self.ys_start = ys_start
        self.ys_length = ys_length
        self.buffer_start = buffer_start
        self.buffer_length = buffer_length


def merge_inplace(A):
    """Takes an array A that is assumed to have two subarrays that are sorted,
    and sorts it in-place.

    Complexity:
        - O(len(A)) time
        - O(1) space
    """
    N = len(A)
    Z = int(math.sqrt(N))
    ys_start = array_utils.find_first_unsorted_index(A, 0, N)
    xs_length = ys_start
    pointers = SubarrayPointers(xs_start=0, xs_length=xs_length,
                                ys_start=ys_start, ys_length=N-xs_length)
    assert array_utils.is_sorted(A, pointers.xs_start,
                                 pointers.xs_length) and \
           array_utils.is_sorted(A, pointers.ys_start,
                                 pointers.ys_length), \
           "Expected an array with two sorted subarrays."

    # 1) Move 'Z' biggest elements to 'buffer'.
    pointers = _move_k_biggest_elements_to_end(A, pointers, Z)
    # TODO(emond): what do I do when len(ys) <= Z? What happens?
    pass  # TODO


def _merge_inplace_with_buffer(A, pointers):
    """"""
    pass  # TODO(emond): implement


def _point_to_kth_biggest(A, pointers, k):
    """Takes two sorted subarrays within A and moves pointers in each subarray
    from both ends until one of them reaches the kth biggest element. The other
    pointer will point to the last element in that subarray which was part of
    the k-1 largest elements before that.
    In simpler terms, point to the end of xs and ys and move, in descending
    order, both pointers until we've moved k times.
    If none of the k biggest elements is in a particular subarray, its pointer
    will be on start+length of that subarray.
    If a subarray is exhausted, the pointer will remain on its start element.

    Returns:
        - (xs_pointer, ys_pointer)
          Tuple of pointers within 'xs' and 'ys', respectively, where one is a
          pointer to the kth biggest element and the other is a pointer to the 
          last of the k-1 biggest elements encountered in that subarray.

    Complexity:
        - O(|ys| + |xs|) time
        - O(1) space
    """
    assert k <= pointers.xs_length + pointers.ys_length
    x_pointer = pointers.xs_start + pointers.xs_length
    y_pointer = pointers.ys_start + pointers.ys_length
    for _ in range(k):
        if x_pointer <= pointers.xs_start:  # 'xs' exhausted
            y_pointer -= 1
        elif y_pointer <= pointers.ys_start:  # 'ys' exhausted
            x_pointer -= 1
        elif A[y_pointer-1] > A[x_pointer-1]:  # 'ys' has next largest element
            y_pointer -= 1
        else:
            x_pointer -= 1
    return (x_pointer, y_pointer)


def _move_k_biggest_elements_to_end(A, pointers, k):
    """Takes in an array A (that is split in two sorted subarrays
    [xs_start, xs_start+xs_length) and [ys_start, ys_start+ys_length)) and moves
    its top k biggest elements to the end of where 'ys' was (leaving them
    unsorted), at [ys_start+ys_length-k, ys_start+ys_length), which we call
    'buffer'. Assumes that 'xs' and 'ys' are contiguous and have, together, at
    least 'k' elements.
    Returns the indices for the mutated subarrays and the new buffer.

    Returns:
        A SubarrayPointers object, with the pointers to the modified 'xs', 'ys'
        and new 'buffer' regions set.

    Note:
        - Conceptually changes the lengths of 'xs' and 'ys' (as well as the
          index of new_ys_start), while keeping them sorted.
        - 'ys' becomes [new_ys_start, ys_start+ys_length-k), which might become
          an empty range (e.g. if |ys| < k and all 'ys' were part of the
          biggest elements)

    Guarantees after calling:
        - [xs_start, new_ys_start) will be sorted, and the new 'xs';
        - [new_ys_start, buffer_start] will be sorted, and the new 'ys';
        - [buffer_start, buffer_start+buffer_length) has the top k biggest
          elements from [xs_start, ys_start+ys_length), with no guarantees about
          their order.

    Complexity:
        - O(|ys| + |xs|) time
        - O(1) space
    """
    assert pointers.xs_length + pointers.ys_length >= k
    # How many elements from 'xs' are part of the 'k' biggest?
    xs_biggest_start, ys_biggest_start = _point_to_kth_biggest(A, pointers, k)
    # What will my new xs and ys look like?
    xs_biggest_length = pointers.ys_start - xs_biggest_start
    ys_biggest_length = (pointers.ys_start + pointers.ys_length
                         - ys_biggest_start)
    new_xs_length = pointers.xs_length - xs_biggest_length
    new_ys_start = new_xs_length
    new_ys_length = pointers.ys_length - ys_biggest_length
    # Rotate the last elements of 'xs' that belong in 'buffer' ("big xs") so
    # that they're on the right of the new 'ys', starting from:
    # |-----xs-----:--big-xs--|-----ys-----:--big-ys--|
    #              |<=========rotate-------|
    # to get:
    # |-----xs-----|-----ys-----|--big-xs--:--big-ys--|
    #                            ^^^^^^^ buffer ^^^^^^
    array_utils.rotate_k_left(A, start=xs_biggest_start,
                              length=xs_biggest_length + new_ys_length,
                              k=xs_biggest_length)
    return SubarrayPointers(xs_start=pointers.xs_start,
                            xs_length=new_xs_length,
                            ys_start=new_ys_start,
                            ys_length=new_ys_length,
                            buffer_start=new_ys_start + new_ys_length,
                            buffer_length=k)
