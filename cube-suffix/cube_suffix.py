"""Algorithm to find 'x' such that x**3 has the given suffix (as bytes).

E.g. if searching for a 'x**3' with a suffix of '0x15', this would find that 
0x8d**3 = 0x2ac615 (ends in 0x15).

Note that odd suffixes will always have a solution, but even numbers might have
multiple/none.

For odd 'suffix':
    Per Hensel's Lemma, f(x) = 0 (mod p^k) can be lifted to (mod p^(k+1)) if
    f'(x) = 0 (mod p).
    Starting with f(x) = 0 (mod 2):
    f(x) = x^3 - suffix = 0 (mod 2) with suffix = 1 (mod 2) (odd) means that
    x^3 must be odd (= 1 (mod 2)).
    x^3 = 1 (mod 2) gives x = 1 (mod 2) (odd).

    For Hensel's Lemma to apply, we must show that f'(x) != 0 (mod p):
    f'(x) = 3x^2.
    => 3x^2 = 3(1 (mod 2))^2 = 1 != 0 (mod 2)
    So we'll have a unique root solution for f(x) = 0 (mod p^k), for any k > 0.

For even 'suffix':
    Similarly to the odd case, we find that x = 0 (mod 2) for
    x^3 - suffix = 0 (mod 2). Then f'(x) = 3x^2 = 0 (mod 2), so the simple
    version of Hensel's Lemma does not apply. We can still try to lift to higher
    exponents, with two possible cases (for given root 'r' s.t.
    f(r) = 0 (mod p^k)):
     - if f(r) != 0 (mod p^(k+1)), then there is no lifting of r to roots of f
       mod p^(k+1).
     - if f(r) = 0 (mod p^(k+1)), then every lifting of r to mod p^(k+1) is a
       root of f mod p^(k+1).
    So for some even suffixes, we'll find multiple solutions, while for others
    we'll find none. E.g.:
     - suffix=0x12 has no x such that x^3 gives a hex suffix of 0x12.
     - suffix=0x8 has multiple such xs: 
       0x36**3 = 0x26718
       0xb6**3 = 0x5bfd18
       0x76**3 = 0x191218
       0xf6**3 = 0xe32818
"""

import hensel
import polynomial


def cubic_suffix(suffix):
    """Tries to find an 'x' such that x**3 has the provided suffix."""
    # f(x) = x**3 - suffix
    # By finding roots of 'f' mod 2**bitlen(suffix), we are finding values for
    # which x**3 will have the provided suffix, in bits.
    f = polynomial.Polynomial(coefficients=[-suffix, 0, 0, 1])
    k = max(suffix.bit_length(), 1)  # hensel_lift expects k > 0.
    # Note that we round up bitlen to a multiple of 8 bits, since we're working
    # with bytes (e.g. 0x7d ends in same bits as 0x5, but we want the same
    # ending bytes).
    k += -k % 8  # Make k a multiple of 8 bits (byte)
    return hensel.hensel_lift(f, 2, k)


suffix = int(input("Enter the target suffix, as hex: "), 16)
xs = cubic_suffix(suffix)
for x in xs:
    print("Solution: 0x%x**3 = 0x%x" % (x, x**3))
    assert bin(x**3)[2:].endswith(bin(suffix)[2:])
if not xs:
    print("No possible x that gives a x**3 with suffix 0x%x." % suffix)
