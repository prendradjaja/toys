'''
From Puzzles 4 Pleasure by Barry R. Clarke:

Psychic Sally claims to be able to 'sense' the nine different colors on a
3-by-3 grid of squares that a volunteer secretly fills in. Her assistant,
Doubtful Doreen, who looks at the positions of the nine colours, makes five
statements about their relative positions to Sally. What no-one in the
audience realises is that it is possible to deduce the positions from the
statements Doreen makes. On one occasion, the statements were as follows. (1)
A red is directly above a blue. (2) A yellow is two to the right of a green.
(3) An orange is two above a pink. (4) A turquoise is directly below a violet.
(5) A white is directly to the right of a blue. How were the colours arranged
in the grid?
'''

import itertools


def main():
    solutions = []
    for p in itertools.permutations('roygbvptw'):
        p = ''.join(p)
        if correct(p):
            solutions.append(p)

    assert len(solutions) == 1

    solution = solutions[0]

    print(solution[0:3])
    print(solution[3:6])
    print(solution[6:9])


def correct(permutation):
    p = permutation

    index = lambda c: p.index(c)
    row = lambda c: p.index(c) // 3
    col = lambda c: p.index(c) % 3

    return (
        # (1) A red is directly above a blue.
        (index('b') - index('r') == 3)

        # (2) A yellow is two to the right of a green.
        and (
            row('y') == row('g')
            and col('y') == 2
            and col('g') == 0
        )

        # (3) An orange is two above a pink.
        and (
            col('o') == col('p')
            and row('o') == 0
            and row('p') == 2
        )

        # (4) A turquoise is directly below a violet.
        and (index('t') - index('v') == 3)

        # (5) A white is directly to the right of a blue. How were the colours arranged in the grid?
        and (
            index('w') - index('b') == 1
            and col('w') != 0
        )
    )


if __name__ == '__main__':
    main()
