'''
A fully-filled sudoku grid can be transformed into a variety of essentially
equivalent grids.

From Wikipedia:
<https://en.wikipedia.org/w/index.php?title=Mathematics_of_Sudoku&oldid=1095869435>

    Two valid grids are essentially the same if one can be derived from the other, using a so-called validity preserving transformation (VPT). These transformations always transform a valid grid into another valid grid. There are two major types: symbol permutations (relabeling) and cell permutations (rearrangements). They are:

    - Relabeling symbols (9!)
      (Once all possible relabeling combinations are eliminated, except for
      one: for instance, keeping the top row fixed at [123456789], the number
      of fixed grids reduces to 18,383,222,420,692,992. This value is
      6,670,903,752,021,072,936,960 divided by 9!)

    and rearranging (shuffling):

    - Band permutations (3!)
    - Row permutations within a band (3!×3!×3!)
    - Stack permutations (3!)
    - Column permutations within a stack (3!×3!×3!)
    - Reflection, transposition and rotation (2)
      (Given a single transposition or quarter-turn rotation in conjunction
      with the above permutations, any combination of reflections,
      transpositions and rotations can be produced, so these operations only
      contribute a factor of 2)
'''

import itertools
from math import factorial
from random import randrange
import random

from sudoku_utils import parse, is_valid, serialize, ALL_DIGITS_STRING, show


zeros_string = '000000000000000000000000000000000000000000000000000000000000000000000000000000000'


def main():
    example_unsolved = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
    example_solved =   '483921657967345821251876493548132976729564138136798245372689514814253769695417382'

    # Can "scramble" a sudoku into an equivalent one
    shuffled = transform_random(example_solved)
    print(shuffled)
    show(parse(shuffled))

    # Works for solved or unsolved sudokus
    shuffled = transform_random(example_unsolved)
    print(shuffled)
    show(parse(shuffled))


# TODO Maybe use permutation index instead of permutation
def _relabel(digits, permutation):
    '''
    permutation: a digitstring e.g. '987654321'
    '''
    return digits.translate(
        str.maketrans(ALL_DIGITS_STRING, permutation)
    )


def _permute_bands(digits, permutation_index):
    def copy_band(grid1, grid2, b1, b2):
        '''
        Copy band indexed by B1 from GRID1 into GRID2 (at index B2).

        Indices are 0 to 2 (inclusive).
        '''
        for source_row, target_row in zip(
            [b1 * 3 + i for i in range(3)],
            [b2 * 3 + i for i in range(3)]
        ):
            for c in range(9):
                grid2[target_row][c] = grid1[source_row][c]

    assert 0 <= permutation_index < 6  # TODO Move this assertion to nth_permutation
    perm = nth_permutation([0, 1, 2], permutation_index)
    original = parse(digits)
    result = parse(zeros_string)
    for source_band, target_band in zip(range(3), perm):
        copy_band(original, result, source_band, target_band)
    return serialize(result)


def _permute_within_bands(digits, permutation_indices):
    def copy_row(grid1, grid2, source_row, target_row):
        for c in range(9):
            grid2[target_row][c] = grid1[source_row][c]

    original = parse(digits)
    result = parse(zeros_string)

    for band_start, permutation_index in zip([0, 3, 6], permutation_indices):
        source_rows = range(band_start, band_start + 3)
        target_rows = nth_permutation(source_rows, permutation_index)
        for s_row, t_row in zip(source_rows, target_rows):
            copy_row(original, result, s_row, t_row)

    return serialize(result)


def _permute_stacks(digits, permutation_index):
    grid = parse(digits)
    grid = transpose_grid(grid)
    grid = parse(
        _permute_bands(serialize(grid), permutation_index)
    )
    grid = transpose_grid(grid)
    return serialize(grid)


def _permute_within_stacks(digits, permutation_indices):
    grid = parse(digits)
    grid = transpose_grid(grid)
    grid = parse(
        _permute_within_bands(serialize(grid), permutation_indices)
    )
    grid = transpose_grid(grid)
    return serialize(grid)


def _transpose(digits):
    grid = parse(digits)
    grid = transpose_grid(grid)
    return serialize(grid)


def transform(
    digits,  # Should we take a grid or a digitstring?
    *,
    relabel=ALL_DIGITS_STRING,
    permute_bands=0,
    permute_within_bands=(0, 0, 0),
    permute_stacks=0,
    permute_within_stacks=(0, 0, 0),
    transpose=False,
):
    '''
    All optional arguments default to "skip this step".
    '''

    digits = _relabel(digits, relabel)

    digits = _permute_bands(digits, permute_bands)
    digits = _permute_within_bands(digits, permute_within_bands)

    digits = _permute_stacks(digits, permute_stacks)
    digits = _permute_within_stacks(digits, permute_within_stacks)

    if transpose:
        digits = _transpose(digits)

    return digits  # Should we return a grid or a digitstring?


def transform_random(digits):
    return transform(
        digits,
        relabel = ''.join(nth_permutation(ALL_DIGITS_STRING, randrange(factorial(9)))),
        permute_bands=randrange(factorial(3)),
        permute_within_bands=(
            randrange(factorial(3)),
            randrange(factorial(3)),
            randrange(factorial(3)),
        ),
        permute_stacks=randrange(factorial(3)),
        permute_within_stacks=(
            randrange(factorial(3)),
            randrange(factorial(3)),
            randrange(factorial(3)),
        ),
        transpose=random.choice([True, False]),
    )


def nth_permutation(seq, n):
    '''
    n: zero-indexed
    '''
    # There are more performant ways to implement this, but this is perfectly
    # sufficient for this use case.

    # Maybe do a small optimization anyway -- this can be done in "constant
    # space"
    return list(itertools.permutations(seq))[n]


def transpose_grid(m):
    """
    >>> transpose_grid([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]
    """
    return [list(i) for i in zip(*m)]


if __name__ == '__main__':
    main()
