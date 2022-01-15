'''
TODO:
- Fewer multiplications is possible! How? Maybe implement as exp2 below.
  https://projecteuler.net/problem=122
- Use this for AoC 2021.06 "Lanternfish." How fast is it?
  https://adventofcode.com/2021/day/6
'''

def exp1(k, n):  # Exponentiation by squaring
    # k^n can be decomposed into factors of the form k^(2^p).
    #
    # To see this, consider the binary representation of n. For example, if n
    # = 37, then:
    #
    #     k^37 = ?
    #     37 == 0b100101
    #
    #     k^37 = k^32    * k^4     * k^1
    #     k^37 = k^(2^5) * k^(2^5) * k^(2^0)
    #
    # We can generate these factors sequentially by repeatedly squaring k:
    #
    #     p=0: k         = k^1 = k^(2^0)
    #     p=1: k * k     = k^2 = k^(2^1)
    #     p=2: k^2 * k^2 = k^4 = k^(2^2)
    #     p=3: k^4 * k^4 = k^8 = k^(2^3)
    #     ... (as many as needed)

    binary = bin(n)[2:]
    res = 1
    for i, bit in enumerate(reversed(binary)):
        if bit == '1':
            res *= k
        k = k * k
    return res


def exp2(k, n):
    pass


if __name__ == '__main__':
    print('Running tests...')
    for k in range(1, 100):
        for n in range(1, 100):
            expected = k ** n
            actual = exp1(k, n)
            if expected != actual:
                print(f'Failed: {k}**{n} should equal {expected}. Actual: {actual}')
                exit()
    print('Passed.')
