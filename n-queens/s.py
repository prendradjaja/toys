from n_queens_slow import n_queens_slow, display


def main():
    solutions = n_queens_slow(5)
    for each in solutions:
        display(each)
        print()
    print(len(solutions))


if __name__ == '__main__':
    main()
