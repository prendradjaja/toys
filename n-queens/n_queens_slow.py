import itertools
from common import no_diagonal_attacks, as_matrix


def n_queens_slow(n):
    solutions = []
    for placement in itertools.permutations(range(n)):
        matrix = as_matrix(placement)
        if no_diagonal_attacks(matrix):
            solutions.append(matrix)
    return solutions
