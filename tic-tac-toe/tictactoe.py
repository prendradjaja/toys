from collections import namedtuple, Counter
import itertools
import random
import math

from util import flatten, listify, enumerate2d


def demo():
    simulate()
    # negamax_demo()


def simulate():
    n = 1000
    print(f'Simulating {n} random games of tic-tac-toe. Results:')

    results = Counter()
    for _ in range(n):
        state = INITIAL_STATE
        while not is_game_over(state):
            move = random.choice(get_moves(state))
            state = make_move(state, move)
        if winner := is_win(state):
            results[winner] += 1
        else:
            results['D'] += 1

    # For 1000 games, expect approximately: X 580 / O 290 / D 130
    # https://www.reddit.com/r/theydidthemath/comments/7o54fh/request_if_two_people_play_tic_tac_toe_choosing/
    print('X win:', results['X'])
    print('O win:', results['O'])
    print('Draw: ', results['D'])


def negamax(gamestate):
    # This probably has a bug in it! See negamax_demo(). Or the bug could be
    # in my implementation of the rules of the game! I'm guessing it's here,
    # but I haven't tested the rules particularly thoroughly, so it could be
    # anywhere, really...
    if is_game_over(gamestate):
        if is_win(gamestate):
            return -math.inf
        else:
            return 0
    max_value = -math.inf
    for move in get_moves(gamestate):
        score = -negamax(make_move(gamestate, move))
        if score > max_value:
            max_value = score
    return score


def negamax_demo():
    # Looks like I've got the signs right...
    print(negamax(GameState(
        board = (
            ('X', '.', '.'),
            ('X', 'X', '.'),
            ('.', '.', '.'),
        ),
        turn = 'O',
    )) == -math.inf)
    print(negamax(GameState(
        board = (
            ('.', '.', '.'),
            ('O', 'O', '.'),
            ('.', '.', '.'),
        ),
        turn = 'O',
    )) == math.inf)

    # ...but this (which takes about 5 sec) says the game is a forced win for
    # the first player, so there's a bug somewhere.
    print(negamax(INITIAL_STATE))


# Types ----------------------------------------------------------------------

GameState = namedtuple('GameState', 'board turn')


# Rules ----------------------------------------------------------------------

INITIAL_STATE = GameState(
    board = (('.', '.', '.'), ('.', '.', '.'), ('.', '.', '.')),
    turn = 'X',
)


def is_game_over(gamestate):
    board = flatten(gamestate.board)
    if '.' not in board:
        return True
    else:
        return bool(is_win(gamestate))


def is_win(gamestate):
    '''
    Return truthy (actually, the id 'X' or 'O' of the winning player) if the
    game is a win for the player who last moved
    '''
    board = flatten(gamestate.board)
    last_mover = _other(gamestate.turn)
    is_my_chip = [chip == last_mover for chip in board]
    magic = [  # https://en.wikipedia.org/wiki/Number_Scrabble
        2, 7, 6,
        9, 5, 1,
        4, 3, 8
    ]
    my_numbers = [n for include, n in zip(is_my_chip, magic) if include]
    for triple in itertools.combinations(my_numbers, 3):
        if sum(triple) == 15:
            return last_mover
    return None


@listify
def get_moves(gamestate):
    assert not is_game_over(gamestate)
    for pos, chip in enumerate2d(gamestate.board):
        if chip == '.':
            yield pos


def make_move(gamestate, move):
    new_board = []
    for r, old_row in enumerate(gamestate.board):
        new_row = []
        for c, old_chip in enumerate(old_row):
            if move == (r, c):
                new_chip = gamestate.turn
            else:
                new_chip = old_chip
            new_row.append(new_chip)
        new_board.append(tuple(new_row))
    return GameState(
        board = tuple(new_board),
        turn = _other(gamestate.turn),
    )


# Other useful functions related to this game --------------------------------

def show(gamestate):
    for row in gamestate.board:
        print(' '.join(row))


# Private functions ----------------------------------------------------------

def _other(player):
    assert player in 'XO'
    return next(iter({'X', 'O'} - {player}))


if __name__ == '__main__':
    demo()
