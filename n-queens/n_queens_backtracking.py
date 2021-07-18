from common import no_diagonal_attacks


def n_queens_backtracking(n):
    matrix = [[0] * n for _ in range(n)]
    solutions = []
    dfs((), matrix, solutions)
    return solutions


def dfs(node, matrix, solutions):
    n = len(matrix)
    if not no_diagonal_attacks(matrix):
        return
    elif len(node) == n:
        solutions.append(node)
    else:
        for child in children(node, n):
            add_assignment(child, matrix)
            dfs(child, matrix, solutions)
            remove_assignment(child, matrix)


def children(node, n):
    choices = set(range(n))
    choices -= set(node)
    for choice in choices:
        yield node + (choice,)


def add_assignment(child, matrix):
    r = len(child) - 1
    c = child[r]
    assert matrix[r][c] == 0
    matrix[r][c] = 1


def remove_assignment(child, matrix):
    r = len(child) - 1
    c = child[r]
    assert matrix[r][c] == 1
    matrix[r][c] = 0
