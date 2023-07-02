# Partitions

TODO: summary

## Context

While picking back up [Project Euler](https://projecteuler.net/) problems recently (math challenges to solve programatically), I ran into the problem of counting how many ways there are to write a given number as a sum of prime numbers, and in particular finding the _first_ number where the count of "**prime partitions**" of that number was above some threshold.

I solved the problem through a naive recursion, brute-forcing all possible prime multiples that can fit in the number, without re-using any information about the number of prime partitions that came before. This successfully ran within the time limits of _Project Euler_, but was quite unsatisfactory.

While reading through the problem's solution forums to learn about smarter approaches, I saw mentions of the [Partition function](https://en.wikipedia.org/wiki/Partition_function_(number_theory)) (restricted to prime parts) being represented as a [Generating function](https://en.wikipedia.org/wiki/Generating_function), and using an [Euler transform](https://mathworld.wolfram.com/EulerTransform.html) to compute its terms. This was a lot of theory I knew nothing about, so I wanted to explore this further here to better understand how this works, and how to extend the ideas behind it to other problems.

This README covers the following:
- The partition function $p(n)$;
  - Generating functions and their uses;
  - Creating the partition generating function $p(x)$;
  - Restricted partitions and prime partitions;
  - Euler transform: computing $p(n)$ & algorithmic complexity.
- Listing partitions;
- _Application_: subset sum with repeats;
- Extending to multi-dimensional parts;
- _Application_: Tetris perfect packing.

## Partitions Function $p(n)$

$p(n)$, the [partition function](https://en.wikipedia.org/wiki/Partition_function_(number_theory)), counts how many different ways there are to write the positive integer $n$ as a sum of positive integer parts (ignoring the ordering of the summands).

Here are two examples:
- $2$ has $2$ partitions (i.e. $p(2) = 2$):
  - $2$
  - $1 + 1$
- $4$ has $5$ partitions (i.e. $p(4) = 5$):
  - $4$
  - $3 + 1$
  - $2 + 2$
  - $2 + 1 + 1$
  - $1 + 1 + 1 + 1$

Counting partitions is surprisingly non-trivial, and no closed-form expression for it is known. Here are the values of the first 10 $p(n)$, for example:
- $p(1) = 1$
- $p(2) = 2$
- $p(3) = 3$
- $p(4) = 5$
- $p(5) = 7$
- $p(6) = 11$
- $p(7) = 15$
- $p(8) = 22$
- $p(9) = 30$
- $p(10) = 42$

See [A000041](https://oeis.org/A000041) for more values of it.

For some notation, e.g. for $4 = 3 + 1$:
- The partition $3 + 1$ can be written as a tuple $\lambda = (3, 1)$;
- $3$ and $1$ are _parts_ of a partition;
- $(3,1) \vdash 4$ indicates that $3 + 1$ is a partition of $4$.

Using the above vocabulary, we ultimately want to compute the number of _partitions_ made up of only _prime parts_ for a given number.

### Generating Functions

Here, we take a surprising turn and learn about [Generating functions](https://en.wikipedia.org/wiki/Generating_function). I found this quote useful to accept why we should learn about them at all, given how out-of-the-blue they feel:
> A generating function is a device somewhat similar to a bag. Instead of carrying many little objects detachedly, which could be embarrassing, we put them all in a bag, and then we have only one object to carry, the bag.
>
> — George Pólya, Mathematics and plausible reasoning (1954)

What we eventually want is to study the sequence of values of $p(n)$ (and later partitions constrained to prime parts), to learn how to compute individual values of $p(n)$ more efficiently than the very slow recursive brute-force approach I was using. Generating functions will help us do that.

The sequence of integers of values of $p(n)$ ($1, 2, 3, 5, 7, 11, \cdots$) can be studied on its own, but reformulating it as a generating function gives us familiar tools to algebraically manipulate our sequence and learn about its properties.

Let us first talk about [Formal power series](https://en.wikipedia.org/wiki/Formal_power_series): infinite sums of terms of the form $a x^n$, where $a$ is the coefficient, and $x^n$ is a variable $x$ to the $nth$ power. This can be seen as a generalization of a polynomial. For example, $1 - 3x + 5x^2 - 7x^3 + 9x^4 - 11x^5 + \cdots$ is a formal power series alternating positive and negative odd coefficients, which we could also write as $`\sum_{n=0}^{\infty}(-1)^n (2n+1) x^n`$.

The core idea of generating functions is to **rewrite a sequence of numbers $a_n$ as a formal power series** where our sequence $a_n$ are the coefficients in the series. Note that this is not really a function -- $x$ is [indeterminate](https://en.wikipedia.org/wiki/Indeterminate_(variable)) and we're not interested in its value -- we only want to use it as a placeholder to manipulate the overall expression. It is a bit unorthodox, but remembering the quote above about treating generating functions as a "bag" holding our coefficients can be helpful.
- In the earlier example, if we are interested in the series $a_n = (-1)^n (2n+1)$, we might write it as a generating function as $`\sum_{n=0}^{\infty}a_n x^n`$, giving the formal power series above.
- In terms of notation, if a series is called $A(n)$, it is common to name the generating function where $A(n)$ are the coefficients as $A(x)$ (i.e. $`A(x) = \sum_{n=0}^{\infty}A(n) x^n`$).

Back to our initial goal, we will want to find a way to produce a generating function $p(x)$, where $p(n)$ are the coefficients of the formal power series. It will look like:
- $p(x) = p(0) 1 + p(1) x + p(2)x^2 + p(3)x^3 + p(4)x^4 + p(5)x^5 + p(6)x^6 + \cdots$, or:
- $p(x) = 1 + x + 2x^2 + 3x^3 + 5x^4 + 7x^5 + 11x^6 + \cdots$

#### Example: Dice Sum Generating Function

To get used to the idea of generating function, let's imagine that we have two dice: $d_6$, a 6-sided dice, and $d_4$, a 4-sided dice. Let's define $d(s)$ as the probability of getting a given $d_6 + d_4$ sum $s$. This is an easy example to solve manually, but working through it with generating functions will help us understand how to apply similar ideas to partitions.

We can represent the generating function of the possible sides of $d_6$ as $d_6(x) = (x + x^2 + x^3 + x^4 + x^5 + x^6)$. Each coefficient $1$ of $x^k$ represents the equal odds of rolling side $k$. We similarly define $d_4(x) = (x + x^2 + x^3 + x^4)$.

If we then define $d(x) = d_6(x) d_4(x)$ and expand the result, we get something interesting:
$$d(x) = d_6(x) d_4(x)$$
$$d(x) = (x + x^2 + x^3 + x^4 + x^5 + x^6) (x + x^2 + x^3 + x^4)$$
$$d(x) = (x^2 + x^3 + x^4 + x^5) + (x^3 + x^4 + x^5 + x^6) + (x^4 + x^5 + x^6 + x^7) + (x^5 + x^6 + x^7 + x^8) + (x^6 + x^7 + x^8 + x^9) + (x^7 + x^8 + x^9 + x^{10})$$
$$d(x) = x^2 + 2x^3 + 3x^4 + 4x^5 + 4x^6 + 4x^7 + 3x^8 + 2x^9 + 1x^{10}$$

Notice how the coefficient of each $x^k$ now gives us the number of possible scenarios that give us a dice sum of $k$. In other words, using the notation $`[x^k](d(x))`$ to mean the coefficient of $x^k$ in $d(x)$, we can now define our probability function $`d(s) = \frac{1}{40}[x^s](d(x))`$, i.e. the coefficient of $x^s$ in $d(x)$, divided by the total number of pairs $40$.

The multiplication of the polynomials was used as a tool to count how many pairs sum to a given value. A similar idea will be leveraged and generalized to count partitions.

### Geometric Series
To create this $p(n)$ partition generating function, we'll make use of the [Geometric series](https://en.wikipedia.org/wiki/Geometric_series) $1 + x + x^2 + x^3 + x^4 + \cdots$ (note: we're still using the naming of $x$ here, but this is more commonly written as a ratio $r$).

For convenience, we will sometimes write this series as $\frac{1}{1-x}$. This notation comes from the closed form of the geometric series when the "ratio" $x$ has $|x| < 1$ and with coefficient $a=1$, but we use it here even though $x$ is indeterminate as a convenient way to express $1 + x + x^2 + x^3 + \cdots$.

We can similarly express $1 + x^2 + x^4 + x^6 + \cdots$ as $\frac{1}{1-x^2}$, or more generally for a multiple of exponents $k$:
$$\sum_{n=0}^{\infty}{x^{kn}} = \frac{1}{1-x^k}$$

<details>
<summary>Details about the generalization to 'k'</summary>

We can rewrite $1 + x^k + x^2k + x^3k + x^4k + \cdots$ (for some $k$) as $1 + (x^k) + (x^k)^2 + (x^k)^3 + (x^k)^4 + \cdots$, effectively the geometric series of $x' = x^k$ (reparameterization). This will give us:

$$\sum_{n=0}^{\infty}{(x')^n} = \frac{1}{1-x'}$$
$$\sum_{n=0}^{\infty}{(x^k)^n} = \frac{1}{1-(x^k)}_\square$$

</details>

### Multiplying Geometric Series
If we take two geometric series:
- $1 + x + x^2 + x^3 + x^4 + \cdots$
- $1 + x^2 + x^4 + x^6 + x^8 + \cdots$

and multiply them together, we get something interesting:
$$\frac{1}{1-x} \frac{1}{1-x^2}$$
$$=(1+x+x^2+x^3+x^4+\cdots)(1+x^2+x^4+x^6+x^8+\cdots)$$
$$=(1+x+2x^2+2x^3+3x^4+3x^5+\cdots)$$

What this ends up giving us is a generating function for how many ways there are to write a number $k$ (for a given $x^k$ coefficient) using **only** parts "1" and "2". Here is a breakdown the first few $x^k$ coefficients:
- $x^1$ (for $1$): $(1)$
- $2x^2$ (for $2$): $(2),(1,1)$
- $2x^3$ (for $3$): $(2,1), (1,1,1)$
- $3x^4$ (for $4$): $(2,2), (2,1,1), (1,1,1,1)$
- $3x^5$ (for $5$): $(2,2,1), (2,1,1,1), (1,1,1,1,1)$

To help understand how the multiplication of the series leads to this interpretation, it is useful to rewrite the series more explicitly, and follow how a given term of each series multiplies with the others:
$$\frac{1}{1-x} \frac{1}{1-x^2}$$
$$=(1+x^1+x^{1+1}+x^{1+1+1}+x^{1+1+1+1}+\cdots)(1+x^2+x^{2+2}+x^{2+2+2}+x^{2+2+2+2}+\cdots)$$

Then, if we focus on individual terms and how they will multiply we can get a better understanding. When focusing on a single term (e.g. $x^{1+1}$ on the left side), we can conceptually see this as "selecting" one term from the left series, which will then multiply with each term on the right, and focus on how it contributes to the counts of the final product's coefficients. Some examples:
- "Selecting" $1$ on the left focuses only on the partitions that have _no_ parts of value $1$, in other words this will only contribute to counts of the final product's coefficients for partitions that would only have parts of value $2$ in them (example: $x^2$, $x^4$, ...), if you follow how the multiplication occurs;
- $x^1$ on the left only contributes to counts for partitions that have exactly _one_ part of value $1$ (e.g. $(2,1)$, $(2,2,1)$, ...);
- $x^{1+1}$ on the left represents partitions with exactly $2$ parts of value $1$ (e.g. $(1,1)$, $(2,1,1)$, ...);
- $x^{1+1+1}$ on the left represents partitions with exactly $3$ parts of value $1$ (e.g. $(1,1,1)$, $(2,1,1,1)$, ...);
- $x^{2+2}$ on the _right_ represents partitions with exactly $2$ parts of value $2$ (e.g. $(2,2,1)$, $(2,2)$, ...);
- ...

To gain intuition for this, I highly recommend following the [video series from Michael Penn](https://www.youtube.com/watch?v=z0actv-r7jM) on the topic.

This gives us a useful framing of the different parts of the product:
- $x^{1+1+1+1}$ represents (will only count towards) partitions where there are exactly $4$ parts of value $1$;
- $x^{2+2+2}$ represents partitions where there are exactly $3$ parts of value $2$;
- $\frac{1}{1-x}$ represents parts of value $1$;
- $\frac{1}{1-x^2}$ represents parts of value $2$;
- $\frac{1}{1-x} \frac{1}{1-x^2}$ is the generating function for partitions made up of only parts of value $1$ or $2$ -- let's call this function $\pi_2(x)$, where $\pi_k(n)$ gives the number of partitions of $n$ with parts $<= k$.

### Partitions Generating Function: $p(x)$
Now, we can extend this idea to partitions with larger parts as well. Effectively, we want to generalize our $\pi_k(x)$ function of partitions of parts $<= k$ to arbitrarily large $k$, by multiplying geometric series of successive $x^k$. We finally get:

$$p(x) = \prod_{k=1}^{\infty}{\frac{1}{1-x^k}}$$

This will produce a formal power series where the coefficient for a given $x^n$ is $p(n)$. Again, the above [video series](https://www.youtube.com/watch?v=z0actv-r7jM) is really helpful to understand how we get there.

While reading on this topic, it is helpful to be aware of alternative ways to express the different terms in $p(x)$:
- $p(x)$ can be written in terms of the [Euler function](https://en.wikipedia.org/wiki/Euler_function) $\phi(x) = \prod_{k=1}^{\infty}{(1-x^k)}$, i.e. $\frac{1}{\phi(x)}$;
- a [q-Series](https://mathworld.wolfram.com/q-Series.html) is a series involving coefficients of the form $(a; q)_n = \prod_{k=0}^{n-1}{(1-aq^k)}$;
  - $(a; q)_\infty$ is defined as $(a; q)_\infty = \prod_{k=0}^{\infty}{(1-aq^k)}$ and $(a; q)_\infty$ is called a [q-Pochhammer symbol](https://mathworld.wolfram.com/q-PochhammerSymbol.html);
  - $(a)_n$ is shorthand for $(a; q)_n$ and $(q)_n$ is notation for $(q, q)_n = \prod_{k=1}^\infty{(1-q^k)}$;
  - $(x)_\infty$ is the Euler function $\phi(x)$, so we can also write $p(x) = \frac{1}{(x)_\infty}$.

### Restricted Partitions
TODO partition odd parts
TODO others?
TODO why same logic applies

### Prime Partitions
TODO euler
TODO example
TODO generating function

## Computing $p(n)$
TODO Euler transform
TODO proof?
TODO computation high level
TODO computation pseudocode

### Algorithmic Complexity
TODO

## Computing Prime Partitions
TODO eratosthenes to get prime factors
TODO extend prev algo

## Listing Partitions
TODO

## Subset Sum With Repeats
TODO

## Multi-Dimensional Parts
TODO

## Application: Tetris Packing
TODO
TODO comparison to other approach
