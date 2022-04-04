from collections import Counter
import itertools
import random
import shutil

from rules import *  # TODO un-star this import?
from strategies import (
    choose_random_move,
    choose_leftmost_move,
    simple1,
    simple2,
    simple3,
    avoid_winning,
)

from util import chunks
from progress import ProgressBar


# Each player's strategy is set here. Try changing one to choose_minimum_move!
# You'll see that that strategy is much more effective than
# choose_random_move.
STRATEGIES = [
    choose_random_move,
    choose_random_move,

    # choose_leftmost_move,
    # simple1,
    # simple2,
    # simple3,
    # avoid_winning,
]

assert len(STRATEGIES) == 2, "STRATEGIES should be 2 items long (P1's strategy, then P2's strategy)"


def main():
    n = 100

    STRATEGIES[:0] = [None]
    print(f'Playing {n} games of Connect Four with these strategies:')
    print('P1:', STRATEGIES[1].__name__)
    print('P2:', STRATEGIES[2].__name__)

    print()
    progress = ProgressBar(n)

    counts = Counter()
    final_positions = []
    for i in range(n):
        gamestate = get_initial_state()
        while not is_game_over(gamestate):
            move = STRATEGIES[gamestate.turn](gamestate)
            gamestate = make_move(gamestate, move)
        result = is_game_over(gamestate)
        counts[result] += 1
        final_positions.append(gamestate)
        progress.show(i)
    progress.done()

    print('\nFinal positions of some sample games:')
    show_multiple(final_positions[:12])

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
    HORIZONTAL_SPACING = 4

    # Calculate max_boards_per_row based on terminal width
    terminal_width = shutil.get_terminal_size(fallback=80).columns
    for n in range(8, 1, -1):
        board_width = COLS * 2 - 1
        total_width = (board_width * n) + (n-1) * HORIZONTAL_SPACING
        if total_width <= terminal_width:
            max_boards_per_row = n
            break
    else:
        max_boards_per_row = 1

    # Show the boards!
    separator = ' ' * HORIZONTAL_SPACING
    for chunk in chunks(gamestates, max_boards_per_row):
        ascii_arts = [to_ascii(gamestate).split('\n') for gamestate in chunk]
        for i in range(len(ascii_arts[0])):
            print(separator.join(art[i] for art in ascii_arts))


if __name__ == '__main__':
    main()
