def display(matrix):
    for row in matrix:
        cells = []
        for cell in row:
            cells.append('Q' if cell else '.')
        print(' '.join(cells))


def as_matrix(placement):
    '''
    A placement of N queens is a tuple of length N where the ith element
    indicates where (which column) to place a queen in the ith row.

    >>> as_matrix((0, 3, 1, 2)) == [
    ... [1, 0, 0, 0],
    ... [0, 0, 0, 1],
    ... [0, 1, 0, 0],
    ... [0, 0, 1, 0]]
    True
    '''
    n = len(placement)
    matrix = [[0] * n for _ in range(n)]
    for r, c in enumerate(placement):
        matrix[r][c] = 1
    return matrix


def no_diagonal_attacks(matrix):
    n = len(matrix)
    count_diagonals = 2 * n - 1
    for d in range(count_diagonals):
        if sum(northeast_diagonal(matrix, d)) > 1:
            return False
        if sum(southeast_diagonal(matrix, d)) > 1:
            return False
    return True


def northeast_diagonal(matrix, d):
    for r, c in northeast_diagonal_positions(matrix, d):
        yield matrix[r][c]


def southeast_diagonal(matrix, d):
    for r, c in southeast_diagonal_positions(matrix, d):
        yield matrix[r][c]


def northeast_diagonal_positions(matrix, d):
    '''
    e.g. for a 4x4 matrix, the diagonals are numbered like so:

    0 1 2 3
    1 2 3 4
    2 3 4 5
    3 4 5 6
    '''
    # r + c == d
    n = len(matrix)
    if d < n:
        curr = (d, 0)
        while curr[0] >= 0:
            yield curr
            curr = addvec(curr, (-1, 1))
    else:
        curr = (n - 1, d - (n - 1))
        while curr[1] < n:
            yield curr
            curr = addvec(curr, (-1, 1))


def southeast_diagonal_positions(matrix, d):
    '''
    e.g. for a 4x4 matrix, the diagonals are numbered like so:

    3 4 5 6
    2 3 4 5
    1 2 3 4
    0 1 2 3
    '''
    n = len(matrix)
    for r, c in northeast_diagonal_positions(matrix, d):
        r = n - 1 - r
        yield (r, c)


def addvec(a, b):
    return tuple(x+y for x,y in zip(a,b))
