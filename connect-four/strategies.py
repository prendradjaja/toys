import random

from rules import *  # TODO un-star this import?
from constants import DIRECTIONS

from gridlib import gridplane as gridlib


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
    def is_losing(gamestate):
        for move in get_moves(gamestate):
            after = make_move(gamestate, move)
            if is_win(after):
                return True
        return False

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
