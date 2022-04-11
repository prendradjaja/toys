from collections import namedtuple

from util import *


def demo():
    state = INITIAL_STATE

    show(state)

    move = get_moves(state)[0]
    state = make_move(state, move)

    show(state)

    move = get_moves(state)[0]
    state = make_move(state, move)

    show(state)

    move = get_moves(state)[0]
    state = make_move(state, move)

    show(state)

    move = get_moves(state)[1]
    state = make_move(state, move)

    show(state)


# Types ----------------------------------------------------------------------

GameState = namedtuple('GameState', 'board turn')
GameState.board.__doc__ = '''
- e.g. ('K', 'N', 'R', '.', '.', 'r', 'n', 'k') is the starting position.
- White has capital letters and Black has lowercase, like in FEN.
'''
GameState.turn.__doc__ = '''
Which player is about to move: 'white' or 'black'
'''

Move = namedtuple('Move', 'start end')


# Rules ----------------------------------------------------------------------

INITIAL_STATE = GameState(
    board = ('K', 'N', 'R', '.', '.', 'r', 'n', 'k'),
    turn = 'white',
)


# TODO filter out moves that leave you in check
@listify
def get_moves(gamestate):
    for start, piece in enumerate(gamestate.board):
        if piece == "." or _color(piece) != gamestate.turn:
            continue
        lowerpiece = piece.lower()
        if lowerpiece == "k":
            targets = [start - 1, start + 1]
            targets = [
                end
                for end in targets
                if _in_bounds(end) and not _is_own_piece(end, gamestate)
            ]
            moves = [Move(start, end) for end in targets]
            yield from moves
        elif lowerpiece == "n":
            targets = [start - 2, start + 2]
            targets = [
                end
                for end in targets
                if _in_bounds(end) and not _is_own_piece(end, gamestate)
            ]
            moves = [Move(start, end) for end in targets]
            yield from moves
        elif lowerpiece == "r":
            yield from _get_rook_moves(gamestate, start, gamestate.turn)
        else:
            1 / 0


def make_move(gamestate, move):
    board = list(gamestate.board)
    board[move.end] = board[move.start]
    board[move.start] = '.'
    return GameState(
        board = board,
        turn = _other(gamestate.turn),
    )


# Other useful functions related to this game --------------------------------

def show(gamestate):
    print(' '.join(gamestate.board))


# Private functions ----------------------------------------------------------

def _in_bounds(x):
    return 0 <= x < 8


def _other(player):
    if player == 'white':
        return 'black'
    elif player == 'black':
        return 'white'
    else:
        1/0


def _color(piece):
    if piece == '.':
        1/0
    is_white = piece.upper() == piece
    return 'white' if is_white else 'black'


def _is_own_piece(x, gamestate):
    piece = gamestate.board[x]
    return piece != '.' and _color(piece) == gamestate.turn


def _get_rook_moves(gamestate, start, turn):
    # Rightward moves
    for end in range(start + 1, 8):
        move = Move(start, end)
        piece = gamestate.board[end]
        if piece == '.':
            yield move
        else:
            if _color(piece) != turn:
                yield move
            else:
                pass  # Can't capture own piece
            break

    # Leftward moves
    for end in range(start - 1, 0 - 1, -1):
        move = Move(start, end)
        piece = gamestate.board[end]
        if piece == '.':
            yield move
        else:
            if _color(piece) != turn:
                yield move
            else:
                pass  # Can't capture own piece
            break


if __name__ == '__main__':
    demo()
