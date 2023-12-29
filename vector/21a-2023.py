#!/usr/bin/env python3

from vector import Vector


DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def main():
    world = open('./ex-21-2023.txt').read().splitlines()
    step_count = 6

    # Find start position
    for pos, ch in enumerate2d(world):
        if ch == 'S':
            start = Vector(pos)
            break

    # Simulate
    reachable = {start}
    for _ in range(step_count):
        reachable = iterate(world, reachable)

    answer = len(reachable)
    assert answer == 16
    print('(correct)', answer)


def iterate(world, reachable):
    def neighbors(pos):
        for offset in DIRECTIONS:
            pos2 = pos + offset
            if in_bounds(world, pos2) and getitem(world, pos2) != '#':
                yield pos2

    return {
        pos2
        for pos in reachable
        for pos2 in neighbors(pos)
    }


def getitem(grid, pos):
    assert in_bounds(grid, pos)
    r, c = pos
    return grid[r][c]


def in_bounds(grid, pos):
    r, c = pos
    return (
        0 <= r < len(grid) and
        0 <= c < len(grid[0])
    )


def enumerate2d(grid):
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            yield (r, c), value


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


if __name__ == '__main__':
    main()
