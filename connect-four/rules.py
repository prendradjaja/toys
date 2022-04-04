from collections import namedtuple

from constants import COLS, ROWS
from termcolor import colored
from util import consecutives, listify, transpose


GameState = namedtuple('GameState', 'turn board')
GameState.turn.__doc__ = '''- Type: 1 | 2
- Which player (1 or 2) is about to move.'''
GameState.board.__doc__ = '''- Type: (0 | 1 | 2)[][]
- Indexed board[x][y], where y=0 is the bottom of the board.
- board[x][y] == 0 if that space is empty
              == 1 represents a player 1 chip
              == 2 represents a player 2 chip'''


def get_initial_state():
    return GameState(
        turn = 1,
        board = tuple((0,) * ROWS for _ in range(COLS))
    )


GameOver = namedtuple('GameOver', 'type winner')
def is_game_over(gamestate, *, run_length=4, _check_players=frozenset([1, 2])):
    '''
    Return falsy if not game over.

    Return truthy if game over. One of:
        GameOver('win', 1)
        GameOver('win', 2)
        GameOver('draw', None)
    '''
    def has_vertical_win(board):
        for col in board:
            for each in consecutives(col, run_length):
                if each == P1_RUN and 1 in _check_players:
                    return GameOver('win', 1)
                if each == P2_RUN and 2 in _check_players:
                    return GameOver('win', 2)
        return False

    P1_RUN = (1,) * run_length
    P2_RUN = (2,) * run_length

    # Check for vertical wins
    if result := has_vertical_win(gamestate.board):
        return result

    # Check for horizontal wins
    if result := has_vertical_win(transpose(gamestate.board)):
        return result

    # Check for diagonal wins in one direction
    board = _to_mutable(gamestate.board)
    _stagger_up(board)
    if result := has_vertical_win(transpose(board)):
        return result

    # Check for diagonal wins in the other direction
    board = _to_mutable(gamestate.board)
    _stagger_down(board)
    if result := has_vertical_win(transpose(board)):
        return result

    # Check if the board is full
    if len(get_moves(gamestate)) == 0:
        return GameOver('draw', None)

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


# Not really rules, but other Connect 4 utils --------------------------------


def is_win(gamestate):
    '''
    Return True if win for the last player to move
    '''
    last_player = _other(gamestate.turn)
    gameover = is_game_over(gamestate)
    return bool(gameover and gameover.type == 'win' and gameover.winner == last_player)


def show(gamestate):
    print(to_ascii(gamestate), end='')


def to_ascii(gamestate):
    board = gamestate.board
    def chipstr(chip):
        if chip == 0:
            return '.'
        elif chip == 1:
            # return '1'
            return colored('1', color='red')
        elif chip == 2:
            # return '2'
            return colored('2', color='yellow')
        else:
            1/0

    result = ''
    for row in reversed(transpose(board)):
        result += ' '.join(chipstr(x) for x in row) + '\n'
    result += '\n'

    return result


def in_bounds(pos):
    x, y = pos
    return 0 <= x < COLS and 0 <= y < ROWS


def get_longest_run(gamestate, player):
    if has_run(gamestate, 4, player):
        return 4
    elif has_run(gamestate, 3, player):
        return 3
    elif has_run(gamestate, 2, player):
        return 2
    else:
        return 1


def has_run(gamestate, run_length, player):
    gameover = is_game_over(
        gamestate,
        run_length= run_length,
        _check_players = {player},
    )
    return gameover and gameover.type == 'win'


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
