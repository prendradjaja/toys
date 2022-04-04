from collections import Counter
import itertools
import random

from constants import DIRECTIONS
from rules import *
from gridlib import gridplane as gridlib
from util import chunks


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


def choose_random_move(gamestate):
    return random.choice(get_moves(gamestate))


def choose_leftmost_move(gamestate):
    return min(get_moves(gamestate))


def simple1(gamestate):
    # If a win is available, take it
    for move in get_moves(gamestate):
        after = make_move(gamestate, move)
        if is_win(after):
            return move

    # Otherwise, score each possible move by how many "matching neighbors" it has...
    scores = {}
    for x in get_moves(gamestate):
        y = gamestate.board[x].index(0)

        matches = 0
        for offset in DIRECTIONS:
            neighbor = gridlib.addvec((x, y), offset)
            if in_bounds(neighbor) and gridlib.getindex(gamestate.board, neighbor) == gamestate.turn:
                matches += 1
        scores[x] = matches

    # ...and pick a random move that has max score.
    moves_with_score = [*scores.items()]
    random.shuffle(moves_with_score)  # If this step is omitted, the bot will always pick the leftmost move with max score.
    return max(moves_with_score, key=lambda x: x[1])[0]


def simple2(gamestate):
    '''
    Same as simple1, but notices when it's about to lose.
    '''
    # If a win is available, take it
    for move in get_moves(gamestate):
        after = make_move(gamestate, move)
        if is_win(after):
            return move

    # If opponent is threatening to win in one move, don't play that move
    # (unless losing in one move is forced, in which case play a random move)
    candidates = get_moves(gamestate)
    candidates = [move for move in candidates if not is_losing(make_move(gamestate, move))]
    if not candidates:
        return choose_random_move(gamestate)

    # Otherwise, score each possible move by how many "matching neighbors" it has...
    scores = {}
    for x in candidates:
        y = gamestate.board[x].index(0)

        matches = 0
        for offset in DIRECTIONS:
            neighbor = gridlib.addvec((x, y), offset)
            if in_bounds(neighbor) and gridlib.getindex(gamestate.board, neighbor) == gamestate.turn:
                matches += 1
        scores[x] = matches

    # ...and pick a random move that has max score.
    moves_with_score = [*scores.items()]
    random.shuffle(moves_with_score)  # If this step is omitted, the bot will always pick the leftmost move with max score.
    return max(moves_with_score, key=lambda x: x[1])[0]


def is_losing(gamestate):
    for move in get_moves(gamestate):
        after = make_move(gamestate, move)
        if is_win(after):
            return True
    return False


if __name__ == '__main__':
    main()
