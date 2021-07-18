from n_queens_slow import n_queens_slow
from n_queens_backtracking import n_queens_backtracking
import timeit


def main():
    n = 5
    print(timeit.timeit(lambda: print(len(n_queens_backtracking(n))), number=1))
    print(timeit.timeit(lambda: print(len(n_queens_slow(n))), number=1))

    print()

    n = 8
    print(timeit.timeit(lambda: print(len(n_queens_backtracking(n))), number=1))
    print(timeit.timeit(lambda: print(len(n_queens_slow(n))), number=1))

    print()

    n = 9
    print(timeit.timeit(lambda: print(len(n_queens_backtracking(n))), number=1))
    print(timeit.timeit(lambda: print(len(n_queens_slow(n))), number=1))


if __name__ == '__main__':
    main()
