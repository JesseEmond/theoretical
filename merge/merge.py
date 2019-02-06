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
    """Indices to both sorted subarrays within A, in order, 'xs', 'ys' and
    'buffer' (unsorted)."""
    def __init__(self, xs_start, xs_length, ys_start, ys_length,
                 buffer_start, buffer_length):
        assert xs_length >= 0 and ys_length >= 0 and buffer_length >= 0
        self.xs_start = xs_start
        self.xs_length = xs_length
        self.ys_start = ys_start
        self.ys_length = ys_length
        self.buffer_start = buffer_start
        self.buffer_length = buffer_length
    def __eq__(self, other):
        if isinstance(other, SubarrayPointers):
            return self._value() == other._value()
        return NotImplementedError
    def __repr__(self):
        return "xs:[%d, %d) ys:[%d, %d) buf:[%d, %d)" % (
                self.xs_start, self.xs_start+self.xs_length,
                self.ys_start, self.ys_start+self.ys_length,
                self.buffer_start, self.buffer_start+self.buffer_length
                )
    def _value(self):
        return (self.xs_start, self.xs_length, self.ys_start, self.ys_length,
                self.buffer_start, self.buffer_length)



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
    if ys_start == len(A): return  # already sorted!
    xs_length = ys_start
    pointers = SubarrayPointers(xs_start=0, xs_length=xs_length,
                                ys_start=ys_start, ys_length=N-xs_length,
                                buffer_start=ys_start+ys_length,
                                buffer_length=0)
    assert array_utils.is_sorted(A, pointers.xs_start,
                                 pointers.xs_length) and \
           array_utils.is_sorted(A, pointers.ys_start,
                                 pointers.ys_length), \
           "Expected an array with two sorted subarrays."

    # 1) Move 'Z' biggest elements to 'buffer'.
    pointers = _move_k_biggest_elements_to_end(A, pointers, Z)

    # 1.5) Make 'xs' and 'ys' multiples of 'Z'.
    xs_overflow = pointers.xs_length % Z
    ys_overflow = pointers.ys_length % Z
    pointers = _move_last_elements_to_end(A, pointers, xs_overflow, ys_overflow)
    buffer_zone = pointers.buffer_start  # just need buffer now, no more xs/ys

    # 2) Sort the blocks according to their first elements.
    # TODO(emond): README
    num_blocks = (pointers.xs_length + pointers.ys_length) // Z
    start = pointers.xs_start
    compare_first_elem = lambda i, j: A[start+i] < A[start+j]
    swap_block = lambda i, j: array_utils.swap_k_elements(A, start+i*Z,
                                                          start+j*Z, k=Z)
    array_utils.selection_sort(length=num_blocks, compare_fn=compare_first_elem,
                               swap_fn=swap_block)

    # 3) Fully sort a block at a time.
    # TODO(emond): README
    for block_idx in range(num_blocks-1):
        current_block_start = block_idx * Z
        next_block_start = (block_idx + 1) * Z
        _merge_inplace_with_buffer(A,
                SubarrayPointers(xs_start=current_block_start, xs_length=Z,
                                 ys_start=next_block_start, ys_length=Z,
                                 buffer_start=buffer_zone, buffer_length=Z))

    # 4) Sort our buffer of big elements.
    # TODO(emond): README
    array_utils.selection_sort(A, buffer_zone, pointers.buffer_length)


def _merge_inplace_with_buffer(A, pointers):
    """"""
    pass  # TODO(emond): implement


def _point_to_kth_biggest(A, pointers, k):
    """Point to the end of 'xs' and 'ys' and move, in descending order, both
    pointers until we've moved k times.
    If none of the k biggest elements is in a particular subarray ('xs' or
    'ys'), its pointer will be on start+length of that subarray (right after).
    If a subarray is exhausted, the pointer will be on its start element.

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


def _move_last_elements_to_end(A, pointers, xs_to_move, ys_to_move):
    """Moves the ends of both sorted subarrays to the end of A.
    Takes the last 'xs_to_move' elements from 'xs' and the last 'ys_to_move'
    elements from 'ys' and moves them all after 'ys'.
    Returns the new pointers for the adjusted 'xs', 'ys', and 'buffer' sections.
    
    Returns:
        A SubarrayPointers object, with the pointers to the modified 'xs', 'ys',
        and 'buffer' regions set.

    Complexity:
        - O(|ys| + |xs|) time
        - O(1) space
    """
    assert pointers.xs_length >= xs_to_move and pointers.ys_length >= ys_to_move
    # TODO(emond): update README to have this instead
    # What will my new xs and ys look like?
    new_xs_start = pointers.xs_start
    new_xs_length = pointers.xs_length - xs_to_move
    new_ys_start = new_xs_start + new_xs_length
    new_ys_length = pointers.ys_length - ys_to_move
    new_buffer_start = new_ys_start + new_ys_length
    new_buffer_length = pointers.buffer_length + xs_to_move + ys_to_move
    # Rotate the last elements of 'xs' that belong in 'buffer' so that they're
    # on the right of the new 'ys', starting from:
    # |-----xs-----:--big-xs--|-----ys-----:--big-ys--|
    #              |<=========rotate-------|
    # to get:
    # |-----xs-----|-----ys-----|--big-xs--:--big-ys--|
    #                            ^^^^^^^ buffer ^^^^^^
    array_utils.rotate_k_left(A, start=new_ys_start,
                              length=xs_to_move + new_ys_length,
                              k=xs_to_move)
    return SubarrayPointers(xs_start=new_xs_start,
                            xs_length=new_xs_length,
                            ys_start=new_ys_start,
                            ys_length=new_ys_length,
                            buffer_start=new_buffer_start,
                            buffer_length=new_buffer_length)


def _move_k_biggest_elements_to_end(A, pointers, k):
    """Moves the k biggest elements from A (at the end of 'xs' and 'ys') after
    'ys', to make up a new 'buffer' section (unsorted). Returns new pointers to
    the updated 'xs', 'ys', and 'buffer' sections.

    Returns:
        A SubarrayPointers object, with the pointers to the modified 'xs', 'ys',
        and new 'buffer' regions set.

    Guarantees after calling:
        - [new_xs_start, new_ys_start) will be sorted, and the new 'xs';
        - [new_ys_start, buffer_start] will be sorted, and the new 'ys';
        - [buffer_start, buffer_start+buffer_length) has the top k biggest
          elements from [new_xs_start, buffer_start), with no guarantees about
          their order.

    Complexity:
        - O(|ys| + |xs|) time
        - O(1) space
    """
    assert pointers.xs_length + pointers.ys_length >= k
    # How many elements from 'xs' and 'ys' must we move?
    xs_biggest_start, ys_biggest_start = _point_to_kth_biggest(A, pointers, k)
    xs_biggest_length = pointers.ys_start - xs_biggest_start
    ys_biggest_length = (pointers.ys_start + pointers.ys_length
                         - ys_biggest_start)
    return _move_last_elements_to_end(A, pointers, xs_biggest_length,
                                      ys_biggest_length)
