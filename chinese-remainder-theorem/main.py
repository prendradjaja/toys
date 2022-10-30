'''
https://github.com/prendradjaja/toys

Implementation of the Chinese Remainder Theorem / solving a system of
congruences.

Theorem:
  Let m_1, ..., m_n be pairwise coprime. Then the system of n equations
    x = a_1 (mod m_1)
      ...
    x = a_n (mod m_n)
  has a unique solution for x modulo M where M = m1 * ... * m_n.

In fact, there is a formula for that solution:
  x = sum from x=1 to n of (a_i * b_i * b'_i) (mod M)
    where
      b_i = the product of all the moduli except for m_i
      b'_i = the inverse of b_i mod m_i

Proof of CRT: (By proving that this formula is correct. Lynn first proves CRT
  for a system of two equations -- the n-equation case can be proved by
  induction.)
https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html
'''


import math
import itertools


def solve(congruences):
    '''
    Solve a system of congruences.

    Example:
    x = 1 (mod 3)
    x = 1 (mod 4)
    x = 1 (mod 5)
    x = 0 (mod 7)
    Solution is 301 (mod 420)

    >>> solve([
    ...     (1, 3),
    ...     (1, 4),
    ...     (1, 5),
    ...     (0, 7),
    ... ])
    301

    >>> solve([
    ...     (2, 5),
    ...     (3, 7),
    ... ])
    17
    '''
    moduli = [item[1] for item in congruences]
    assert pairwise_coprime(moduli)
    modulus = math.prod(moduli)

    total = 0
    for a, m in congruences:
        other_moduli = list(moduli)
        other_moduli.remove(m)

        b = math.prod(other_moduli)
        b_inv = inverse(b, m)

        total += a * b * b_inv

    return total % modulus


def inverse(a, m):
    '''
    Return the inverse of a mod m.
    '''
    for b in range(m):
        if (a * b) % m == 1:
            return b
    raise Exception('No inverse found')


def pairwise_coprime(lst):
    return all(
        math.gcd(m, n) == 1
        for m, n in itertools.combinations(lst, 2)
    )


if __name__ == '__main__':
    import doctest
    failures, tests = doctest.testmod(verbose=True)
