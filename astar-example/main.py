import astar

from vector import Vector


def main():
    world = [list(line) for line in open('./world.txt').read().splitlines()]
    for pos, ch in Vector.enumerate2d(world):
        if ch == 'S':
            start = pos
        elif ch == 'E':
            end = pos

    print('Without a heuristic, A* is Dijkstra. Here is a shortest path:')
    # n.b. The paths returned may be different, but both are equal length.
    visited = set()
    path = list(astar.find_path(
        start,
        end,
        lambda node: neighbors(world, visited, node),
    ))
    show(world, path, [])

    print('\nDijkstra explores the world from start outward (. = visited)')
    show(world, path, visited)

    print('\nWith a heuristic, A* searches "best first"')
    visited = set()
    path = list(astar.find_path(
        start,
        end,
        lambda node: neighbors(world, visited, node),
        heuristic_cost_estimate_fnct = manhattan_distance,
    ))
    show(world, path, visited)


def show(world, path, visited):
    for r, row in enumerate(world):
        for c, ch in enumerate(row):
            pos = Vector([r, c])
            if ch in ['S', 'E']:
                display = ch
            elif pos in path:
                display = '+'
            elif pos in visited:
                display = '.'
            else:
                display = ch
            print(display, end='')
        print()


def manhattan_distance(node1, node2):
    return sum(abs(x) for x in node1 - node2)


def neighbors(world, visited, node):
    visited.add(node)
    for d in DIRECTIONS:
        neighbor = node + d
        if in_bounds(world, neighbor) and getitem(world, neighbor) != '#':
            yield neighbor


DIRECTIONS = [
    UP := (-1, 0),
    RIGHT := (0, 1),
    DOWN := (1, 0),
    LEFT := (0, -1),
]


def getitem(grid, pos):
    r, c = pos
    assert (0 <= r < len(grid) and 0 <= c < len(grid[0]))
    return grid[r][c]


def in_bounds(grid, pos):
    r, c = pos
    return (
        0 <= r < len(grid) and
        0 <= c < len(grid[0])
    )


if __name__ == '__main__':
    main()
