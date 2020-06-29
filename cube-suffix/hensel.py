"""Usage of Hensel's Lemma to iteratively solve roots for f(x) = 0 (mod p^k)."""

def egcd(a, b):
    """as + bt = gcd(a, b). Returns (gcd(a,b), s, t)"""
    # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    s, old_s = 0, 1
    r, old_r = b, a
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    bezout_t = (old_r - old_s * a) // b if b != 0 else 0
    return old_r, old_s, bezout_t


def modinv(a, n):
    """at = 1 mod n, returns t if gcd(a, n) = 1, otherwise raises ValueError."""
    # ns + at = 1
    # => at = 1 (mod n)
    r, _, t = egcd(n, a)
    if r != 1: raise ValueError("a and n are not coprime (gcd(a, n) != 1).")
    return t


def hensel_lift(f, p, k):
    """Returns a list of roots for f mod p^k, lifting solutions from mod p.

    For k=1, we can find roots by trying all x in range(p) (brute-force).

    For k>1, we use Hensel's Lemma to lift a root of f mod p^k to mod p^(k+1).
    Starting from f(r) = 0 (mod p^k) (root for mod p^k):
    - If f'(r) != 0 (mod p), then the simple form of Hensel's Lemma applies,
      and we can find the unique root mod p^(k+1) by lifting our root r. There
      is a unique t (modulo p) such that f(r + tp^k) = 0 (mod p^(k+1)).
      The new root is (r - f(r) * f'(r)^(-1)) (mod p^(k+1)).
    - If f'(r) = 0 (mod p), then we have two cases:
      - f(r) != 0 (mod p^(k+1)), in which case there is *no* lifting of 'r' to
        a root of f mod p^(k+1).
      - f(r) = 0 (mod p^(k+1)), in which case *every* lifting of 'r' is a root
        of f mod p^(k+1). So r + tp^k for any integer t are all roots.

    It is worth nothing that if we can't find a root mod p^k, we won't find
    roots for higher exponents, i.e. finding a root at an exponent k+1 implies
    that it's a root at exponent k:
    f(x) = 0 (mod p^(k+1))
    => f(x) = p^(k+1) * c  (c integer)
    p^(k+1) * c (mod p^k) = p * p^k * c (mod p^k) = 0 (mod p^k)
    i.e. f(x) = 0 (mod p^(k+1)) => f(x) = 0 (mod p^k).

    Resources:
    - https://math.stackexchange.com/a/90856
    - https://en.wikipedia.org/wiki/Hensel%27s_lemma#Hensel_lifting
    - https://brilliant.org/wiki/hensels-lemma/
    - https://github.com/gmossessian/Hensel
    """
    assert k > 0
    if k == 1:
        # Find the roots (mod p) via bruteforce.
        return [x for x in range(p) if f.eval(x) % p == 0]
    # We'll be lifting solutions starting from f(x) = 0 (mod p^(k-1)).
    roots = hensel_lift(f, p, k - 1)
    new_roots = []
    df = f.derivative()
    for r in roots:
        if df.eval(r) % p != 0:  # f'(r) != 0, can apply Hensel's Lemma.
            # We can lift to the unique solution mod p^k.
            df_r_inv = modinv(df.eval(r), p)
            new_root = (r - f.eval(r) * df_r_inv) % p**k
            assert f.eval(new_root) % p**k == 0
            new_roots.append(new_root)
        elif f.eval(r) % p**k == 0:
            # f'(r) = 0 (mod p), can't apply Hensel's Lemma directly.
            # If f(r) = 0 (mod p^k), however, then every lifting of r to mod p^k
            # is a root of f(x) mod p^k. Note that if it is not, then there is
            # no lifting of r to mod p^k.
            for t in range(p):
                new_root = (r + t * p**(k - 1)) % p**k
                assert f.eval(new_root) % p**k == 0
                new_roots.append(new_root)
    return new_roots
