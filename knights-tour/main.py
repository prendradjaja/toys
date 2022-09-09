'''
Find a knight's tour on an NxN chessboard using Warnsdorff's rule, which is a
heuristic for choosing which square to move to. It is not guaranteed to
produce a successful tour, but it is quite effective: "It produces a
successful tour more than 85% of the time on boards smaller than 50×50, and
more than 50% of the time on boards smaller than 100×100."*

* https://www.futilitycloset.com/2014/11/10/warnsdorffs-rule/
'''


import random
import time
import os


N = 8


def main():
    visited = set()
    pos = (random.randrange(N), random.randrange(N))
    for _ in range(N * N):
        visited.add(pos)
        show(visited)
        time.sleep(0.02)
        moves = [pos2 for pos2 in legal_moves(pos) if pos2 not in visited]
        if not moves:
            break
        pos = min(moves, key=lambda pos2: warnsdorff_heuristic(pos2, visited))


def warnsdorff_heuristic(pos2, visited):
    return len([pos3 for pos3 in legal_moves(pos2) if pos3 not in visited])


def show(visited):
    os.system('clear')
    for r in range(N):
        for c in range(N):
            if (r, c) in visited:
                print('# ', end='')
            else:
                print('. ', end='')
        print()


def legal_moves(pos):
    r, c = pos
    offsets = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2)]
    for (i, j) in offsets:
        pos2 = (r + i, c + j)
        if in_bounds(pos2):
            yield pos2


def in_bounds(pos):
    r, c = pos
    return (
        0 <= r < N and
        0 <= c < N
    )


main()
