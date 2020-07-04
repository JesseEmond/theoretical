# Perfect Cube Suffix

Algorithm to find an `x` such that `x^3` has the given suffix, in bits. In other
words, finding a perfect cube with a given bits suffix.

## Context
While working on a
[Cryptopals challenge](https://cryptopals.com/sets/6/challenges/42)
, I was learning about forging `e=3` RSA signatures that fool
implementations that check the decrypted padding in a fuzzy way (bypassing the
need to solve `sig^3 (mod N)` without knowing the private `d` RSA exponent, by
instead giving a `sig` that gives a final `sig^3` result that has the bits we want +
some garbage for bits that are not checked by vulnerable implementations).

The attack in this Cryptopals challenge is the
[Bleichenbacher'06](https://mailarchive.ietf.org/arch/msg/openpgp/5rnE9ZRN1AokBVj3VqblGlP63QE/)
attack, where we are only concerned about forging a signature that gives a
target prefix. This breaks implementations that do not verify that the provided
signed hash is right-justified, meaning that as long as our prefix makes sense,
the suffix is ignored (i.e. find `x` such that `x^3` has a given prefix). We can
thus easily find a forged signature by using an integer cube root. See my
[solutions repository](https://github.com/JesseEmond/matasano-cryptopals) for
more details.

An interesting follow-up to this attack is to target implementations that _do_
check that the hash is right-justified, but not the bits in the middle. In other
words, we must now forge a signature that produces a given suffix (i.e. find `x`
such that `x^3` has a given suffix). We can easily merge the `x` that gives our
target suffix with one that gives a target prefix (found with previous method).

[Filippo Valsorda](https://twitter.com/FiloSottile) has a
[blog post](https://blog.filippo.io/bleichenbacher-06-signature-forgery-in-python-rsa/)
about using this attack to break `python-rsa`, using similar tricks to what was
used in [BERserk](https://github.com/FiloSottile/BERserk#the-attack). The blog
post describes a simple iterative algorithm to find a cube with a target suffix,
based on the intuition that flipping the Nth bit (from the right) in `x` causes
the Nth bit in `x^3` to flip, leaving the bits 0 to N-1 unaffected. We can then
start from bit 0 and iteratively flip bits (as needed) of `x` to find our target
suffix. Lower in the post, however, there is a check that **suffix is odd** to
use that algorithm.

This made me wonder:

 1. **Why must suffix be odd for this algorithm to work?**
 2. **Does this algorithm work for all odd suffixes?**
 3. **What can we do about even suffixes?**

## Problem Statement
We are ultimately interested in finding `x` such that `x^3` ends in a given
`suffix`. In other words, we want to solve:

```
x^3 = suffix (mod 2^bitlen(suffix))
```

Where `bitlen(suffix)` is `ceil(log2(suffix))`.

We will analyze an equivalent problem, finding roots for `f(x) = x^3 - suffix`,
in `mod 2^bitlen(suffix)`, or more generally in `mod p^k` for prime `p`:

```
f(x) = x^3 - suffix = 0 (mod p^k)
```

Roots of `f(x) mod p^k` with `p=2` and `k=bitlen(suffix)` will be values that
give us our target suffix when cubed. Code to handle polynomials is in
[polynomial.py](./polynomial.py).

## Hensel's Lemma
[Hensel's Lemma](https://en.wikipedia.org/wiki/Hensel%27s_lemma) tells us that
(less general form of the lemma):

```
If r is an integer such that:
    f(r) = 0    (mod p^k)
    and
    f'(r) != 0  (mod p)

Then there exists a unique 's' (mod p^(k+1)) such that:
    f(s) = 0    (mod p^(k+1))
    and
    r = s       (mod p^k)

In particular, 's' can be computed explicitly:
    s = r - f(r) * (f'(r) mod p)
```

Essentially, when `f'(r) != 0 (mod p)`, we can **"lift"** a solution for
`f(r) = 0 (mod p^k)` to `f mod (p^(k+1))`.

## Odd Suffixes
If we go back to the condition that suffixes are odd in Filippo's algorithm, we
can see how it is essentially an iterative application of Hensel's Lemma with
`f'(x) != 0 (mod p)`.

For odd suffixes, we have `suffix = 1 (mod 2)`. `suffix = x^3 = 1 (mod 2)` gives
us that `x = 1 (mod 2)` (in other words `x` must be odd).

We can show that `f'(x) != 0 (mod 2)` for odd `x` (all in `mod 2`):
```
f'(x) = 3x^2
=> 3x^2 = 3(1 (mod 2))^2 = 1 != 0 (mod 2)
```

So Hensel's Lemma applies, meaning that we are guaranteed to be able to lift a
solution to `x^3 = suffix (mod 2^k)` uniquely to `(mod 2^(k+1))`.

We start with `x = 1 (mod 2)`, our base case. We know that our solution `r` in
`(mod 2^k)` will be `s = r (mod 2^k)` in `(mod 2^(k+1))`. In other words,
`s = r + t*2^k` (integer `t`). Because we're dealing with `p=2`, that gives us
only two possible values for `s` in `(mod 2^(k+1))`: `r`, or `r + 2^k`.
Note that adding `2^k` in `(mod 2^(k+1))` is equivalent to XORing (flipping) the
kth bit.

With that perspective, we see how Filippo's algorithm is equivalent to
leveraging Hensel's Lemma to find the solution for the next bit, but instead of
using the exact formula to compute the leveraged `s`, we just try both possible
values (`r` and `r + 2^N (mod 2^(N+1))`).

With this theoretical equivalence, however, we now have guidance to apply this
for (some) even suffixes as well.

## Even Suffixes: f'(x) = 0 (mod p)
Now, `f'(x) = 0 (mod p)` does not necessarily imply that there are no roots.
For example, with `2^3 = 8 (mod 2^4)`, we see that we can find a solution for a
target suffix of `8`.

With `f'(x) = 0 (mod p)`, we can show
[through the Taylor expansion of f](https://math.stackexchange.com/a/90856) that
`f(x + tp^k) = f(x) (mod p^(k+1))` for all integers `t`:
```
Taylor expansion of f(a + h):
f(a + h) = f(a) + f'(a)h + 1/2 f''(a)h^2 + ... + 1/(n!) f^(n)(a)h^n

For f(x + tp^k):
f(x + tp^k) = f(x) + f'(x)tp^k + ... + f^(n)(x)t^np^(kn)/n!

Since f'(x) = 0 (mod p):
f(x + tp^k) = f(x) (mod p^(k+1))
```

This means that either a root `r` for `f (mod p^k)` can be lifted to
`(mod p^(k+1))` for _all_ `r + tp^k (mod p^(k+1))`, or for none of them.


## Algorithm: Hensel Lifting 

We can put these cases together into a recursive function that tries to lift
from roots with the previous exponent. The code for this lies under
[hensel.py](./hensel.py), note that it is based on an
[existing implementation](https://github.com/gmossessian/Hensel), reimplemented
here for my own understanding.

The final algorithm:
```
hensel_lift(f, p, k):
  if k = 1: return [x for x in range(p) if f(x) = 0 (mod p)]

  prev_roots := hensel_lift(f, p, k-1)
  new_roots  := []
  for r in prev_roots:
    if f'(r) != 0 (mod p):                     # Hensel's Lemma (simple root)
      s := (r - f(r) * f'(r)^(-1))) (mod p^k)  # Note f'(r)^(-1) is in (mod p)
      new_roots.append(s)
    elif f(r) = 0 (mod p^k):                   # If r+tp^(k-1) are all solutions
      for t in range(p):
        s := (r + tp^(k-1)) (mod p^k)
        new_roots.append(s)
  return new_roots
```

## Conclusion
With this, we now have a general algorithm to solve `f(x) = 0 (mod p^k)`, which
we use to solve `x^3 = suffix (mod 2^bitlen(suffix))`. We know that this will
always find a unique solution `(mod 2^bitlen(suffix))` when `suffix` is odd, and
sometimes find solutions when `suffix` is even.

This does mean, however, that there are suffixes that we can never find an `x`
for. In the context of our attack, that means that we are unable to forge a
signature that will produce our target suffix. Our suffix in this case is the
ending of an ASN-1 hash, or the hash of the message we want to sign:
`suffix = asn-1-blob(hash) + hash(msg)`. For example, we could not produce a
forged signature that ends in `02` (without wrapping around RSA's `N`, that is).

This is unfortunate, but in most realistic scenarios it is possible to slightly
alter `msg` until it gives us a hash suffix for which we can forge a signature.
This is why Filippo's much simpler algorithm is likely all we need, because in
practical scenarios we probably have a way to alter `msg` within our attack
context to change the hash, until we get a odd hash.

## Resources
Useful links to get a better understanding of Hensel's Lemma:

- https://math.stackexchange.com/a/90856
- https://en.wikipedia.org/wiki/Hensel%27s_lemma#Hensel_lifting
- https://brilliant.org/wiki/hensels-lemma/
- https://github.com/gmossessian/Hensel
