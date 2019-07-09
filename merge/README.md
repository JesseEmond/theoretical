# In-Place Linear Merge

A colleague of mine gave me an interesting challenge: to essentially do the merge part of a merge-sort in `O(N)` time and `O(1)` extra space. A bit more formally:

Given an array of `N` elements split in two sorted subarrays (of potentially different sizes):

​	`x0  x1  ...  xn   y0  y1  ...  ym` 

​	(where `n+m = N` , `x0  x1  ...  xn` are sorted and `y0  y1  ...  ym` are sorted),

merge both subarrays such that the final array of `N` elements is sorted. Do so in time `O(N)` and `O(1)` extra memory. In short, merge two sorted arrays in-place linearly.

A concrete example:

`0  7  8  10   1  2  3  4  5  6  9`

Would have to be sorted in `O(N)`, without an additional memory requirement that grows with `N`, as:

`0  1  2  3  4  5  6  7  8  9  10`

*Note: by "in-place" and "`O(1)` extra space", I really mean "a constant number of pointers into the array" ([LSPACE](https://en.wikipedia.org/wiki/L_(complexity))), which amounts in reality to `O(lg N)` additional memory. Keep this in mind whenever you see `O(1)` memory. By `O(N)` time, I implicitly assume `O(1)` time to compare two elements. If that's not the case, the final complexity becomes `O(N)` times the complexity of a comparison.*

## Naive Approaches

To appreciate the complexity of the problem, it helps to see why and how naive approaches fail.

If we didn't care about `O(N)` time, we could use an in-place sort algorithm (probably not merge-sort, which would likely use a function like the one we're trying to code here... :-) ) to solve it in `O(N lg N)`.

If we didn't have the `O(1)` memory requirement, we could easily build a new sorted array from copying, in order, from both subarrays:

```python
first_y = index_first_out_of_order(original)
x, y = 0, first_y  # ptrs within subarrays
new = list(original)  # make a new array of N elements
for i in range(len(new)):
  xs_exhausted = x >= first_y
  ys_exhausted = y >= len(original)
  if ys_exhausted or (not xs_exhausted and original[x] < original[y]):
	new[i] = original[x]
    x += 1
  else:
 	new[i] = original[y]
 	y += 1
```

But we're not allowed the `O(N)` extra memory.

What if we blindly tried this approach, but did it all in-line with swaps instead of doing copies to separate storage (essentially replace `new[i] = original[whatever]` with `new[i], original[whatever] = original[whatever], new[i]` (swap))? We'd run into issues pretty fast:

```
4  5  8  9   0  1  2  3  6  7
^            ^ (swap)
0  5  8  9   4  1  2  3  6  7
             !  ! (ys not sorted anymore)
```

We break the sort on `ys`, which is a problem because then we would need to remember that there's a `4` sitting there that will eventually be the smallest element to grab (after `1  2  3`). We could try to remember that this one element is sitting there (with a pointer), but then how many more elements will we need to remember in the same manner before getting to that `4`? If we can come up with examples where this additional bookkeeping grows with `N` (i.e. non-constant), we're no longer `O(1)` memory.

What if we try to move the `4` to where it belongs in `ys`, via an `O(k)`  rotate (`k` being the number of elements in `ys` that are `< 4`), before doing that swap? A strategy like that would break down if we have something like this:

```
5  6  7  8  9   0  1  2  3  4
```

because we would swap the `5`, rotate it to the right of `ys`, swap the `6`, rotate it to the right, ... We would have to shift each `N/2` `xs` elements to the right of `ys` (which takes `O(N/2)`), which would lead to `O(N^2)`.

What if instead of just swapping the `0` with the `4` in our first example (`4  5  8  9   0  1  2  3  6  7`), we also swap any other `ys` numbers that we *know* will come before `4`:

```
4  5  8  9   0  1  2  3  6  7
^  -  -  -   ^  ^  ^  ^ (0 1 2 3 must be swapped because < 4)
0  1  2  3   4  5  8  9  6  7
                      !  ! (ys not sorted anymore)
```

No dice. The problem is that by doing this we can bring in numbers that are bigger than what will follow them once they are in `ys` (e.g. `8` and `9` > `6`).

Clearly, coming up with simple ideas and trying to "patch" the counterexamples that we find isn't working out (what a surprise!)

## Hints

I spent a long time exploring a bunch of ideas.

I considered finding the `(n+1)`th smallest element in `O(N)` (by having a pointer on `xs` and one on `ys` and moving one at a time until we moved `n+1` times), which would then give us the element that belongs at the index of `y0`, call it `P` (at the `nth` index). Then, I was hoping I could partition `xs` and `ys` to move the elements `<= P` to `xs`, and the ones `> P` to `ys`.

By naively doing so, I could have two subarrays that each contained two sorted subarrays to merge... so no closer to solving the problem in `O(N)` than initially.

I played with ideas to move the elements `<= P` to `xs` while ensuring that they are in a sorted order in `xs` (so solving the problem for the first `n` elements!) Then, if I could find a way to maintain two sorted subarrays in the elements that I have to move to `ys`, I could hopefully maybe have sorted `n` elements in `O(n)` with an array of `m` elements (`N-n`) left to merge. However, finding a way to do that proved to be quite hard, or at least not in a way that would have been `O(n)`.

At this point I decided to read up on the problem a bit more, to see if there were theoretical tools that I was missing to find a solution. I ended up finding resources on the problem itself, with [this stackoverflow question](https://stackoverflow.com/q/2126219) standing out.

Turns out this isn't exactly a trivial problem (one that I'll see in TAOCP Vol. 3!), and likely not one one would encounter in an interview. The stackoverflow answers link to some relatively old papers that address it, and give some very helpful high-level ideas to solve it, from *Kronrod*:

- Divide in blocks of `sqrt(N)`;
- Use last `sqrt(N)` of biggest numbers as a buffer;
- Sort blocks by their first number;
- Remember that selection sort has a predictable number of moves (`N`).

At this point, I stopped reading to try and use those hints to come up with the rest of the algorithm on my own (what follows). The time spent thinking about the problem thankfully proved to be useful, because it was then much more straightforward to combine those hints with the tricks I developed while working on the problem.

For future personal reference, some ideas that I think are pretty neat and could help me in the future:

- Dividing in `sqrt(N)` tasks of `sqrt(N)` elements is a way to get `O(N)`;
- Keeping a small block of data as an unstructured buffer that we can fix in a "slow" way as a final step is fine (if it's small enough like `sqrt(N)` we can do `O(N^2)` processing on it to stay `O(N)`!);
- Selection sort of `sqrt(N)` blocks does `sqrt(N)` swaps, which can matter for expensive swaps (e.g. swapping blocks of `sqrt(N)` elements!), so it's important to think about the cost of the swaps.

## High-Level Algorithm

Let's define `Z = floor(sqrt(N))`.

Here will be the high-level steps:

1. Move the `Z` biggest elements to the end, which we'll call `buffer`.
   ​	`buffer` doesn't have to stay sorted, we'll fix it later.
   ​	Divide `xs` and `ys` into blocks of `Z` elements (assume we can, we'll fix in detailed algorithm)
2. Sort the blocks according to their first elements.
3. For each block, grab the `Z` smallest unsorted elements (using `buffer` as buffer to do so).
4. Sort `buffer`.

General structure that we follow:

```
|-----:-----:--xs-:-----:-----|-----:-----:--ys--:-----:-----:-----|-buffer-|
|=====|        ^                             ^                          ^
   Z           |                             |                          |
               |                             |                          |
sorted, blocks of 'Z' elements               |           unsorted, 'Z' biggest elements
                                             | 
                               sorted, blocks of 'Z' elements
```



The trick here is that the setup that we create (having blocks sorted by their first elements) allows us to do step 3 (grab `Z` smallest unsorted elements) in `O(Z)` for each block, giving us the following time complexities per step:

1. `O(Z)` to grab the `Z` biggest elements;
2. `O(Z^2) = O(sqrt(N)^2) = O(N)`, because with selection sort we can sort `Z` blocks with `O(Z^2)` comparisons of `O(1)` (comparing the first elements) with `Z` swaps (`O(Z)` to swap a block of `Z` elements), yielding `O(Z^2)` for comparisons + `O(Z^2)` for swaps;
3. Processing of `O(Z)` for each block to grab the `Z` smallest unsorted elements, done for each `Z` blocks: `O(Z^2) = O(N)`;
4. Selection sort of a buffer of `Z` elements, `O(Z^2) = O(N)`.

If we're careful in our implementation of each step to use a constant amount of pointers, we get an algorithm that is `O(N)` time and `O(1)` extra memory!

## Detailed Algorithm

The code is heavily commented if you want to take a closer look at how this can be implemented.

### 0.5) Setup

Call our array to merge `A` (`N = len(A)`). Compute `Z = floor(sqrt(N))`.

Find `ys_start` (first element of `ys`) by going linearly through `A` to find the first unsorted element:

```python
ys_start = next(i for i in range(1, len(A)) if A[i-1] > A[i])  # O(N)
```

Then delimiters of start and length of `xs` and `ys` are easy to deduce:

```python
xs_start, xs_length = 0, ys_start
ys_length = N - xs_length
```

### 1) Move `Z` biggest elements to `buffer`

To move the `Z` biggest elements to the end of the array, we do so in 2 steps:

1. Spot which elements of `xs` and `ys` are part of the `Z` biggest (`xs_to_move` and `ys_to_move`);
2. Move that many last elements of `xs` and `ys` to the end of the array (to the `buffer`). We do so like such: rotate to move the smaller `ys` to be alongside the smaller `xs` (bringing the biggest numbers to the back).

With a diagram:

```
|----------------xs---------------|------------------ys-------------------|
#1: Z biggest elements:  ^^^^^^^^^                               ^^^^^^^^^

|----------------xs------|-xs_big-|------------------ys----------|-ys_big-|
#2: rotate                <=======rotate-------------------------|
|----------------xs------|------------------ys----------|-xs_big-|-ys_big-|
                                                        |------buffer-----|
```

 To do so, we'll need a few tools.

```python
def point_to_kth_biggest(A, xs_start, xs_length, ys_start, ys_length, k):
  """Returns pointers within each sorted array such that one of them points
  to the kth biggest element, while the other one points to the last element
  seen within its subarray part of the k biggest elements.
  
  In simpler terms, point to the end of xs and ys and move, in descending order
  through the array, both pointers until we've moved k times.
  
  Assumes k <= |xs|+|ys| and that xs and ys are sorted.
  """
  x_ptr = xs_start+xs_length
  y_ptr = ys_start+ys_length
  for _ in range(k):
    if x_ptr <= xs_start:  # exhausted all 'xs'
      y_ptr -= 1  # move y
    elif y_ptr <= ys_start:  # exhausted all 'ys'
      x_ptr -= 1  # move x
    elif A[y_ptr-1] > A[x_ptr-1]:  # 'ys' has next largest element
      y_ptr -= 1  # move y
    else:
      x_ptr -= 1  # move x
  return (x_ptr, y_ptr)
```

We'll also need a rotate function, which we can cleverly implement linearly in-place with `invert` (learned about this through some stackoverflow answer that I can't find anymore):

```python
def rotate_k_left(A, start, length, k):
  """Rotate elements within an array k elements to the left, using inversions."""
  invert(A, start, k)
  invert(A, start+k, length-k)
  invert(A, start, length)
  
def invert(A, start, length):
  last = start+length-1
  for i in range(length//2):
    A[start+i], A[last-i] = A[last-i], A[start+i]
```

To see why rotate left works when implemented like that, it helps to follow a labeled array:

```
Initially we have:
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
```

With a reminder of what we want to do:

```
|----------------xs---------------|------------------ys-------------------|
#1:         xs_to_move:  ^^^^^^^^^                   ys_to_move: ^^^^^^^^^

|----------------xs------|-xs_big-|------------------ys----------|-ys_big-|
#2: rotate                <=======rotate-------------------------|
|----------------xs------|------------------ys----------|-xs_big-|-ys_big-|
                                                        |------buffer-----|
```

We can make a generic function that moves the last `xs_to_move` elements from `xs` and last  `ys_to_move` elements from `ys` to the end of our array (in `buffer`):

```python
def move_last_elements_to_end(A, xs_start, xs_length, ys_start, ys_length,
                              buffer_length, xs_to_move, ys_to_move):
  """Moves the end of both sorted subarrays to the end of A.
  Takes the last 'xs_to_move' elements from 'xs' and the last 'ys_to_move'
  elements from 'ys' and moves them all after 'ys' (in 'buffer').
  
  Assumes xs_to_move<=|xs|, ys_to_move<=|ys|
  """
  new_xs_start = xs_start
  new_xs_length = xs_length - xs_to_move
  new_ys_start = new_xs_start + new_xs_length
  new_ys_length = ys_length - ys_to_move
  new_buffer_start = new_ys_start + new_ys_length
  new_buffer_length = buffer_length + xs_to_move + ys_to_move
  
  # from:
  # |-----xs-----:--big-xs--|-----ys-----:--big-ys--|
  #              |<=========rotate-------|                                     
  # to get:                                                                    
  # |-----xs-----|-----ys-----|--big-xs--:--big-ys--|                          
  #                            ^^^^^^^ buffer ^^^^^^ 
  array_utils.rotate_k_left(A, start=new_ys_start, length=xs_to_move + new_ys_length,
                            k=xs_to_move)
  return (new_xs_start, new_xs_length, new_ys_start, new_ys_length,
          new_buffer_start, new_buffer_length)  # dimensions of sections change
```

We can now get back to moving the `Z` biggest elements:

```python
# 1) Move the Z biggest elements to the end (our buffer).
xs_big_start, ys_big_start = point_to_kth_biggest(A, xs_start, xs_length,
                                                  ys_start, ys_length, k=Z)
# How many elements from xs and ys do we have to move?
xs_top_elements = ys_start - xs_big_start
ys_top_elements = ys_start + ys_length - ys_big_start
xs_start, xs_length, ys_start, ys_length, buffer_start, buffer_length =
	move_last_elements_to_end(A, xs_start, xs_length, ys_start, ys_length,
                              buffer_length=0,
                              xs_to_move=xs_top_elements, ys_to_move=ys_top_elements)
```

In actual code, we make this clutter of keeping track of positions a little less worse by wrapping them in a structure.

`buffer` now has `Z` elements.

### 1.5) Make `xs` and `ys` multiples of `Z`

Now, to make the rest of the algorithm simpler, we'll guarantee that `xs` and `ys` are exact multiples of `Z` by moving their `mod Z` "overflow" at the end:

```python
# 1.5) Make xs and ys multiples of Z.
xs_overflow = xs_length % Z
ys_overflow = ys_length % Z
xs_start, xs_length, ys_start, ys_length, buffer_start, _ =
	move_last_elements_to_end(A, xs_start, xs_length, ys_start, ys_length,
                              buffer_start, buffer_length,
                              xs_to_move=xs_overflow, ys_to_move=ys_overflow)
```

Note that this could have been combined in the previous step to only do one rotate (we can compute `new_xs_length` to then compute `xs_overflow` and add it to `xs_top_elements` and do the same for `ys`), but I feel that doing so as a separate step like here keeps the functions pretty contained and with a clear purpose (with the same complexity!)

Now, `buffer` has `< 3Z` elements (`Z + (|X| % Z) + (|Y| % Z) < 3Z`, which still keeps our last buffer-sorting step `O(Z)`).

### 2) Sort blocks based on first element

To sort our blocks, we use selection sort. It has the nice property that it will do `O(n)` swaps (and each block swap is `O(Z)` (swapping the whole block), for a total of `O(Z^2) = O(N)`). Since there are `O(Z)` blocks in `A` (`N = sqrt(N)^2 = Z^2` and we divided `N` elements into blocks of `Z` elements, then moved some of those elements to `buffer`, so we still have `O(Z)` remaining blocks), selection sort will do `O(Z^2) = O(N)` comparisons. The swap and comparison costs conserve our `O(N)` time complexity requirement.

We implement selection sort as a general function so that we can reuse it both to sort blocks and to sort `buffer` at the end:

```python
def selection_sort(length, compare_fn, swap_fn):
  for i in range(length):
    min_index = i
    for j in range(i+1, length):
      if compare_fn(j, min_index):
        min_index = j
    if min_index != i:
      swap_fn(i, min_index)
```

For example, here is how we would swap a normal list of numbers:

```python
A = [3, 2, 1, 0]
compare_fn = lambda i, j: A[i] < A[j]
def swap_fn(i, j): A[i], A[j] = A[j], A[i]
selection_sort(len(A), compare_fn, swap_fn)
assert A == [0, 1, 2, 3]
```

Let's define another helper function:

```python
def swap_k_elements(A, start, target, k):
  for i in range(k):
    A[start+i], A[target+i] = A[target+i], A[start+i]
```

We can now sort the blocks:

```python
# 2) Sort blocks based on first element.
num_blocks = (xs_length + ys_length) // Z
compare_first_elem = lambda i, j: A[xs_start+i*Z] < A[xs_start+j*Z]
swap_block = lambda i, j: swap_k_elements(A, xs_start+i*Z, xs_start+j*Z, k=Z)
selection_sort(length=num_blocks, compare_fn=compare_first_elem, swap_fn=swap_block)
```

Now what's interesting about sorting blocks in this way is that, if we take the first 2 adjacent blocks afterwards and assume that everything to the left of them is fully sorted (in their final positions in `A`, i.e. in the middle of the algorithm), they are guaranteed to contain the next `Z` smallest elements of the unsorted part of `A`. Diagram to help picture that:

```
|-----:-----:-----:-----|--a--:--b--|--c--:--d--:--e--:--f--:--g--|-buffer-|
 ^^^^^^^^^^^^^^^^^^^^^^^|===========|
   sorted elems of A          ^ contains Z smallest elements of
        (final)                 U{a, b, ..., f, g}
```

Why is that?

- If both blocks are from the same original sorted subarray (assume they are both from `xs` , but the logic holds for `ys` too), then step 2 would not have changed their relative order and they would have remained sorted in their original order.
  - So, we know that the first block of `Z` elements would be the smallest `Z` elements out of all the remaining `xs` (same as the original sorted subarray);
  - We know that no `ys` element can be smaller than any `xs` element within the first block. This is because the first element of the second `xs` block is bigger than any `xs` element in the first block (retained their order from the original `xs` subarray), and no `ys` element is smaller than the first element from the second block (otherwise the second block would come from `ys`!);
  - This means that this first block is in its final position, and we can skip it (it has the `Z` smallest elements, in order).
- If both blocks originate from different sorted subarrays (assume the first block is from `xs` and the second from `ys`, but logic holds both ways), then the first block contains the smallest `Z` remaining elements of `xs` (similar logic as the precedent case) and the second block contains the smallest `Z` remaining elements of `ys` (same idea). Thus, the `Z` smallest elements of the two blocks are the `Z` smallest elements of `U{xs, ys}`.

We'll go over an example in the next section to make this clearer.

### 3) Grab `Z` smallest unsorted elements for each block

This is where the algorithm gets really elegant in my opinion.

We ultimately want to go through `A`, one block at a time, doing a merge (**not** in-place!) between the current block and the next. How can we afford to do it with extra memory? By using our buffer that we created in step 1! There's something that feels very elegant about implementing an in-place algorithm by using the additional-memory version of itself, with a temporary working area of the input data.

Let's focus on the implementation first, then go into more detail about why that properly sorts the array `A`.

Let's start with the implementation of merging with a buffer (notice the similarities with our very first `O(n)` memory naive approach):

``` python
def merge_into_target(A, xs_start, ys_start, target, length):
  """Merges the sorted xs and ys (both of same length), swapping
  with the elements at 'target'.
  
  Note that this works even if ys_start (or xs_start) equals target+length, e.g.:
  |-----------|-----------|----------- ... -----------|-----------|
  ^ target    ^ ys_start                              ^ xs_start
  
  Whenever 'target' reaches ys_start during the merge, the current y pointer is, in
  the worst case, still at ys_start (if all xs are smaller than all ys). From there,
  we can't overwrite values from ys, because we'd essentially swap y elements with
  themselves (current target is always <= current y pointer).
  
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
```

The comment about the validity of the algorithm even when `target` and `ys` overlap (specifically when `ys_start = target + length`) will matter because we'll be using that property.

So, say that we are looking at a certain block `a` and the next one `b`:

```
|-----:-----:-----:-----|--a--:--b--|--c--:--d--:--e--:--f--:--g--|-buffer-|
|======== sorted =======|  ^     ^
```

Remember: `a` is sorted, `b` is sorted, both of length `Z` (`sqrt(N)`). We want to merge them. We can use our `buffer` as needed (which has a size within `[Z, 3Z)` (at least 1 block, plus `|xs|%Z` and `|ys|%Z`). We don't know that it has at least `2Z` elements (as required by `merge_into_target`), so we'll instead swap `a` (first block) with the start of `buffer`. Then we can use the start of our original `a` as a target directly (that's where we want our merged blocks anyway!) Using our property that it's fine to have our second block be at `target + Z`, we're ready to go:

```python
# 3) Grab Z smallest unsorted elements for each block.
for i in range(0, buffer_start - Z, Z):
  current_block = i
  next_block = i + Z
  # Move first block to our buffer to make space for the block-merge output.
  swap_k_elements(A, start=current_block, target=buffer_start, k=Z)  # O(Z)
  merge_into_target(A, xs_start=buffer_start, ys_start=next_block,
                    target=current_block, length=Z)
```

TODO why that works

### 4) Sort `buffer`

TODO

## Full Example

TODO

## Merge Sort

TODO
