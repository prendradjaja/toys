#!/usr/bin/env python3.12

import itertools

from vector import Vector


UP = Vector([-1, 0])
DOWN = Vector([1, 0])
LEFT = Vector([0, -1])
RIGHT = Vector([0, 1])


def main():
    instructions = []
    for line in open('./ex-18-2023.txt').read().splitlines():
        hexnum = line.split()[-1].strip('()#')
        assert len(hexnum) == 6
        n = int(hexnum[:5], 16)
        direction = {
            '0': RIGHT,
            '1': DOWN,
            '2': LEFT,
            '3': UP,
        }[hexnum[-1]]
        instructions.append((direction, n))

    pos = Vector([0, 0])
    vertices = []
    for direction, n in instructions:
        pos = pos + n * direction
        vertices.append(pos)

    # This approach is from _Kuroni_ on Reddit: https://old.reddit.com/r/adventofcode/comments/18evyu9/2023_day_10_solutions/kcqmhwk/
    answer = perimeter_rectilinear(vertices) + count_interior_points(vertices)
    assert answer == 952408144115
    print('(correct)', answer)


def perimeter_rectilinear(polygon):
    '''
    Polygon must be rectilinear.
    '''
    total = 0
    for v, w in itertools.pairwise(polygon + [polygon[0]]):
        total += abs(sum(w - v))
    return total


def count_interior_points(polygon):
    '''
    Polygon must be rectilinear and have only integer vertices.

    Uses Pick's Theroem:
    https://en.wikipedia.org/wiki/Pick%27s_theorem
    '''
    perimeter = perimeter_rectilinear(polygon)
    assert perimeter % 2 == 0
    half_perimeter = perimeter // 2

    my_area = area(polygon)
    assert int(my_area) == my_area
    my_area = int(my_area)

    return my_area + 1 - half_perimeter


def area(polygon):
    '''
    Shoelace formula
    https://en.wikipedia.org/wiki/Shoelace_formula
    '''
    total = 0
    for v, w in itertools.pairwise(polygon + [polygon[0]]):
        vr, vc = v
        wr, wc = w
        total += vr * wc
        total -= wr * vc
    return abs(total / 2)


if __name__ == '__main__':
    main()
