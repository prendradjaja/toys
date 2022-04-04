from collections import Counter
import itertools
import random

from rules import *  # TODO un-star this import?
from strategies import (
    choose_random_move,
    choose_leftmost_move,
    simple1,
    simple2,
)

from util import chunks


# Each player's strategy is set here. Try changing one to choose_minimum_move!
# You'll see that that strategy is much more effective than
# choose_random_move.
strategies = [
    choose_random_move,
    choose_random_move,

    # choose_leftmost_move,
    # simple1,
    # simple2,
    # simple3,
]

assert len(strategies) == 2, "`strategies` should be 2 items long (P1's strategy, then P2's strategy)"


def main():
    n = 500

    strategies[:0] = [None]
    print(f'Playing {n} games of Connect Four with these strategies:')
    print('P1:', strategies[1].__name__)
    print('P2:', strategies[2].__name__)

    counts = Counter()
    final_positions = []
    for _ in range(n):
        gamestate = get_initial_state()
        while not is_game_over(gamestate):
            move = strategies[gamestate.turn](gamestate)
            gamestate = make_move(gamestate, move)
        result = is_game_over(gamestate)
        counts[result] += 1
        final_positions.append(gamestate)

    print('\nFinal positions of some sample games:')
    show_multiple(final_positions[:10])

    print('Results:')
    result_names = {
        ('win', 1): 'P1 win',
        ('win', 2): 'P2 win',
        ('draw', None): 'Draw',
    }
    for result, name in result_names.items():
        percent = counts[result] / n
        print(f'{name}\t{percent:>6.1%}')  # https://docs.python.org/3/library/string.html#format-specification-mini-language


def show_multiple(gamestates):
    MAX_BOARDS_PER_ROW = 5
    HORIZONTAL_SPACING = 4

    separator = ' ' * HORIZONTAL_SPACING

    for chunk in chunks(gamestates, MAX_BOARDS_PER_ROW):
        ascii_arts = [to_ascii(gamestate).split('\n') for gamestate in chunk]
        for i in range(len(ascii_arts[0])):
            print(separator.join(art[i] for art in ascii_arts))
        # print()


if __name__ == '__main__':
    main()
