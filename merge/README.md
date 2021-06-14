# In-Place Linear Merge

A colleague of mine gave me an interesting challenge: to essentially do the merge part of a merge-sort in `O(N)` time and `O(1)` extra space. A bit more formally:

Given an array of `N` elements split in two sorted subarrays (of potentially different sizes):

​	`x0  x1  ...  xn   y0  y1  ...  ym` 

​	(where, by definition, `n+m = N` , `x0  x1  ...  xn` are sorted and `y0  y1  ...  ym` are sorted),

merge both subarrays such that the final array of `N` elements is sorted. Do so in time `O(N)` and `O(1)` extra memory. In short, merge two sorted arrays in-place linearly.

A concrete example:

`0  7  8  10   1  2  3  4  5  6  9`

Would have to be sorted in `O(N)`, without an additional memory requirement that grows with `N`, as:

`0  1  2  3  4  5  6  7  8  9  10`

*Note: by "in-place" and "`O(1)` extra space", I really mean "a constant number of pointers into the array" ([LSPACE](https://en.wikipedia.org/wiki/L_(complexity))), which amounts in reality to `O(lg N)` bits of additional memory. Keep this in mind whenever you see `O(1)` memory. By `O(N)` time, I implicitly assume `O(1)` time to compare two elements. If that's not the case, the final complexity would be `O(N)` times the complexity of a comparison.*

_Also note that the examples & this write-up assume distinct elements, but that's not necessary overall._

## Naive Approaches

To appreciate the complexity of the problem, it helps to see how and why naive approaches fail.

If we didn't care about `O(N)` time, we could use an in-place sort algorithm (maybe not merge-sort, which would likely use a function like the one we're trying to code here for its merge operation... :-) ) to solve it in `O(N lg N)`.

If we didn't have the `O(1)` memory requirement, we could relatively easily build a new sorted array where we copy, in order, from both subarrays:

```python
first_y = index_first_out_of_order(original)
x, y = 0, first_y  # ptrs within subarrays
new = list(original)  # make a new array of N elements
for i in range(len(new)):
  xs_exhausted = x >= first_y
  ys_exhausted = y >= len(original)
  if ys_exhausted or (not xs_exhausted and original[x] < original[y]):  # pick an x
	new[i] = original[x]
    x += 1
  else:  # pick a y
 	new[i] = original[y]
 	y += 1
```

But we're not allowed the `O(N)` extra memory.

What if we blindly tried this approach, but did it all in-place with swaps instead of doing copies to separate storage (essentially replace `new[i] = original[whatever]` with `new[i], original[whatever] = original[whatever], new[i]` (swap))? We'd run into issues pretty fast. Here's an example:

```
4  5  8  9   0  1  2  3  6  7
^            ^ (should swap)
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

I considered finding the `(n+1)`th sorted element (`(n+1)`th smallest element) in `O(N)` (by having a pointer on `xs` and one on `ys` and moving one at a time until we moved `n+1` times), which would then give us the element that belongs at the index of `y0`, call it `P` for a sort of "partition" point (at the `nth` index in the final sorted array). Then, I was hoping I could partition `xs` and `ys` to move the elements `<= P` to `xs`, and the ones `> P` to `ys`.

By naively doing that, I would have two subarrays that each contained their own two sorted subarrays to merge... so no closer to solving the problem in `O(N)` than initially.

I played with ideas to move the elements `<= P` to `xs` while ensuring that they are in a sorted order in `xs` (so solving the problem for the first `n` elements!) Then, if I could find a way to maintain two sorted subarrays in the elements that I move to `ys`, I could have sorted `n` elements in `O(n)` with an array of `m` elements (`N-n`) left to merge, with the same strategy that would have been `O(m)` (so `O(n+m)=O(N)`. However, finding a way to preserve the two sorted subarrays in `ys` while sorting the `xs` proved to be quite hard, or at least not in a way that would have been `O(n)`.

At this point I decided to read up on the problem a bit more, to see if there were theoretical tools that I was missing to find a solution. I ended up finding resources on the problem itself, with [this stackoverflow question](https://stackoverflow.com/q/2126219) standing out.

Turns out this isn't exactly a trivial problem (one that I'll see in _The Art of Computer Programming_ Vol. 3!), and likely not one one would encounter in an interview, for example. The stackoverflow answers link to some relatively old papers that address it, and give some very helpful high-level ideas to solve it, from *Kronrod*:

- Divide in blocks of `sqrt(N)`;
- Use last `sqrt(N)` of biggest numbers as a buffer;
- Sort blocks by their first number;
- Remember that selection sort has a predictable, linear number of moves (`N`).

At this point, I stopped reading to try and use those hints to come up with the rest of the algorithm on my own (what follows). The time spent thinking about the problem thankfully proved to be useful, because it was then much more straightforward to combine those hints with the tricks I developed while working on the problem.

For future personal reference, some clever ideas to remember that I think are pretty neat, which I didn't think of:

- Dividing in `sqrt(N)` tasks of `sqrt(N)` elements is a strategy to get `O(N)`;
- Keeping a small block of data as an unstructured buffer that we can fix in a "slow" way as a final step is fine (if it's small enough, like `sqrt(N)`, we can do `O((sqrt N)^2)` processing on it to stay `O(N)`!);
- Selection sort of `sqrt(N)` blocks does `sqrt(N)` swaps, which can matter for expensive swaps (e.g. swapping blocks of `sqrt(N)` elements!), so it's important to think about the cost of the swaps in some cases.

## High-Level Algorithm

Let's define our **block size** `Z = floor(sqrt(N))`.

Here will be the high-level steps:

1. Move the `Z` biggest elements to the end, which we'll call `buffer`.
   ​	`buffer` doesn't have to stay sorted -- we'll fix it at the end.
   ​	Divide `xs` and `ys` into blocks of exactly `Z` elements (assume we can, we'll make it happen in the detailed algorithm)
2. Sort the blocks according to their first elements.
3. For each block pairs, grab the `Z` smallest unsorted elements (using `buffer` as additional storage to do so).
4. Sort `buffer`.

General structure that we follow, to help visualize it:

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
2. `O(Z^2) = O(sqrt(N)^2) = O(N)` to sort blocks by their first elements, because with selection sort we can sort `Z` blocks with `O(Z^2)` comparisons of `O(1)` (comparing the first elements) with `Z` swaps (`O(Z)` to swap a block of `Z` elements), yielding `O(Z^2)` for comparisons + `O(Z^2)` for swaps, or `O(N)`;
3. Processing of `O(Z)` for each block to grab the `Z` smallest unsorted elements of the block and its next one, done for each `Z` blocks: `O(Z^2) = O(N)`;
4. Selection sort of a `buffer` of `Z` elements, `O(Z^2) = O(N)`.

If we're careful in our implementation of each step to use a constant amount of pointers, we get an algorithm that is `O(N)` time and `O(1)` extra memory!

## Detailed Algorithm

The code is heavily commented if you want to take a closer look at how this can be implemented, but here's a fairly detailed view of how this works.

### 0.5) Setup

Call our array to merge `A` (`N = len(A)`). Compute `Z = floor(sqrt(N))`.

Find `ys_start` (first element of `ys`) by going linearly through `A` to find the first unsorted element:

```python
ys_start = next(i for i in range(1, len(A)) if A[i-1] > A[i])  # O(N)
```

*Notes: perhaps there is a smarter way to find the pivot point here in O(lg N),
but since O(N) still satisfies our overall complexity goal we'll leave it
as-is.*

If we never find one, well the array is already sorted, we can exit already.

Then delimiters of start and length of `xs` and `ys` are easy to deduce:

```python
xs_start, xs_length = 0, ys_start
ys_length = N - xs_length
```

### 1) Move biggest elements to `buffer`

To move the `Z` biggest elements to the end of the array, we can do so in 2 steps:

1. Spot which elements of `xs` and `ys` are part of the `Z` biggest (call them `xs_to_move` and `ys_to_move`);
2. Move that many last elements of `xs` and `ys` to the end of the array (to what we'll then call `buffer`). We do so like such: rotate to move the smaller `ys` to be alongside the smaller `xs` (bringing the biggest numbers of both `xs` and `ys` to the back).

With an ASCII diagram:

```
|----------------xs-------------------|------------------ys-------------------|
#1: Z biggest elements:  ^^^^^^^^^^^^^                               ^^^^^^^^^

|----------------xs------|---xs_big---|--------------ys--------------|-ys_big-|
#2: rotate                <=======rotate-----------------------------|
|----------------xs------|---------------ys-------------|---xs_big---|-ys_big-|
                                                        |--------buffer-------|
```

 To do so, we'll need a few tools:

- **point_to_kth_biggest**: function to get pointers to the start of `xs_big` and start of `ys_big`;
- **rotate_k_left**: function to rotate `k` elements to the left.

```python
def point_to_kth_biggest(A, xs_start, xs_length, ys_start, ys_length, k):
  """Returns pointers within each sorted array such that one of them points
  to the kth biggest element, while the other one points to the last element
  seen within its subarray part of the k biggest elements.
  
  In simpler terms: point to the end of xs and ys and move, in descending order
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
    else: # 'xs' does
      x_ptr -= 1  # move x
  return x_ptr, y_ptr
```

We'll also need a rotate function, which we can cleverly implement linearly in-place with `invert` (learned about this technique through some stackoverflow answer that I can't find anymore, sadly):

```python
def rotate_k_left(A, start, length, k):
  """Rotate elements within an array k elements to the left, using inversions."""
  k %= length
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

Might as well implement `rotate_k_right` in while we're at it:

```python
def rotate_k_right(A, start, length, k):
  """Same as rotate_k_left, but to the right."""
  rotate_k_left(A, start, length, -k)
```

With a reminder of what we wanted to do:

```
|----------------xs-------------------|------------------ys-------------------|
#1:          xs_to_move: ^^^^^^^^^^^^^                   ys_to_move: ^^^^^^^^^

|----------------xs------|---xs_big---|--------------ys--------------|-ys_big-|
#2: rotate                <=======rotate-----------------------------|
|----------------xs------|---------------ys-------------|---xs_big---|-ys_big-|
                                                        |--------buffer-------|
```

We can make a generic function, **move_last_elements_to_end**, that moves the last `xs_to_move` elements from `xs` and last  `ys_to_move` elements from `ys` to the end of our array (in `buffer`):

```python
def move_last_elements_to_end(A, xs_start, xs_length, ys_start, ys_length,
                              buffer_length, xs_to_move, ys_to_move):
  """Moves the specified ends of both sorted subarrays to the end of A.
  
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
  rotate_k_left(A, start=new_ys_start, length=xs_to_move + new_ys_length,
                k=xs_to_move)
  return (new_xs_start, new_xs_length, new_ys_start, new_ys_length,
          new_buffer_start, new_buffer_length)  # dimensions of sections change
```

We can now get back to how we could move the `Z` biggest elements to the end:

```python
def move_k_biggest_elements_to_end(A, xs_start, xs_length, ys_start, ys_length, k):
  """Finds the 'k' biggest elements of A within 'xs' and 'ys' and move them to the end. 
  
  Assumes 'xs' and 'ys' are sorted, xs_start+xs_length=ys_start, k<=|xs|+|ys|.
  """
  xs_big_start, ys_big_start = point_to_kth_biggest(A, xs_start, xs_length,
                                                    ys_start, ys_length, k)
  
  # How many elements from xs and ys do we have to move?
  xs_top_elements = ys_start - xs_big_start
  ys_top_elements = ys_start + ys_length - ys_big_start
  (new_xs_start, new_xs_length, new_ys_start, new_ys_length,
   new_buffer_start, new_buffer_length) = move_last_elements_to_end(
    	A, xs_start, xs_length, ys_start, ys_length, buffer_length=0,
        xs_to_move=xs_top_elements, ys_to_move=ys_top_elements)
  return (new_xs_start, new_xs_length, new_ys_start, new_ys_length,
          new_buffer_start, new_buffer_length)
```

In the actual code, we make this clutter of keeping track of positions a little less worse by wrapping them in a structure (you can see why!)

If we called this with `k=Z`, `buffer` would now have `Z` elements. However, in order to make our next step work (making `xs` and `ys` multiples of `Z`), we'll end up moving a bit more than `Z` elements, and we'll explain why.

### 1.5) Make `|xs|` and `|ys|` multiples of `Z`

So, suppose we moved `Z` elements to the end and we wanted to make `xs` and `ys` multiples of `Z` (to make the rest of the algorithm simpler by knowing that all blocks have `Z` elements). My initial thought was to just move the `(mod Z)` leftover from each subarray to the end, but see this example:

```
2 3 4 5 6 7 8 9   1
^xs               ^ys     move Z=sqrt(9)=3 biggest elements to the end, we get:
2 3 4 5 6   1    7 8 9
^xs         ^ys  ^buf     if we move (mod 3) elements from 'xs' and 'ys' to the end:
2 3 4   5 6 1 7 8 9
^xs     ^buf
            !!! 'buffer' has '1', smaller than elements in 'xs'! 
```

 We can't guarantee that `buffer` has the `Z` biggest elements anymore, that's a problem. So that's not going to work.

The problem ultimately comes from the fact that we're trying to "push" the leftover `xs` and `ys` elements to `buffer` (elements that may not belong in `buffer`, because they're not the largest elements of `A`). Instead, we should use `buffer` as the set of largest elements of `A` that we can safely take from, to pad `xs` and `ys` to be multiples of `Z`. Let's change our previous step to move `3Z-2` elements to the end  (we want at least a `buffer` of `Z` plus max `Z-1` elements to pad `xs` to a multiple of `Z`, and `Z-1` elements to pad `ys` (and `Z + (Z-1) + (Z-1) = 3Z-2`)):

```python
# 1) Move Z+2(Z-1) biggest elements to the end (our buffer + elements to pad xs & ys).
(xs_start, xs_length, ys_start, ys_length,
 buffer_start, buffer_length) = move_k_biggest_elements_to_end(A, xs_start, xs_length,
                                                               ys_start, ys_length,
                                                               k=3*Z-2)
```

Next, to grab elements for `xs` and `ys` (to pad them to `0 (mod Z)` elements) while conserving the invariant that `buffer` has the biggest elements of `A`, we'll sort `buffer` (because our rotates to move `3Z-2` elements to `buffer` didn't sort them). We can do that in `O(Z^2)` by doing a selection sort (`O((3Z-2)^2) = O(Z^2)`. Then, as long as we grab the first elements of the sorted `buffer`, we conserve our invariant while successfully padding `xs` and `ys`.

Let's first implement a general selection sort, which we'll later use to sort blocks of elements, too:

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

Which we can use to implement a traditional sort for our buffer:

```python
def sort_buffer(A, start, length):
  def compare_buffer_elem(i, j): return A[start+i] < A[start+j]
  def swap_buffer_elem(i, j): A[start+i], A[start+j] = A[start+j], A[start+i]
  selection_sort(length=length, compare_fn=compare_buffer_elem,
                 swap_fn=swap_buffer_elem)
```

So now we have all the pieces:

```python
# 1.5) Make |xs| and |ys| multiples of Z. 
# Sort the buffer so that we can use its smaller elements to pad xs and ys.
sort_buffer(A, buffer_start, buffer_length)
# How many more elements do we need to reach 0 (mod Z)?
xs_needs = (-xs_length) % Z
ys_needs = (-ys_length) % Z
# Grab them from the smaller elements of buffer, via rotations.
#                           |-----------------buffer---------------------|
# |-----xs-----|-----ys-----|--ys_needs--|--xs_needs--|-buffer-remainder-|
#              |---------------------rotate==========>|
# To get:
# |-----xs-----|--xs_needs--|-----ys-----|--ys_needs--|-buffer-remainder-|
rotate_k_right(A, start=ys_start, length=ys_length + xs_needs + ys_needs,
               k=xs_needs)
xs_length += xs_needs
ys_start += xs_needs
ys_length += ys_needs
buffer_start += xs_needs + ys_needs
buffer_length -= xs_needs + ys_needs
```

Now, `buffer` has `< 3Z` elements (`Z + (-|X|) % Z + (-|Y|) % Z < 3Z`, which still keeps our final buffer-sorting step `O(Z)`). Buffer still has the biggest elements of `A`. `xs` and `ys` now have `0 (mod Z)` elements, so we can work with blocks of `Z` elements from now on.

*Note: at first I tried to move the `k` biggest elements to `buffer` in a way that would already have them sorted, but then I realized that this is similar in many ways to the merge problem that we're trying to solve in the first place... Overall I'm sure that there are ways to deal with padding to `0 mod Z` more efficiently here, but this seemed like a reasonably simple approach that stays within our algorithmic bounds.*

### 2) Sort blocks based on first element

From here, we're going to start mixing blocks from `xs` and `ys` together by sorting the blocks by their first element. To sort our blocks, we use selection sort. It has the nice property that it will do `<= |blocks|` swaps. Each block swap is `O(Z)` (swapping `Z` elements), for a total computation cost of `O(Z^2) = O(N)` for swapping `< Z` blocks (`sqrt(N)` blocks of `sqrt(N)` elements, minus the elements in `buffer`). Selection sort on blocks will do `O(Z^2) = O(N)` comparisons (`O(|blocks|^2)`). The swap and comparison costs conserve our `O(N)` time complexity requirement.

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

Now what's interesting about having sorted blocks in this way is that, if we take the first 2 adjacent blocks afterwards and assume that everything to the left of them is fully sorted (in their final positions in `A`, i.e. in the middle of the algorithm), they are guaranteed to contain the next `Z` smallest elements of the unsorted part of `A`. Diagram to help picture that:

```
|-----:-----:-----:-----|--a--:--b--|--c--:--d--:--e--:--f--:--g--|-buffer-|
 ^^^^^^^^^^^^^^^^^^^^^^^|===========|
   sorted elems of A          ^ contains Z smallest elements of
        (final)                 U{a, b, ..., f, g}
```

Why is that?

- If both blocks are from the same original sorted subarray (assume they are both from `xs` , but the logic holds for `ys` too), then step 2 would not have changed their relative ordering and they would have remained sorted in their original order.
  - So, we know that the first block of `Z` elements would be the smallest `Z` elements out of all the remaining `xs` (they're the same as the original sorted `xs` subarray);
  - We know that no `ys` element can be smaller than any `xs` element within the first block. This is because the first element of the second `xs` block is bigger than any `xs` element in the first block (retained their order from the original `xs` subarray), and no `ys` element is smaller than the first element from the second block (otherwise the second block would come from `ys`!);
  - This means that this first block is in its final position, and we can skip it altogether (it already has the `Z` smallest elements, in order).
- If both blocks originate from different sorted subarrays (assume the first block is from `xs` and the second from `ys`, but logic holds both ways), then the first block contains the smallest `Z` remaining elements of `xs` (similar logic as the precedent case) and the second block contains the smallest `Z` remaining elements of `ys` (same idea). Thus, the `Z` smallest elements of the two blocks are the `Z` smallest elements of `U{xs, ys}`.

We'll go over an example in the next section to make this clearer and expand on the guarantees we preserve.

### 3) Grab `Z` smallest unsorted elements for each block

This is where the ideas behind the hints for Kronrod's algorithm get really elegant, in my opinion.

For this step, we ultimately want to go through `A`, one block at a time, doing a merge (**not** in-place!) between the current block and the next. How can we afford to do it with extra memory? By using our buffer that we created in step 1! There's something that feels very elegant (if not a bit claustrophobic) about implementing an in-place algorithm by using the additional-memory version of itself, using a temporary working area of the input data.

Let's focus on the implementation first, then go into more detail about why that properly sorts the array `A`.

Let's start with the implementation of merging with a buffer (notice the similarities with our very first `O(n)` memory naive approach):

``` python
def merge_into_target(A, xs_start, ys_start, target, length):
  """Merges the sorted xs and ys (same length), swapping with elements at 'target'.
  
  Note that this works even if ys_start (or xs_start) equals target+length, e.g.:
  |-----------|-----------|----------- ... -----------|-----------|
  ^ target    ^ ys_start                              ^ xs_start
  
  Whenever 'target' reaches ys_start during the merge, the current y pointer is, in
  the worst case, still at ys_start (if all xs are smaller than all ys). From there,
  we can't overwrite values from ys, because we'd essentially swap y elements with
  themselves (so, in other words, current target is always <= current y pointer).
  
  Assumptions:
  - 'target' has enough space to hold 2*length elements;
  - [target, target+length) does not overlap with xs or ys, the rest can overlap.
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

Remember: `a` is sorted, `b` is sorted, both of length `Z` (`sqrt(N)`). We want to merge them. We can use our `buffer` as needed (which has size `>= Z`). We'll swap `a` (first block) with the start of `buffer`. Then we can use the start of our original `a` as a target directly (that's where we want our merged blocks anyway!) Using our property that it's fine to have our second block be at `target + Z`, we're ready to go:

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

#### (Why) Does this work?

For this step to sort the blocks of `Z` elements and produce a sorted `[0, buffer_start)` subarray, we mostly care about two things:

- Does each block sort guarantee that it will grab the `Z` smallest elements of all that is remaining?
- Does this leave the following block in a state that will preserve that guarantee for the next iterations?

To expand on why this does grab the `Z` smallest elements of `[current_block, buffer_start)` while preserving an overall `xs`/`ys` block structure, let's look at an example with marked elements (note: indices here are relative, they're not the absolute indices of `xs`/`ys` elements), assuming `Z=4`.

##### `xs` current block, `xs` next block

Let's start with the easier case where `current_block` comes from `xs`, and `next_block` also comes from `xs` (similar logic for both coming from `ys`):

```
a0 a1 a2 a3 | a4 a5 a6 a7 ... | x0 x1 x2 x3 | x4 x5 x6 x7 | y0 y1 y2 y3 | ...
```

Of note:

- We don't care about the `a0 ... a7`, we assume they're already sorted and smaller than every element after them (from previous iterations in this step of the algorithm).
- We assume what follows `x7` is `y0` (values from `ys`). There could be more blocks of `xs` before the next value coming from `ys`, but in terms of an analysis of "are we sure this grabs the `Z` smallest unsorted elements", we want to pay attention to `xs`/`ys` boundaries, since we know the `xs` are already sorted relative to eachother, and the first block of `Z` elements from `xs` will be the `Z` smallest `xs`elements.

To reiterate what was brought up in the previous section:

- We know that the smallest `Z` elements of `x0 x1 x2 x3 | x4 x5 x6 x7` will be `x0 x1 x2 x3`. They were kept as sorted from the original `xs`. So `x0 x1 x2 x3` are the smaller `Z` elements of the remaining `xs`.
- We know that `x0 < x1 < x2 < x3` (original `xs` sort), we similarly know that `x3 < x4` (thus all elements in the current block are smaller than `x4`), we know that `x0 < x4 < y0` because of the previous step's sorting based on each block's first element, we know that `y0` is the smallest of all `ys`. From that, we know that `x0 x1 x2 x3` are the smallest `Z` elements from the remaining `xs` and `ys`.

We can then just skip that block! The remaining blocks are left intact, so there's nothing else to do to show that this preserves the guarantees for next iterations.

##### `xs` current block, `ys` next block

Let's look at the case where the blocs don't come from the same original subset, `current_block` comes from `xs`, and `next_block` comes from `ys` (similar logic if we swap those labels):

```
a0 a1 a2 a3 | a4 a5 a6 a7 ... | x0 x1 x2 x3 | y0 y1 y2 y3 | ...
```

We know that `x0 .. x3` are the smallest elements of the remaining `xs`, and that `y0 .. y3` are the smallest elements of the remaining `ys`, so the first `Z` elements of `sort(x0 x1 x2 x3 y0 y1 y2 y3)` are the smallest elements of all that's remaining.

But what about the last `Z` elements of `sort(x0 x1 x2 x3 y0 y1 y2 y3)` (which will become our next block)? For our analysis to hold for all blocks, we must show that this next block that we are creating post-sort can be considered elements of `xs` or `ys`, since we make some of our arguments using assumptions on `xs` and `ys`. In this case, whatever "label" was associated with the biggest element from that sort of `current_block` and `next_block`, we conceptually label the entire block with that. For example, if `y3 > x3` (i.e. `y3` ends up last), we call this new block a block of `ys`. If `x3 > y3` (i.e. `x3` ends up last), we call this a block of `xs`. This makes it such that the overall ordering of `xs` (or `ys`) is preserved like before, since this block is ordered, and the last element is still smaller than the other elements from that "group". For all intents and purposes, we consider that new block as if it was from `xs` (or `ys`) in the first place (since it preserves the properties we care about).

What about the first element of that next block? Is it still ordered compared to the first element of following blocks (i.e. what we did in step #2)?

- If that new first element originally came from `xs`, then we know it is already ordered against following `xs` blocks. Now, note that `x0` in that example will stay where it's at (it's the smallest of `x0 x1 x2 x3`, and we know `x0 < y0` from step #2 of our algorithm, so it's the smallest element of both blocks). That means that we can only have 3 `xs` in that new block, so surely we have at least one element from `ys`. Thus, that new first element is smaller than some `ys` element, so it will be smaller than the following `ys` blocks. So yes, it would preserve our first-element ordering.
- If that new first element came from `ys` instead, we know it is already ordered against following `ys` blocks. If all block elements are from `ys`, then `y0 y1 y2 y3` stayed as-is, and the first-element ordering is unchanged. If some elements from the new block are from `xs`, then with a similar argument to the previous point, we know that it must be smaller than future `xs` blocks, too.

So that's it! The properties hold for each block, and by the time we have processed all of them, our entire array (aside from `buffer`) is sorted, all in `O(N)` time, with no extra space.

### 4) Sort `buffer`

This part's easy, we've done it before:

```python
sort_buffer(A, buffer_start, buffer_length)
```

And we're done!

## Full Example

This is a lot to take in, let's look at an example to get a feel for the structure and operations of this algorithm. Note that all of this processing will feel superfluous and costly for such a small array, but keep in mind that an in-place linear algorithm like this could be used even if the array was `1 PiB` big, while still being linear in time and constant in extra space.



We will be merging an example array that I generated randomly by shuffling 27 ints, splitting them, then sorting each subarray:

```
1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 25, 0, 8, 10, 18, 19, 20, 24, 26
```

### 0.5) Setup

`N = 27`, `Z=5`

```
1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 25, 0, 8, 10, 18, 19, 20, 24, 26
^                                                                   ^
xs                                                                  ys
```

We calculate:

`xs_start = 0`, `xs_length = 19`, `ys_start = 19`, `ys_length = 8`

### 1) and 1.5) Move biggest elements to `buffer`, making `|xs|` and `|ys|` multiples of `Z`.

First, we want to move the `3Z-2 = 3(5)-2 = 13` biggest elements to `buffer`. We find pointers in `xs` and `ys` of the `13` elements to move:

```
1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 25, 0, 8, 10, 18, 19, 20, 24, 26
[0th biggest]                                                       ^ xs_biggest                  ^ ys_biggest
[1st biggest]                                                       ^ xs_biggest              ^ ys_biggest
[2nd biggest]                                                   ^ xs_biggest                  ^ ys_biggest
...
[13th biggest]                      ^ xs_biggest                              ^ ys_biggest
```

From there, we rotate left by `13` to move them to the end, which we'll now call buffer:

```
1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 25, 0, 8, 10, 18, 19, 20, 24, 26
|-----------------------------------******************************------------*****************| (to move)
                                    <==========================rotate--------------------------|
1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 0, 8, 10, 18, 19, 20, 24, 26, 14, 15, 16, 17, 21, 22, 23, 25
|----------------xs---------------| |---ys--| |--------------------buffer----------------------|
```

Sort `buffer`, with selection sort:

```
1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 0, 8, 10, 18, 19, 20, 24, 26, 14, 15, 16, 17, 21, 22, 23, 25
|----------------xs---------------| |---ys--| |--------------------buffer----------------------|
1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 0, 8, 10, 18, 19, 20, 24, 26, 14, 15, 16, 17, 21, 22, 23, 25
                                              ^                   ^ (swap)
1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 0, 8, 10, 14, 19, 20, 24, 26, 18, 15, 16, 17, 21, 22, 23, 25
                                                  ^                   ^ (swap)
1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 0, 8, 10, 14, 15, 20, 24, 26, 18, 19, 16, 17, 21, 22, 23, 25
...

1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 0, 8, 10, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
|----------------xs---------------| |---ys--| |--------------------buffer----------------------|
```

Pad `xs ` and `ys` to become multiples of `Z=5`:

- Need to pad with`xs_needs = 4`, `ys_needs = 2` elements to become multiples of `5`.

```
1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 0, 8, 10, 14, 15,   16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
|----------------xs---------------| |---ys--| |ys-needs|---xs-needs---|----------buffer----------|
                                    |---------------rotate============>
1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 16, 17, 18, 19, 0, 8, 10, 14, 15, 20, 21, 22, 23, 24, 25, 26
|--------------------xs---------------------------| |------ys-------| |--------buffer----------|
```

### 2) Sort blocks based on first element

Now we can conceptually break up `xs` and `ys` into blocks of `5` elements:

```
1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 16, 17, 18, 19, 0, 8, 10, 14, 15, 20, 21, 22, 23, 24, 25, 26
|-------------:---------xs-----:-------------------|-------ys--------|----------buffer---------|
```

Sort each of the blocks based on their first elements (highlighted), using selection sort:

```
1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 16, 17, 18, 19, 0, 8, 10, 14, 15, 20, 21, 22, 23, 24, 25, 26
^              ^                ^                   ^                | ... buffer
*                                                   * (swap)
0, 8, 10, 14, 15, 6, 7, 9, 11, 12, 13, 16, 17, 18, 19, 1, 2, 3, 4, 5, 20, 21, 22, 23, 24, 25, 26
^                 ^                ^                   ^             | ... buffer
                  *                                    * (swap)
0, 8, 10, 14, 15, 1, 2, 3, 4, 5, 13, 16, 17, 18, 19, 6, 7, 9, 11, 12, 20, 21, 22, 23, 24, 25, 26
^                 ^              ^                   ^               | ... buffer
                                 *                   * (swap)
0, 8, 10, 14, 15, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
^                 ^              ^                ^                  | ... buffer
```

### 3) Grab `Z` smallest unordered elements for each block

For each blocks (note: we have 4 blocks total here), do our non-in-place merge.

Block `[0,5)`:

```
0, 8, 10, 14, 15, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
|-current_block-| |-next_block-|                                     |---------buffer----------|
```

The sorting process, where we do a **non-in-place** merge using `buffer` as "extra" space:

```
0, 8, 10, 14, 15  |  1, 2, 3, 4, 5  [...]  20, 21, 22, 23, 24, 25, 26
^^^^^^^^^^^^^^^^                           ^^^^^^^^^^^^^^^^^^ (move block to buffer)
20, 21, 22, 23, 24  |  1, 2, 3, 4, 5  [...]  0, 8, 10, 14, 15  |  25, 26
^                      ^                     ^ (next smallest)
0, 21, 22, 23, 24  |  1, 2, 3, 4, 5  [...]  20, 8, 10, 14, 15  |  25, 26
   ^                  ^ (next smallest)         ^
0, 1, 22, 23, 24  |  21, 2, 3, 4, 5  [...]  20, 8, 10, 14, 15  |  25, 26
...

0, 1, 2, 3, 4, 5, 8, 10, 14, 15, 6, 7, 9, 11, 12, 13, 16, 17, 18, 19, 20, 22, 23, 24, 21, 25, 26
<### done ###> |---next_block--|                                      |---------buffer---------|
```

Now block `[0, 5)` is done! Notice how buffer was shuffled around a bit -- that's fine, we sort it at the end.

Block `[5,10)`:

```
0, 1, 2, 3, 4, 5, 8, 10, 14, 15, 6, 7, 9, 11, 12, 13, 16, 17, 18, 19, 20, 22, 23, 24, 21, 25, 26
<### done ###> |-current_block-| |--next_block--|                     |---------buffer---------|
...

0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 13, 16, 17, 18, 19, 20, 24, 22, 23, 21, 25, 26
<########## done ###########> |---next_block----|                     |---------buffer---------|
```

Block `[10,15)`:

```
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 13, 16, 17, 18, 19, 20, 24, 22, 23, 21, 25, 26
<########## done ###########> |--current_block--| |---next_block----| |---------buffer---------|
...

0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24, 22, 21, 23, 25, 26
<#################### done #####################> |---next_block----| |---------buffer---------|
```

And note that for our last block (`[15,20)`) we don't have to do anything, since our two-block sorting has already taken care of it!

```
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24, 22, 21, 23, 25, 26
<############################## done ###############################> |---------buffer---------|
```

### 4) Sort `buffer`

We just do a selection sort, like we've done before:

```
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24, 22, 21, 23, 25, 26
<############################## done ###############################> |---------buffer---------|
...

0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
```

And we are done!

## Merge Sort

What's neat is that we now have a very nice primitive to implement a simple bottom-up merge sort in-place that's `O(n lg n)` if we want to:

- We start with subarrays of size `1`, merge each pair of subarrays, using our algorithm (this one is a bit trivial, only involves swaps);
- Double subarrays size (`2` now), merge each pair of subarrays (which we know are already sorted from our previous step);
- Double subarrays size (`4` now), merge;
- Continue until the subarrays size is as big as `A`.

We end up doing `lg N` iterations, where each of them goes over `N` elements.

We can rework the code from before to handle relative positions within an array to implement our merge sort:

```python
# Assuming our previous code is available under `merge_inplace(array, start_idx, length)`.

def merge_sort_inplace(A):
    size = 1  # powers of 2
    while size < len(A):  # lg N iterations
        for xs_start in range(0, len(A), size * 2):  # goes over N elements
            ys_start = xs_start + size
            length = min(len(A), ys_start + size) - xs_start
            merge_inplace(A, start_idx=xs_start, length=length)
        size *= 2
```

This is perhaps a bit too involved in terms of practical constants just for doing a sort! Maybe there would be a better way to take advantage of the fact that most subarrays (except the last ones) will have the same size when merging, too. But our more general merge is still usable here and this is a nice showcase of it.

## Peeking

Now that we have a functional linear in-place algorithm (although with quite a bit of intricate steps), let's look at the "real" version of this algorithm, and inspect the differences.

I had a hard time finding the Kronrod source from 1969, but did find the exercise and its answer in the Volume 3 of The Art of Computer Programming,  section 5.2.4, exercise #18:

```
[40] (M. A. Kronrod.) Given a file of N records containing only two runs,

    K_1 <= ... <= K_M    and    K_{M+1} <= ... <= K_N,

is it possible to sort the file with O(N) operations in a random-access memory,
using only a small fixed amount of additional memory space regardless of the
sizes of M and N? (All of the merging algorithms described in this section make
use of extra memory space proportional to N.)
```

Of note, this exercise has difficulty 40! No wonder this was a difficult task.
In Donald Knuth's words, an exercise of difficulty 40 is:

```
Quite a difficult of lengthy problem that would be suitable for a term project
in classroom situations. A student should be able to solve the problem in a
reasonable amount of time, but the solution is not trivial.
```

We can look at Donald Knuth's notes on Kronrod's algorithm in the answers section of the book.

### Handling of duplicates

While the overall structure is similar (naturally, we started from hints based on Kronrod's work), there are a bunch of differences. The first one that stood
out to me is a small note when sorting blocks based on their first element:

```
If more than one zone has the smallest leading element, choose one that has the
smallest trailing element.
```

We did not pay a lot of attention to duplicate elements in our analysis of the algorithm, and at first I suspected a bug if I specifically included a block full of duplicates to mess with the first-element sorting that we are currently doing , e.g. `3 8 9   3 3 3   3 4 5`. As much as I tried to produce a buggy example, it seems that our current algorithm is still working despite not adding a check on the trailing element when leading elements match.

I might be missing something, but ultimately duplicates don't impact the two main properties we rely on for our blocks:

 - Leading block elements are in ascending order.
 - Each block is sorted, and comes from `xs` or `ys`, in the same relative order that they appeared in their source subarray.

And we maintain those properties as we sort one block at a time, regardless of duplicates. Perhaps I _am_ missing something, or perhaps this is only necessary with the approach presented in the book.

### Simpler handling of block remainders

The next thing that stands out is the overall handling of the remainder blocks of `xs` and `ys`. We approached it by a pretty tedious process of extracting the `3Z-2` biggest elements, sorting them, then rotating to pad `xs` and `ys` with enough elements to be multiples of `Z`.

In Knuth's notes about Kronrad's algorithm, we see that we can simplify our overall preparation and leave some things to be fixed by later processing. The algorithm described in the book is the following, adapted to keep the terms we've been using here:

```
Divide the array in blocks of Z (i.e. sqrt N) elements each, except the last
block will contain N mod Z elements. Call the last two blocks (size Z +
(N mod Z)) area our buffer. Call len(buffer) 's'.

The block containing the last element of 'xs' is swapped with the
previous-to-last block.

Sort the m blocks based on their leading elements, comparing trailing
elements when leading elements are equal.

Merge each pairs of blocks in order by first swapping the first block with our
buffer area, then merging into the first block's original position.

For the final cleanup, sort 2*s elements at the end of our array with insertion
sort, this brings the s largest elements into our buffer. Then, merge A_{1..N-2*s}
and A_{N-2*s..N-s} using a similar trick as our block merging, swapping left/right
and less/greater. Finally, sort buffer by insertion.
```

Some notes:
 - Only `Z + (N mod Z)` elements in buffer, and throughout the algorithm buffer does not necessarily hold the biggest elements. This is remedied via extra cleanup at the end.
 - The swap of the last block of `xs` to move it to buffer cuts into `ys`'s start if `xs` isn't a multiple of `Z`, but this is fine as the `ys` stays
   sorted overall. `buffer` won't have only the biggest elements, but we fix that in cleanup.
 - The block that we bring at the end of `xs` via swapping might not fit there, but when we sort blocks by first elements we mitigate that. Perhaps this is where looking at the trailing element matters, I'm not sure.
 - Same block merging logic as we implemented, which is somewhat encouraging.
 - The final cleanup is clever -- the block sort & merge steps give us sorted elements before our buffer, so sorting `2s` elements at the end will get us the s largest elements in buffer. The elements we were holding in buffer that are now moved back in our array are not necessarily in order, so we need to merge the big portion of our array with what we just moved in there to restore that. We use `buffer` as temporary storage in the process, so we
   finally re-sort it to make up for it.

In a way, this approach is akin to moving the processing from preparation to cleanup instead. I have to imagine my approach, while equivalent in algorithmic complexity, is suboptimal in comparison, but I'd be curious to compute by how much.

We can implement Kronrad's algorithm relatively simply, with the primitives we built (available as `merge_inplace_kronrad` or via `kronrad` parameter of `merge_inplace`):

```python
def merge_inplace_kronrad(R, N):
    # Note: using the same terminology as TAOCP here.
    M = array_utils.find_first_unsorted_index(R, start=0, length=N)

    n = int(math.sqrt(N))
    s = s + N%n  # length of 'auxiliary' area

    # Prepare auxiliary storage.
    aux_start = N - s
    zone_R_M = (M-1) // n  # zone that contains R_M
    # If R_M is in our last zone, need to make sure we don't swap past the end.
    swap_len = min(n, N - (zone_R_M * n + n))
    array_utils.swap_k_elements(R, start=zone_R_M*n, k=swap_len,
                                target=aux_start)

    # Sort & merge blocks.
    # Very much like our previous algorithm!
    for i in range(0, N-s-n, n):
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
    for i in reversed(range(aux_start)):
        if y < aux_start:
            break  # Swapped the last auxiliary element, we are done.
        if x >= 0 and R[x] > R[y]:
            R[x], R[i] = R[i], R[x]
            x -= 1
        else:
            R[y], R[i] = R[i], R[y]
            y -= 1
    _selection_sort(R, start=aux_start, length=s)
```

Relatively concise! We could probably rework `_merge_into_target` in a more general form such that it could handle both cases, too.

### Refinements

This was an interesting theoretical challenge with a focus on algorithmic complexity, but clearly the practical constants can't be ignored, and we did not ensure stability (duplicate elements preserve their relative ordering).
Subsequent refinements to Kronrod's 1969 algorithm were made (see [this report](https://nms.kcl.ac.uk/informatics/techreports/papers/TR-04-05.pdf) for an example overview), but the core ideas (using an _internal buffer_ and _block rearrangement_) remain.
