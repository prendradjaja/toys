from collections import namedtuple

from constants import COLS, ROWS
from termcolor import colored
from util import consecutives, listify, transpose


GameState = namedtuple('GameState', 'turn board')
GameState.turn.__doc__ = '''Type: 1 | 2
Which player (1 or 2) is about to move.'''
GameState.board.__doc__ = '''Type: (0 | 1 | 2)[][]
Indexed board[col][row], where row=0 is the bottom. 0 represents an empty
space.'''


def get_initial_state():
    return GameState(
        turn = 1,
        board = tuple((0,) * ROWS for _ in range(COLS))
    )


def is_game_over(gamestate):
    '''
    Return falsy if not game over.

    Return truthy if game over. One of:
        ('win', 1)
        ('win', 2)
        ('draw', None)
    '''
    ONES = (1, 1, 1, 1)
    TWOS = (2, 2, 2, 2)

    # Check for vertical wins
    for col in gamestate.board:
        for each in consecutives(col, 4):
            if each == ONES:
                return ('win', 1)
            if each == TWOS:
                return ('win', 2)

    # Check for horizontal wins
    for col in transpose(gamestate.board):
        for each in consecutives(col, 4):
            if each == ONES:
                return ('win', 1)
            if each == TWOS:
                return ('win', 2)

    # Check for diagonal wins in one direction
    board = _to_mutable(gamestate.board)
    _stagger_up(board)
    for col in transpose(board):
        for each in consecutives(col, 4):
            if each == ONES:
                return ('win', 1)
            if each == TWOS:
                return ('win', 2)

    # Check for diagonal wins in the other direction
    board = _to_mutable(gamestate.board)
    _stagger_down(board)
    for col in transpose(board):
        for each in consecutives(col, 4):
            if each == ONES:
                return ('win', 1)
            if each == TWOS:
                return ('win', 2)

    if len(get_moves(gamestate)) == 0:
        return ('draw', None)

    return False


def make_move(gamestate, x):
    turn = gamestate.turn
    board = gamestate.board
    try:
        # Find first free slot
        y = board[x].index(0)
    except ValueError:
        raise Exception('Invalid move (column is full)')

    return GameState(
        turn = _other(turn),
        board = _setindex(board, (x, y), turn)
    )


@listify
def get_moves(gamestate):
    for y, col in enumerate(gamestate.board):
        if 0 in col:
            yield y


def show(gamestate):
    board = gamestate.board
    def chipstr(chip):
        if chip == 0:
            return '.'
        elif chip == 1:
            return colored('1', color='red')
        elif chip == 2:
            return colored('2', color='yellow')
        else:
            1/0

    for row in reversed(transpose(board)):
        print(' '.join(chipstr(x) for x in row))
    print()


# Private functions ----------------------------------------------------------


def _other(player):
    if player == 1:
        return 2
    elif player == 2:
        return 1
    else:
        1/0


def _setindex(board, index, new_value):
    '''
    Given a (2d) index into a 2d tuple and a value to be set, return a new 2d
    tuple (with that value set).

    >>> g = ((1, 2), (3, 4), (5, 6))
    >>> _setindex(g, (0, 0), 99)
    ((99, 2), (3, 4), (5, 6))
    >>> _setindex(g, (2, 1), 99)
    ((1, 2), (3, 4), (5, 99))
    '''
    result = []
    for r, row in enumerate(board):
        new_row = []
        for c, old_value in enumerate(row):
            if index == (r, c):
                new_row.append(new_value)
            else:
                new_row.append(old_value)
        result.append(tuple(new_row))
    return tuple(result)


def _to_mutable(board):
    '''
    Turns a 2d tuple into a 2d list so that it can be mutated.
    '''
    # TODO Use a faster implementation :)
    return transpose(transpose(board))


def _stagger_up(mutable_board):
    for i, col in enumerate(mutable_board):
        bottom_padding = [0] * i
        top_padding = [0] * (len(mutable_board) - i)
        col[:0] = bottom_padding
        col.extend(top_padding)


def _stagger_down(mutable_board):
    for i, col in enumerate(mutable_board):
        bottom_padding = [0] * (len(mutable_board) - i)
        top_padding = [0] * i
        col[:0] = bottom_padding
        col.extend(top_padding)
