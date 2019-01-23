""" Helper generic array functions. """


def find_first_unsorted_index(X):
    """
    Finds the first element in an array that is not in sorted order.
    If the array is fully sorted, returns the length of the array.

    Example:
        i = find_first_unsorted_index([10, 12, 13, 11, 14, 15])
        assert i == 3  # '11'

    Complexity:
        - O(n) time
        - O(1) space
    """
    unsorted_elements = (i for i in range(1, len(X)) if X[i-1] > X[i])
    return next(unsorted_elements, len(X))

def swap_k_elements(X, start, k, target):
    """
    Swaps elements in-place at indices [start, start+k) with the elements at
    indices [target, target+k), from left to right.
    Assumes that all indices to be swapped are valid indices.

    Example:
        X = [0, 0, 1, 2, 2]
        swap_k_elements(X, start=0, k=2, target=3)
        assert X == [2, 2, 1, 0, 0]

    Complexity:
        - 0(k) time
        - O(1) space
    """
    for i in range(k):
        X[start+i], X[target+i] = X[target+i], X[start+i]

def selection_sort(X, start, length):
    """
    Sorts the region [start, start+length) within X, using selection sort.
    Guarantees to do at most |length| swaps (/moves).

    Example:
        X = [3, 2, 1, 0]
        selection_sort(X, start=1, length=2)
        assert X == [3, 1, 2, 0]

    Complexity:
        - O(length^2) time
        - O(1) space
    """
    for current in range(start, start+length):  # length iterations
        remaining_elems_indices = (i for i in range(current, start+length))
        smallest_idx = min(remaining_elems_indices,  # O(length)
                           key=lambda i: X[i])
        X[current], X[smallest_idx] = X[smallest_idx], X[current]


def rotate_k_left(X, start, length, k):
    """
    Rotates the region [start, start+length) by k elements to the left within X.

    Example:
        X = [0, 1, 2, 3, 4, 5]
        rotate_k_left(X, start=1, length=4, k=1)
        assert X == [0, 2, 3, 4, 1, 5]

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
    invert(X, start, k)  # O(k) = O(length)
    invert(X, start+k, length-k)  # O(length-k) = O(length)
    invert(X, start, length)  # O(length)

def invert(X, start, length):
    """
    Inverts the region [start, start+length) within X.

    Example:
        X = [0, 1, 2, 3]
        invert(X, start=1, length=2)
        assert X == [0, 2, 1, 3]

    Complexity:
        - O(length) time
        - O(1) space
    """
    end = start+length-1
    while start < end:
        X[start], X[end] = X[end], X[start]
        start += 1
        end -= 1
