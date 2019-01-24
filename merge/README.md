# In-Place Linear Merge

A colleague of mine gave me an interesting problem: to essentially do the merge part of a merge-sort in `O(N)` time and `O(1)` extra space. A bit more formally:

Given an array of `N` elements split in two sorted subarrays:

​	`x0  x1  ...  xn   y0  y1  ...  ym` 

​	(where `n+m = N` , `x0  x1  ...  xn` is sorted and `y0  y1  ...  ym` is sorted),

merge both subarrays such that the final array of `N` elements is sorted. Do so in time `O(N)` and `O(1)` extra memory. In short, merge two sorted arrays in-place linearly.

A concrete example:

`0  7  8  10   1  2  3  4  5  6  9`

Would have to be sorted in `O(N)`, without an additional memory requirement that grows with `N`, as:

`0  1  2  3  4  5  6  7  8  9  10`

*Note: by "in-place" and "`O(1)` extra space", I really mean "a constant number of pointers into the array", which amounts in reality to `O(lg n)` additional memory. Keep this in mind whenever you see `O(1)` memory.*

## Naive Approaches

To appreciate the complexity of the problem, it helps to see why and how naive approaches fail.

If we didn't care about `O(N)` time, we could use an in-place sort algorithm (likely not merge-sort, which would likely use a function like the one we're trying to code... :-) ) to solve it in `O(n lg n)`.

If we didn't have the `O(1)` memory requirement, we could easily build our sorted array from copying, in order, from both subarrays:

```python
xs, ys = split(orig)  # find first unsorted element (y0) to split in the two subarrays
new = list(orig)  # make a new array of N elements
for i in range(len(new)):
	if len(xs) > 0 and xs[0] < ys[0]:
		new[i] = xs[0]
       	xs = xs[1:]  # move forward within xs
	else:
  		assert len(ys) > 0
 		new[i] = ys[0]
 		ys = ys[1:]  # move forward within ys
```

But we're not allowed the `O(N)` extra memory.

What if we blindly tried this, but stored the results in-line with swaps instead of doing copies to separate storage? We'd run into issues pretty fast:

```
4  5  8  9   0  1  2  3  6  7
^            ^ (swap)
0  5  8  9   4  1  2  3  6  7
             !  ! (ys not sorted anymore)
```

We break the sort on `ys`, which is a problem because then we would need to remember that there's a `4` there that will be the smallest element to place at some point (after `1  2  3`). We could try to remember this one element, but then how many more elements will we need to remember in the same manner before getting to that `4`? If we can come up with examples where that grows with `N`, we're no longer `O(1)` memory with our bookkeeping.

What if I try to move the `4` to where it belongs in `ys`, via an `O(k)`  rotate? A strategy like that would break down if I have something like this:

```
5  6  7  8  9   0  1  2  3  4
```

because I would swap the `5`, rotate it to the right of `ys`, swap the `6`, rotate it to the right, ... I would have to shift each `N/2` `xs` elements to the right of `ys` (which takes `O(N/2)`), which would lead to `O(N^2)`.

What if instead of just swapping the `0` with the `4` in my first example, I also swap any other `ys` numbers that I *know* will come before `4`:

```
4  5  8  9   0  1  2  3  6  7
^  -  -  -   ^  ^  ^  ^ (0 1 2 3 must be swapped because < 4)
0  1  2  3   4  5  8  9  6  7
                      !  ! (ys not sorted anymore)
```

No dice. The problem is that by doing this we can bring in numbers that are bigger than what will follow them once in `ys` (e.g. `8` and `9` > `6`).

Clearly, coming up with simple ideas and trying to "patch" the counterexamples that we find isn't working out (what a surprise).

## Hints

I spent a long time exploring a couple ideas.

I considered finding the `(n+1)`th smallest element in `O(N)` (by having a pointer on `xs` and one on `ys` and moving one at a time until we moved `n+1` times), which would then give us the element that belongs at the index of `y0`, call it `P` (at the `nth` index). Then, I was hoping I could partition `xs` and `ys` to move the elements `<= P` to `xs`, and the ones `> P` to `ys`.

By naively doing so, I could have two subarrays that each contained two sorted subarrays to merge... so no closer to solving the problem in `O(n)` than initially.

I played with ideas to move the elements `<= P` to `xs` while ensuring that they are in a sorted order in `xs`. Then, if I could find a way to maintain two sorted subarrays in the elements that I have to move to `ys`, I could hopefully maybe have sorted `n` elements in `O(n)` with an array of`m` elements (`N-n`) left to merge. However, finding a way to do that proved to be quite hard, or at least not in a way that would have been `O(n)`.

At this point I decided to read up on the problem a bit more, to see if there were theoretical tools that I was missing to find a solution. I ended up finding resources on the problem itself, with [this stackoverflow question](https://stackoverflow.com/q/2126219) standing out.

Turns out this isn't exactly a trivial problem (one that I'll see in TAOCP Vol. 3!), and likely not one you would encounter in an interview. The stackoverflow answers link to some relatively old papers that address it, and give some very helpful ideas to solve it, from *Kronrod*:

- Divide in blocks of `sqrt(N)`;
- Use last `sqrt(N)` of biggest numbers as buffer;
- Sort blocks by their first number;
- Selection sort has a predictable number of moves (`N`).

At this point, I stopped reading to try and use those hints to come up with the rest of the algorithm on my own. My time spent thinking about the problem thankfully proved to be useful, because I then knew how to combine those hints with tricks I had to come up with when thinking about the problem to produce the final algorithm.

For future personal reference, some ideas that I think are pretty neat and could help me in the future:

- Dividing in `sqrt(N)` tasks of `sqrt(N)` elements is a way to get `O(N)`;
- Keeping a small block of data as an unstructured buffer that we can "slowly" fix at the end is fine (if it's small enough like `sqrt(N)` we can do `O(N^2)` processing on it to stay `O(N)`!);
- Selection sort of `sqrt(N)` blocks does `sqrt(N)` swaps, which can matter for expensive swaps (e.g. blocks of `sqrt(N)` elements!).

## High-Level Algorithm

TODO

## Detailed Algorithm

TODO

## Full Example

TODO

## Merge Sort

TODO