# In-Place Linear Merge

A colleague of mine gave me an interesting challenge: to essentially do the merge part of a merge-sort in `O(N)` time and `O(1)` extra space. A bit more formally:

Given an array of `N` elements split in two sorted subarrays:

​	`x0  x1  ...  xn   y0  y1  ...  ym` 

​	(where `n+m = N` , `x0  x1  ...  xn` are sorted and `y0  y1  ...  ym` are sorted),

merge both subarrays such that the final array of `N` elements is sorted. Do so in time `O(N)` and `O(1)` extra memory. In short, merge two sorted arrays in-place linearly.

A concrete example:

`0  7  8  10   1  2  3  4  5  6  9`

Would have to be sorted in `O(N)`, without an additional memory requirement that grows with `N`, as:

`0  1  2  3  4  5  6  7  8  9  10`

*Note: by "in-place" and "`O(1)` extra space", I really mean "a constant number of pointers into the array" ([LSPACE](https://en.wikipedia.org/wiki/L_(complexity))), which amounts in reality to `O(lg n)` additional memory. Keep this in mind whenever you see `O(1)` memory.*

## Naive Approaches

To appreciate the complexity of the problem, it helps to see why and how naive approaches fail.

If we didn't care about `O(N)` time, we could use an in-place sort algorithm (probably not merge-sort, which would likely use a function like the one we're trying to code here... :-) ) to solve it in `O(n lg n)`.

If we didn't have the `O(1)` memory requirement, we could easily build a new sorted array from copying, in order, from both subarrays:

```python
first_y = index_first_out_of_order(original)
x, y = 0, first_y  # ptrs within subarrays
new = list(original)  # make a new array of N elements
for i in range(len(new)):
	if x < first_y and original[x] < original[y]:
		new[i] = original[x]
       	x += 1
	else:
  		assert y < len(original)
 		new[i] = original[y]
 		y += 1
```

But we're not allowed the `O(N)` extra memory.

What if we blindly tried this approach, but did it all in-line with swaps instead of doing copies to separate storage? We'd run into issues pretty fast:

```
4  5  8  9   0  1  2  3  6  7
^            ^ (swap)
0  5  8  9   4  1  2  3  6  7
             !  ! (ys not sorted anymore)
```

We break the sort on `ys`, which is a problem because then we would need to remember that there's a `4` sitting there that will eventually be the smallest element to grab (after `1  2  3`). We could try to remember that this one element is sitting there (with a pointer), but then how many more elements will we need to remember in the same manner before getting to that `4`? If we can come up with examples where that bookkeeping grows with `N`, we're no longer `O(1)` memory.

What if we try to move the `4` to where it belongs in `ys`, via an `O(k)`  rotate (`k` being the number of elements in `ys` that are `< 4`), before doing that swap? A strategy like that would break down if we have something like this:

```
5  6  7  8  9   0  1  2  3  4
```

because we would swap the `5`, rotate it to the right of `ys`, swap the `6`, rotate it to the right, ... We would have to shift each `N/2` `xs` elements to the right of `ys` (which takes `O(N/2)`), which would lead to `O(N^2)`.

What if instead of just swapping the `0` with the `4` in our first example, we also swap any other `ys` numbers that we *know* will come before `4`:

```
4  5  8  9   0  1  2  3  6  7
^  -  -  -   ^  ^  ^  ^ (0 1 2 3 must be swapped because < 4)
0  1  2  3   4  5  8  9  6  7
                      !  ! (ys not sorted anymore)
```

No dice. The problem is that by doing this we can bring in numbers that are bigger than what will follow them once in `ys` (e.g. `8` and `9` > `6`).

Clearly, coming up with simple ideas and trying to "patch" the counterexamples that we find isn't working out (what a surprise!)

## Hints

I spent a long time exploring a bunch of ideas.

I considered finding the `(n+1)`th smallest element in `O(N)` (by having a pointer on `xs` and one on `ys` and moving one at a time until we moved `n+1` times), which would then give us the element that belongs at the index of `y0`, call it `P` (at the `nth` index). Then, I was hoping I could partition `xs` and `ys` to move the elements `<= P` to `xs`, and the ones `> P` to `ys`.

By naively doing so, I could have two subarrays that each contained two sorted subarrays to merge... so no closer to solving the problem in `O(N)` than initially.

I played with ideas to move the elements `<= P` to `xs` while ensuring that they are in a sorted order in `xs` (so solving the problem for the first `n` elements!) Then, if I could find a way to maintain two sorted subarrays in the elements that I have to move to `ys`, I could hopefully maybe have sorted `n` elements in `O(n)` with an array of`m` elements (`N-n`) left to merge. However, finding a way to do that proved to be quite hard, or at least not in a way that would have been `O(n)`.

At this point I decided to read up on the problem a bit more, to see if there were theoretical tools that I was missing to find a solution. I ended up finding resources on the problem itself, with [this stackoverflow question](https://stackoverflow.com/q/2126219) standing out.

Turns out this isn't exactly a trivial problem (one that I'll see in TAOCP Vol. 3!), and likely not one one would encounter in an interview. The stackoverflow answers link to some relatively old papers that address it, and give some very helpful ideas to solve it, from *Kronrod*:

- Divide in blocks of `sqrt(N)`;
- Use last `sqrt(N)` of biggest numbers as buffer;
- Sort blocks by their first number;
- Selection sort has a predictable number of moves (`N`).

At this point, I stopped reading to try and use those hints to come up with the rest of the algorithm on my own (what follows). The time spent thinking about the problem thankfully proved to be useful, because it was then much more straightforward to combine those hints with the tricks I developed while working on the problem.

For future personal reference, some ideas that I think are pretty neat and could help me in the future:

- Dividing in `sqrt(N)` tasks of `sqrt(N)` elements is a way to get `O(N)`;
- Keeping a small block of data as an unstructured buffer that we can fix in a "slow" way as a final step is fine (if it's small enough like `sqrt(N)` we can do `O(N^2)` processing on it to stay `O(N)`!);
- Selection sort of `sqrt(N)` blocks does `sqrt(N)` swaps, which can matter for expensive swaps (e.g. swapping blocks of `sqrt(N)` elements!).

## High-Level Algorithm

Let's define `Z = floor(sqrt(N))`.

Here will be the high-level steps:

1. Move the `Z` biggest elements to the end, which we'll call `buffer`.
   ​	`buffer` doesn't have to stay sorted, we'll fix it later.
   ​	Divide `xs` and `ys` into blocks of `Z` elements (assume we can, we'll fix in detailed algorithm)
   ​	TODO(emond): diagram here
2. Sort the blocks according to their first elements.
3. For each block, grab the `Z` smallest unsorted elements (using `buffer` as buffer to do so).
4. Sort `buffer`.

The trick here is that the setup that we create (having blocks sorted by their first elements) allows us to do step 3 in `O(Z)` for each block, giving us the following time complexities per step:

1. `O(Z)` to grab the `Z` biggest elements;
2. `O(Z^2) = O(sqrt(N)^2) = O(N)`, because with selection sort we can sort `Z` blocks with `O(Z^2)` comparisons of `O(1)` (comparing the first elements) with `Z` swaps (`O(Z)` to swap a block of `Z` elements), yielding `O(Z^2)` for comparisons + `O(Z^2)` for swaps;
3. Processing of `O(Z)` for each block to grab the `Z` smallest unsorted elements, done for each `Z` blocks: `O(Z^2) = O(N)`;
4. Selection sort of a buffer of `Z` elements, `O(Z^2) = O(N)`.

If we're careful in our implementation of each step to use a constant amount of pointers, we get an algorithm that is `O(N)` time and `O(1)` extra memory!

## Detailed Algorithm

The code is heavily commented if you want to take a closer look at how this can be implemented.

### 0.5 Setup

Call our array to merge `A`. Compute `Z = floor(sqrt(N))`.

Find `ys_start` (first element of `ys`) by going linearly through `A` to find the first unsorted element:

```
ys_start = next(i for i in range(1, len(A)) if A[i-1] > A[i])
```



### 1. Move `Z` biggest elements to `buffer`

TODO

### 1.5 Make `xs` and `ys` multiples of `Z`

TODO

### 2. Sort blocks based on first element

TODO

### 3. Grab `Z` smallest unsorted elements

TODO

### 4. Sort `buffer`

TODO

## Full Example

TODO

## Merge Sort

TODO