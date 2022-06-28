'''
A fully-filled sudoku grid can be transformed into a variety of essentially
equivalent grids.

From Wikipedia:
<https://en.wikipedia.org/wiki/Mathematics_of_Sudoku#Validity_preserving_transformations>

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

from sudoku_utils import parse, is_valid, serialize, ALL_DIGITS_STRING, show


zeros_string = '000000000000000000000000000000000000000000000000000000000000000000000000000000000'


def main():
    # An arbitrary example sudoku
    digits = '124567893378294516659831742987123465231456978546789321863972154495618237712345689'

    show(parse(digits))
    show(parse(transform(digits, relabel='123456798', permute_bands=1)))


# TODO Use permutation index instead of permutation. Requires find_nth_permutation
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

    assert 0 <= permutation_index < 6
    perm = nth_permutation([0, 1, 2], permutation_index)
    original = parse(digits)
    result = parse(zeros_string)
    for source_band, target_band in zip(range(3), perm):
        copy_band(original, result, source_band, target_band)
    return serialize(result)


# TODO Add support for the rest of the transformations
# TODO Allow use of "transformation index" that combines all these args into
# one integer?
def transform(
    digits,  # Should we take a grid or a digitstring?
    *,
    relabel=ALL_DIGITS_STRING,
    permute_bands=0,
):
    '''
    All optional arguments default to "skip this step".
    '''
    digits = _relabel(digits, relabel)
    digits = _permute_bands(digits, permute_bands)
    return digits  # Should we return a grid or a digitstring?


def nth_permutation(seq, n):
    '''
    n: zero-indexed
    '''
    # There are more performant ways to implement this, but this is perfectly
    # sufficient for this use case.

    # Maybe do a small optimization anyway -- this can be done in "constant
    # space"
    return list(itertools.permutations(seq))[n]


if __name__ == '__main__':
    main()
