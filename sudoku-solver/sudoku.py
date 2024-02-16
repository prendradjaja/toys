#!/usr/bin/env python3

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
        slot = slots[len(assignment)]
        r, c = slot
        if not is_invalid_digit(puzzle, r, c, n):
            # Add var=value to assignment
            # (*) Mutating puzzle. If we wanted to stick more closely to the
            # pseudocode, we'd avoid mutating the puzzle and reconstruct it at
            # each step i.e. `puzzle = fill_slots(initial_puzzle,
            # assignment)`, where fill_slots() isn't a function that exists in
            # this file, you'd have to implement that; and initial_puzzle is
            # the puzzle with just the givens)
            fill_slot(puzzle, slots, len(assignment), n)
            assignment.append(n)

            result = recursive_backtracking(assignment, csp)
            if result != recursive_backtracking.FAILURE:
                return result

            # Remove var=value from assignment
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


def is_invalid_digit(sudoku, r, c, digit):
    '''
    Returns True if adding digit to the given position would create an invalid
    solution
    '''

    row = [digit] + [
        sudoku[r][c]
        for c in range(9)
        if sudoku[r][c] != 0
    ]
    if has_duplicate(row):
        return True

    col = [digit] + [
        sudoku[r][c]
        for r in range(9)
        if sudoku[r][c] != 0
    ]
    if has_duplicate(col):
        return True

    R = r - r % 3
    C = c - c % 3
    box = [digit] + [
        sudoku[R + i][C + j]
        for i in range(3)
        for j in range(3)
        if sudoku[R + i][C + j] != 0
    ]
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
