"""Merge function and related helpers to sort an array that has two sorted
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
import copy
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
        return (self.__class__ == other.__class__ and
                self._value() == other._value())
    def __repr__(self):
        return "xs:[%d, %d) ys:[%d, %d) buf:[%d, %d)" % (
                self.xs_start, self.xs_start+self.xs_length,
                self.ys_start, self.ys_start+self.ys_length,
                self.buffer_start, self.buffer_start+self.buffer_length
                )
    def _value(self):
        return (self.xs_start, self.xs_length, self.ys_start, self.ys_length,
                self.buffer_start, self.buffer_length)
    def show(self, A):
        return "xs: %s  ys: %s  buf: %s" % (
                A[self.xs_start:self.xs_start + self.xs_length],
                A[self.ys_start:self.ys_start + self.ys_length],
                A[self.buffer_start:self.buffer_start + self.buffer_length])



def merge_inplace(A, start, length, verbose=False):
    """Takes a subarray within A that is assumed to have two subarrays that are
    sorted, and sorts it in-place.

    Complexity:
        - O(len(A)) time
        - O(1) space
    """
    # TODO(emond): test relative
    N = length
    Z = int(math.sqrt(N))
    ys_start = array_utils.find_first_unsorted_index(A, start, N)
    if ys_start == N: return  # already sorted!
    pointers = SubarrayPointers(xs_start=start,xs_length=ys_start - start,
                                ys_start=ys_start,
                                ys_length=start + N - ys_start,
                                buffer_start=start + N,
                                buffer_length=0)
    assert array_utils.is_sorted(A, pointers.xs_start,
                                 pointers.xs_length) and \
           array_utils.is_sorted(A, pointers.ys_start,
                                 pointers.ys_length), \
           "Expected an array with two sorted subarrays."

    if verbose: print("Start: %s Z=%d" % (pointers.show(A), Z))

    # 1) Move (at least) the 'Z' biggest elements to 'buffer'.
    # We need to pad xs and ys with the biggest elements to become multiples of
    # Z while keeping a resulting buffer of at least Z elements, so take Z
    # largest elements (buffer) + (Z-1) (max xs padding) + (Z-1) (max ys
    # padding) = 3Z-2.
    _move_k_biggest_elements_to_end(A, pointers, k=3*Z-2)
    _sort_buffer(A, pointers)
    if verbose: print("1.0) move 3Z-2 to end + sort: %s" % pointers.show(A))
    _make_multiples_of_k(A, pointers, k=Z)
    if verbose: print("1.1) make multiples of Z: %s" % pointers.show(A))

    # 2) Sort the blocks according to their first elements.
    _sort_blocks(A, pointers, Z)
    if verbose: print("2) sort blocks based on first elements: %s" %
                      pointers.show(A))

    # 3) Fully sort a block at a time.
    for i in range(pointers.xs_start, pointers.buffer_start - Z, Z):
        current_block = i
        next_block = i + Z
        # Optimization: if the last element of the current block is smaller than
        # the first element of the next block, there is no work to do (blocks
        # are already sorted).
        if A[next_block-1] < A[next_block]: continue
        # Move first block to our buffer to make space for the output of merging
        # the two blocks.
        array_utils.swap_k_elements(A, start=current_block,
                                    target=pointers.buffer_start, k=Z)
        _merge_into_target(A, xs_start=pointers.buffer_start,
                           ys_start=next_block, target=current_block, length=Z)
        if verbose: print("3.%d) sort block #%d: %s" % (i, i, pointers.show(A)))
    if verbose: print("3) sort blocks one at a time : %s" % pointers.show(A))

    # 4) Sort our buffer of "large" elements.
    # TODO(emond): README
    _sort_buffer(A, pointers)
    if verbose: print("4) sort buffer: %s" % pointers.show(A))
    assert array_utils.is_sorted(A, start, length)


def merge_sort_inplace(A):
    """TODO(emond): doc"""
    # TODO(emond): more tests
    size = 2  # powers of 2
    while size < len(A):  # lg(len(A)) iterations
        for i in range(size, len(A), size):  # goes over all elements of A
            previous = i - size
            length = min(size*2, len(A)-previous)
            merge_inplace(A, start=previous, length=length)
        size *= 2
    assert array_utils.is_sorted(A, 0, len(A))


def _merge_into_target(A, xs_start, ys_start, target, length):
    """Merges the sorted xs and ys (both of same length), swapping
    with the elements at 'target'.

    Note that this works even if ys_start (or xs_start) equals target+length,
    e.g.:
    |-----------|-----------|----------- ... -----------|-----------|
     ^ target    ^ ys_start                              ^ xs_start

    Whenever 'target' reaches ys_start during the merge, the current y pointer
    is, in the worst case, still at ys_start (if all xs are smaller than
    all ys). From there, we can't overwrite values from ys, because we'd
    essentially swap y elements with themselves (i.e. current target is always
    <= current y pointer).

    Assumptions:
    - 'target' has enough space to hold 2*length elements;
    - [target, target+length) does not overlap with xs or ys.
    """
    x, y = xs_start, ys_start
    for i in range(length * 2):
        xs_exhausted = x >= xs_start + length
        ys_exhausted = y >= ys_start + length
        if ys_exhausted or (not xs_exhausted and A[x] < A[y]):
            A[x], A[target+i] = A[target+i], A[x]
            x += 1
        else:
            A[y], A[target+i] = A[target+i], A[y]
            y += 1


def _point_to_kth_biggest(A, pointers, k):
    """Point to the end of 'xs' and 'ys' and move, in descending order through
    the array, both pointers until we've moved k times.
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
        xs_exhausted = x_pointer <= pointers.xs_start
        ys_exhausted = y_pointer <= pointers.ys_start
        if xs_exhausted or (not ys_exhausted and
                            A[y_pointer-1] > A[x_pointer-1]):  # ys next largest
            y_pointer -= 1
        else:
            x_pointer -= 1
    return (x_pointer, y_pointer)


def _move_last_elements_to_end(A, pointers, xs_to_move, ys_to_move):
    """Moves the ends of both sorted subarrays to the end of A.
    Takes the last 'xs_to_move' elements from 'xs' and the last 'ys_to_move'
    elements from 'ys' and moves them all after 'ys'. Updates the pointers.

    Complexity:
        - O(|ys| + |xs|) time
        - O(1) space
    """
    assert pointers.xs_length >= xs_to_move and pointers.ys_length >= ys_to_move
    # TODO(emond): update README to have this instead
    # Rotate the last elements of 'xs' that belong in 'buffer' so that they're
    # on the right of the new 'ys', starting from:
    # |-----xs-----:--big-xs--|-----ys-----:--big-ys--|
    #              |<=========rotate-------|
    # to get:
    # |-----xs-----|-----ys-----|--big-xs--:--big-ys--|
    #                            ^^^^^^^ buffer ^^^^^^
    pointers.xs_length -= xs_to_move
    pointers.ys_start -= xs_to_move
    pointers.ys_length -= ys_to_move
    pointers.buffer_start -= xs_to_move + ys_to_move
    pointers.buffer_length += xs_to_move + ys_to_move
    array_utils.rotate_k_left(A, start=pointers.ys_start,
                              length=xs_to_move + pointers.ys_length,
                              k=xs_to_move)


def _move_k_biggest_elements_to_end(A, pointers, k):
    """Moves the k biggest elements from A (at the end of 'xs' and 'ys') after
    'ys', to make up a new 'buffer' section (unsorted). Updates the pointers.

    Guarantees after calling:
        - [xs_start, ys_start) will be sorted, and the new 'xs';
        - [ys_start, buffer_start) will be sorted, and the new 'ys';
        - [buffer_start, buffer_start+buffer_length) has the top k biggest
          elements from [xs_start, buffer_start+buffer_length), with no
          guarantees about their order.

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
    _move_last_elements_to_end(A, pointers, xs_biggest_length,
                               ys_biggest_length)


def _make_multiples_of_k(A, pointers, k):
    """Modifies 'xs' and 'ys' to have a multiple of 'k' elements.
    TODO(emond): update all

    Assumes that one already ran _point_to_kth_biggest before with a 'k' of at
    least 3k-2 (k in this method's context). In the context of the merge, of
    3Z-2. This is because this function takes from the big elements to construct
    sorted 'xs' and 'ys' as multiple of k elements, while ensuring that we still
    end up with at least k "big" elements. 3Z-2 comes from:
    Z (want min Z big elements) + Z-1 (max of |xs|%Z) + Z-1 (max of |ys|%Z)

    Assumptions:
        - xs_biggest_length + ys_biggest_length >= 3*k-2
    Guarantees:
        - xs, ys will remain sorted, but ys might move
        - new_xs_biggest_length + new_ys_biggest_length >= k
    """
    # TODO(emond): TEST
    # How many more elements do we need to reach %k==0?
    xs_needs = (-pointers.xs_length) % k
    ys_needs = (-pointers.ys_length) % k
    # Rotate the (sorted) smallest elements of 'buffer' to extend xs and ys as
    # needed. This way, we know that 'buffer-remainder' still has the biggest
    # elements, and xs and ys get elements that preserve their sorted order.
    #                           |-----------------buffer---------------------|
    # |-----xs-----|-----ys-----|--ys_needs--|--xs_needs--|-buffer-remainder-|
    #              |---------------------rotate==========>|
    # to get:
    # |-----xs-----|--xs_needs--|-----ys-----|--ys_needs--|-buffer-remainder-|
    #                                                      ^^^^^ buffer ^^^^^
    array_utils.rotate_k_right(A, start=pointers.ys_start,
                               length=pointers.ys_length + xs_needs + ys_needs,
                               k=xs_needs)
    pointers.xs_length += xs_needs
    pointers.ys_start += xs_needs
    pointers.ys_length += ys_needs
    pointers.buffer_start += xs_needs + ys_needs
    pointers.buffer_length -= xs_needs + ys_needs

def _sort_buffer(A, pointers):
    """Sorts the buffer subarray (at the end) in-place in O(buffer_length^2)."""
    start = pointers.buffer_start
    compare_buffer_elem = lambda i, j: A[start+i] < A[start+j]
    def swap_buffer_elem(i, j): A[start+i], A[start+j] = A[start+j], A[start+i]
    array_utils.selection_sort(length=pointers.buffer_length,
                               compare_fn=compare_buffer_elem,
                               swap_fn=swap_buffer_elem)

def _sort_blocks(A, pointers, Z):
    """TODO(emond): document"""
    assert (pointers.xs_length + pointers.ys_length) % Z == 0
    num_blocks = (pointers.xs_length + pointers.ys_length) // Z
    start = pointers.xs_start
    compare_first_elem = lambda i, j: A[start+i*Z] < A[start+j*Z]
    swap_block = lambda i, j: array_utils.swap_k_elements(A,
                                                          start=start+i*Z,
                                                          k=Z,
                                                          target=start+j*Z)
    array_utils.selection_sort(length=num_blocks, compare_fn=compare_first_elem,
                               swap_fn=swap_block)
