import random
from collections import Counter

from rules import *


def main():
    n = 500

    # Each player (1 and 2)'s strategy is set here. Try changing one to
    # choose_minimum_move! You'll see that that strategy is much more
    # effective than choose_random_move.
    strategies = {
        1: choose_random_move,
        2: choose_random_move,
    }

    print(f'Playing {n} games of Connect Four with these strategies:')
    print('P1:', strategies[1].__name__)
    print('P2:', strategies[2].__name__)

    counts = Counter()
    for _ in range(n):
        gamestate = get_initial_state()
        while not is_game_over(gamestate):
            move = strategies[gamestate.turn](gamestate)
            gamestate = make_move(gamestate, move)
        result = is_game_over(gamestate)
        counts[result] += 1

    print('\nFinal position of the last game:')
    show(gamestate)

    print('Results:')
    result_names = {
        ('win', 1): 'P1 win',
        ('win', 2): 'P2 win',
        ('draw', None): 'Draw',
    }
    for result, name in result_names.items():
        percent = counts[result] / n
        print(f'{name}\t{percent:>6.1%}')  # https://docs.python.org/3/library/string.html#format-specification-mini-language


def choose_random_move(gamestate):
    return random.choice(get_moves(gamestate))


def choose_minimum_move(gamestate):
    return min(get_moves(gamestate))


if __name__ == '__main__':
    main()
