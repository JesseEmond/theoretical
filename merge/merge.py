"""Merge function and related helpers to merge two sorted subarrays in-place.

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
    """Subarray indices within A: xs, ys (sorted) and buffer (unsorted)."""
    def __init__(self, xs_start, xs_length, ys_start, ys_length,
                 buffer_start, buffer_length):
        assert xs_length >= 0 and ys_length >= 0 and buffer_length >= 0
        assert ys_start >= xs_start and buffer_start >= ys_start
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


def merge_inplace(A, start, length, verbose=False, kronrad=False):
    """Sorts, in-place, a subarray within A that contains 2 sorted subarrays.

    Complexity:
        - O(length) time
        - O(1) space
    """
    if kronrad:
        merge_inplace_kronrad(A, start, length, verbose=verbose)
        return
    N = length
    Z = int(math.sqrt(N))
    ys_start = array_utils.find_first_unsorted_index(A, start, N)
    if ys_start is None:
        return  # already sorted!
    pointers = SubarrayPointers(xs_start=start,
                                xs_length=ys_start - start,
                                ys_start=ys_start,
                                ys_length=start + N - ys_start,
                                buffer_start=start + N,
                                buffer_length=0)
    assert array_utils.is_sorted(A, pointers.xs_start,
                                 pointers.xs_length) and \
           array_utils.is_sorted(A, pointers.ys_start,
                                 pointers.ys_length), \
           "Expected an array with two sorted subarrays."

    if verbose:
        print(f"Start: {pointers.show(A)} Z={Z}")

    # 1) Move (at least) the 'Z' biggest elements to 'buffer'.
    # We need to pad xs and ys with the biggest elements to become multiples of
    # Z while keeping a resulting buffer of at least Z elements, so take Z
    # largest elements (buffer) + (Z-1) (max xs padding) + (Z-1) (max ys
    # padding) = 3Z-2.
    _move_k_biggest_elements_to_end(A, pointers, k=3*Z-2)
    if verbose:
        print(f"1.0) move 3Z-2 to end: {pointers.show(A)}")
    _make_multiples_of_k(A, pointers, k=Z)
    if verbose:
        print(f"1.1) make multiples of Z: {pointers.show(A)}")

    # 2) Sort the blocks according to their first elements.
    _sort_blocks(A,
                 pointers.xs_start, pointers.xs_length + pointers.ys_length,
                 Z)
    if verbose:
        print(f"2) sort blocks based on first elements: {pointers.show(A)}")

    # 3) Fully sort a block at a time.
    for i in range(pointers.xs_start, pointers.buffer_start - Z, Z):
        current_block = i
        next_block = i + Z
        if A[next_block-1] < A[next_block]:
            # Optimization: if the last element of the current block is smaller
            # than the first element of the next block, there is no work to do
            # (blocks are already sorted).
            continue

        # Move first block to our buffer to make space for the output of
        # merging the two blocks.
        array_utils.swap_k_elements(A, start=current_block,
                                    target=pointers.buffer_start, k=Z)
        _merge_into_target(A, xs_start=pointers.buffer_start,
                           ys_start=next_block, target=current_block, length=Z)
        if verbose:
            print(f"3.{i}) sort block #{i}: {pointers.show(A)}")
    if verbose:
        print(f"3) sort blocks one at a time : {pointers.show(A)}")

    # 4) Sort our buffer of "large" elements.
    _selection_sort(A, pointers.buffer_start, pointers.buffer_length)
    if verbose:
        print(f"4) sort buffer: {pointers.show(A)}")
    assert array_utils.is_sorted(A, start, length)


def merge_inplace_kronrad(R, start, N, verbose=False):
    """As described in TAOCP Vol 3, 5.2.4. exercise #18."""
    # Note: using the same terminology as TAOCP here.
    M = array_utils.find_first_unsorted_index(R, start, N)
    if M is None:
        return  # Already sorted.
    n = int(math.sqrt(N))
    s = n + N % n  # length of auxiliary area

    # Prepare auxiliary storage.
    aux_start = start + N - s
    zone_R_M = (M-start-1) // n  # zone that contains R_M (when indexed by 1).
    # If R_M turns out to be in the last mod n zone, swap only mod n.
    swap_len = min(n, N - (zone_R_M * n + n))
    array_utils.swap_k_elements(R, start=start+zone_R_M*n, k=swap_len,
                                target=aux_start)

    # Sort & merge blocks.
    _sort_blocks(R, start, N-s, n)
    for i in range(start, N-s-n, n):
        # Swap block to auxiliary storage
        array_utils.swap_k_elements(R, start=i, target=aux_start, k=n)
        _merge_into_target(R, xs_start=aux_start, ys_start=i+n, target=i,
                           length=n)

    # Cleanup
    _selection_sort(R, start=aux_start-s, length=2*s)  # Move s biggest to aux.
    # Same idea as our other merge, but a bit different; going from right to
    # left (grabbing bigger elements) and not assuming that both sides are the
    # same length.
    array_utils.swap_k_elements(R, start=aux_start-s, target=aux_start, k=s)
    x, y = aux_start-s-1, aux_start+s-1
    for i in reversed(range(start, aux_start)):
        if y < aux_start:
            break  # Swapped the last auxiliary element, we are done.
        if x >= start and R[x] > R[y]:
            R[x], R[i] = R[i], R[x]
            x -= 1
        else:
            R[y], R[i] = R[i], R[y]
            y -= 1
    _selection_sort(R, start=aux_start, length=s)


def merge_sort_inplace(A):
    """Merge sort 'A' in-place, using a bottom-up approach."""
    size = 1  # powers of 2
    while size < len(A):  # lg N iterations
        for xs_start in range(0, len(A), size * 2):  # goes over N elements
            ys_start = xs_start + size
            length = min(len(A), ys_start + size) - xs_start
            merge_inplace(A, start=xs_start, length=length)
        size *= 2
    assert array_utils.is_sorted(A, 0, len(A))


def _merge_into_target(A, xs_start, ys_start, target, length):
    """Merges sorted xs&ys (both same length), swapping with 'target' elements.

    Note that this works even if ys_start (or xs_start) equals target+length,
    e.g.:
    |-----------|-----------|----------- ... -----------|-----------|
     ^ target    ^ ys_start                              ^ xs_start
    <=======================>
           2 * length

    Whenever 'target' reaches ys_start during the merge, the current y pointer
    is, in the worst case, still at ys_start (if all xs are smaller than
    all ys). From there, we can't overwrite values from ys, because we'd
    essentially swap y elements with themselves (i.e. current target is always
    <= current y pointer).

    Assumptions:
        - 'target' has enough space to hold 2*length elements;
        - [target, target+length) does not overlap with xs or ys.

    Complexity:
        - O(length) time
        - O(1) space (using 'target' as temporary space)
    """
    x, y = xs_start, ys_start
    for i in range(length * 2):
        xs_exhausted = x >= xs_start + length
        ys_exhausted = y >= ys_start + length
        # Either we're forced to read x or y (all that's left), or pick the
        # smallest.
        if ys_exhausted or (not xs_exhausted and A[x] < A[y]):
            A[x], A[target+i] = A[target+i], A[x]
            x += 1
        else:
            A[y], A[target+i] = A[target+i], A[y]
            y += 1


def _point_to_kth_biggest(A, pointers, k):
    """Move k times total, in descending order, pointers from the end of xs/ys.

    Point to the end of 'xs' and 'ys' and move, in descending order through
    the array, both pointers until we've moved k times.
    If none of the k biggest elements is in a particular subarray ('xs' or
    'ys'), its pointer will be on start+length of that subarray (right after).
    If a subarray is exhausted, the pointer will be on its start element.

    Returns:
        - (xs_pointer, ys_pointer)
          Tuple of pointers within 'xs' and 'ys', respectively, where one is a
          pointer to the kth biggest element and the other is a pointer to the
          last of the k-1 biggest elements encountered (if any) in that
          subarray.

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
        # ys next largest
        if xs_exhausted or (not ys_exhausted and
                            A[y_pointer-1] > A[x_pointer-1]):
            y_pointer -= 1
        else:  # xs next largest
            x_pointer -= 1
    return (x_pointer, y_pointer)


def _move_last_elements_to_end(A, pointers, xs_to_move, ys_to_move):
    """Moves the ends of both sorted subarrays to the end of A (buffer).

    Takes the last 'xs_to_move' elements from 'xs' and the last 'ys_to_move'
    elements from 'ys' and moves them all after 'ys'. Updates the pointers.

    Complexity:
        - O(|ys| + |xs|) time
        - O(1) space
    """
    assert pointers.xs_length >= xs_to_move and \
           pointers.ys_length >= ys_to_move
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
    """Moves k largest elements of A to 'buffer' section (unsorted).

    Moves the k largest elements from A (at the end of 'xs' and 'ys') after
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

    Takes from buffer to pad 'xs' and 'ys' with extra elements to each have a
    size of '0 mod k'. Does so by first sorting 'buffer', then rotating.
    """
    _selection_sort(A, pointers.buffer_start, pointers.buffer_length)
    # How many more elements do we need to reach %k==0?
    xs_needs = (-pointers.xs_length) % k
    ys_needs = (-pointers.ys_length) % k
    assert pointers.buffer_length >= xs_needs + ys_needs
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


def _selection_sort(A, start, length):
    """O(length^2)"""
    def compare_buffer_elem(i, j): return A[start+i] < A[start+j]
    def swap_buffer_elem(i, j): A[start+i], A[start+j] = A[start+j], A[start+i]

    array_utils.selection_sort(length=length,
                               compare_fn=compare_buffer_elem,
                               swap_fn=swap_buffer_elem)


def _sort_blocks(A, start, length, Z):
    """Sorts blocks of Z elements based on their first element."""
    assert length % Z == 0
    num_blocks = length // Z

    def compare_first_elem(i, j): return A[start+i*Z] < A[start+j*Z]

    def swap_block(i, j):
        array_utils.swap_k_elements(A, start=start+i*Z, k=Z, target=start+j*Z)

    array_utils.selection_sort(length=num_blocks,
                               compare_fn=compare_first_elem,
                               swap_fn=swap_block)
