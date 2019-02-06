""" Helper generic array functions. """


def find_first_unsorted_index(A, start, length):
    """Finds the index to the first element in the
    subarray A[start:start+length) that is not in sorted order.
    If the subarray is fully sorted, returns start+length.

    Example:
        A = [10, 12, 13, 11, 14, 15]
        i = find_first_unsorted_index(A, start=1, length=4)
        assert i == 3 and A[i] == 11

    Complexity:
        - O(length) time
        - O(1) space
    """
    unsorted_elements = (i for i in range(start+1, start+length)
                         if A[i-1] > A[i])
    default = start+length
    return next(unsorted_elements, default)

def swap_k_elements(A, start, k, target):
    """Swaps elements in-place at indices [start, start+k) with the elements at
    indices [target, target+k), from left to right.
    Assumes that all indices to be swapped are valid indices.

    Example:
        A = [0, 0, 1, 2, 2]
        swap_k_elements(A, start=0, target=3, k=2)
        assert A == [2, 2, 1, 0, 0]

    Complexity:
        - O(k) time
        - O(1) space
    """
    for i in range(k):
        A[start+i], A[target+i] = A[target+i], A[start+i]


def selection_sort(length, compare_fn, swap_fn):
    """Generalized sort, using selection sort.
    Elements are compared by calling compare_fn with the indices of 2 elements.
    Elements are swapped by calling swap_fn with the indices of 2 elements.
    Guarantees to do at most |length| swaps (/moves).

    Example:
        A = [3, 2, 1, 0]
        compare_fn = lambda i, j: A[i] < A[j]
        def swap_fn(i, j): A[i], A[j] = A[j], A[i]
        selection_sort(len(A), compare_fn, swap_fn)
        assert A == [0, 1, 2, 3]

    Complexity:
        - O(length^2) time  (O(length) swaps)
        - O(1) space
    """
    for i in range(length):
        min_index = i
        for j in range(i+1, length):
            if compare_fn(j, min_index):
                min_index = j
        if min_index != i:
            swap_fn(i, min_index)


def rotate_k_left(A, start, length, k):
    """Rotates the region [start, start+length) by k elements to the left
    within A.

    Example:
        A = [0, 1, 2, 3, 4, 5]
        rotate_k_left(A, start=1, length=4, k=1)
        assert A == [0, 2, 3, 4, 1, 5]

    Complexity:
        - O(length) time
        - O(1) space

    Note:
        To do this in O(n) time O(1) mem, we apply 3 invertions:
            # assuming we're rotating a full array of length n for simplicity...
            invert(0, k)
            invert(k, n)
            invert(0, n)
        To see why this works, here is a labelled array:
            x_0  x_1  ...  x_{k-2}  x_{k-1}  x_k  x_{k+1}  ...  x_{n-1}  x_n
        Our goal is to have:
            x_k  x_{k+1}  ...  x_{n-1}  x_n  x_0  x_1  ...  x_{k-2}  x_{k-1}
        So from our initial array:
            x_0  x_1  ...  x_{k-2}  x_{k-1}  x_k  x_{k+1}  ...  x_{n-1}  x_n
        We do invert(0, k):
            x_{k-1}  x_{k-2}  ...  x_1  x_0  x_k  x_{k+1}  ...  x_{n-1}  x_n
        Then invert(k, n):
            x_{k-1}  x_{k-2}  ...  x_1  x_0  x_n  x_{n-1}  ...  x_{k+1}  x_k
        Finally invert(0, n):
            x_k  x_{k+1}  ...  x_{n-1}  x_n  x_0  x_1  ...  x_{k-2}  x_{k-1}
    """
    k %= length  # prevent index out of bounds for looping ks
    invert(A, start, k)  # O(k) = O(length)
    invert(A, start+k, length-k)  # O(length-k) = O(length)
    invert(A, start, length)  # O(length)

def invert(A, start, length):
    """Inverts the region [start, start+length) within A.

    Example:
        A = [0, 1, 2, 3]
        invert(A, start=1, length=2)
        assert A == [0, 2, 1, 3]

    Complexity:
        - O(length) time
        - O(1) space
    """
    last = start+length-1
    for i in range(length//2):
        A[start+i], A[last-i] = A[last-i], A[start+i]

def is_sorted(A, start, length):
    """Checks if the given array is sorted for the range [start, start+length).
    """
    all_unsorted_index = start + length
    return find_first_unsorted_index(A, start, length) == all_unsorted_index
