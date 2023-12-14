#!/usr/bin/env python3
'''
Similar to sudoku.py (compare with diff), but checks the whole puzzle at each
step instead of just checking the last-assigned digit -- slower. Usually just
use sudoku.py.
'''

import copy


def main():
    puzzles = parse_file(open('sudoku.txt').read())

    answer = 0
    for i, each in enumerate(puzzles, start=1):
        solution = solve(each)
        a, b, c = solution[0][:3]
        n = int(f'{a}{b}{c}')
        print(i, n)
        answer += n
    print(answer)


def solve(puzzle):
    puzzle = copy.deepcopy(puzzle)
    puzzle_with_extras = (puzzle, find_slots(puzzle))
    backtracking_search(puzzle_with_extras)
    return puzzle


def backtracking_search(csp):
    return recursive_backtracking([], csp)


def recursive_backtracking(assignment, csp):
    # Differences vs pseudocode are marked with (*)

    puzzle, slots = csp
    if len(assignment) == len(slots):
        return assignment

    # (*) The next unassigned variable is always the next spot in the sudoku;
    # there doesn't need to be a line of code for it right here (though it is
    # handled by fill_slot())

    for n in range(1, 9 + 1):
        # (*) Mutate the puzzle not just the assignment
        fill_slot(puzzle, slots, len(assignment), n)
        if is_invalid(puzzle):
            # (*) This `if is_invalid` portion is necessary because we're
            # mutating the puzzle not just the assignment
            fill_slot(puzzle, slots, len(assignment), 0)
        else:
            # Add var=value to assignment
            assignment.append(n)

            result = recursive_backtracking(assignment, csp)

            if result != recursive_backtracking.FAILURE:
                return result

            # Remove var=value from assignment
            # (*) And unmutate the puzzle
            assignment.pop()
            fill_slot(puzzle, slots, len(assignment), 0)

    return recursive_backtracking.FAILURE

recursive_backtracking.FAILURE = 'FAILURE'


def fill_slot(puzzle, slots, idx, value):
    r, c = slots[idx]
    puzzle[r][c] = value


def find_slots(puzzle):
    return tuple(
        (r, c)
        for r in range(9)
        for c in range(9)
        if puzzle[r][c] == 0
    )


def is_invalid(partial_sudoku):
    '''
    Returns True if the partial sudoku is invalid.

    Returns False if the partial sudoku is OK. This does not mean the sudoku
    is necessarily solved. A sudoku is solved if and only if
    (is_invalid(sudoku) == False and is_filled(sudoku) == True)
    '''
    rows = (
        (
            partial_sudoku[r][c]
            for c in range(9)
            if partial_sudoku[r][c] != 0
        )
        for r in range(9)
    )
    if any(has_duplicate(row) for row in rows):
        return True

    columns = (
        (
            partial_sudoku[r][c]
            for r in range(9)
            if partial_sudoku[r][c] != 0
        )
        for c in range(9)
    )
    if any(has_duplicate(col) for col in columns):
        return True

    for R in range(0, 9, 3):
        for C in range(0, 9, 3):
            box = (
                partial_sudoku[R + r][C + c]
                for r in range(3)
                for c in range(3)
                if partial_sudoku[R + r][C + c] != 0
            )
            if has_duplicate(box):
                return True
    return False


def has_duplicate(seq):
    lst = list(seq)
    return len(set(lst)) < len(lst)


def parse_file(text):
    lines = iter(text.splitlines())
    puzzles = []
    for _ in range(50):
        discard = next(lines)
        assert discard.startswith('Grid ')
        puzzle = []
        for _ in range(9):
            puzzle.append([
                int(n) for n in next(lines)
            ])
        puzzles.append(puzzle)

    empty = False
    try:
        next(lines)
    except StopIteration:
        empty = True
    assert empty

    return puzzles


if __name__ == '__main__':
    main()
