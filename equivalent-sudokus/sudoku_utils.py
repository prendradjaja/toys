ALL_DIGITS_SET = {1, 2, 3, 4, 5, 6, 7, 8, 9}
ALL_DIGITS_STRING = '123456789'


def show(grid):
    for row in grid:
        print(' '.join(str(n) for n in row))
    print()


def parse(digits):
    grid = []
    for r in range(9):
        startindex = r * 9
        row_string = digits[startindex : startindex + 9]
        row = [int(n) for n in row_string]
        grid.append(row)
    return grid


def serialize(grid):
    result = ''
    for row in grid:
        result += ''.join(str(n) for n in row)
    return result


def is_valid(grid):
    for row in grid:
        if set(row) != ALL_DIGITS:
            return False

    for c in range(9):
        col = [grid[r][c] for r in range(9)]
        if set(col) != ALL_DIGITS:
            return False

    # For every box
    for i in range(3):
        for j in range(3):
            box = []
            # For every cell in the box
            for sub_r in range(3):
                for sub_c in range(3):
                    r = i * 3 + sub_r
                    c = j * 3 + sub_c
                    box.append(grid[r][c])
            if set(box) != ALL_DIGITS:
                return False

    return True
