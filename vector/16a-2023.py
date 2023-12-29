#!/usr/bin/env python3

from collections import namedtuple

from vector import Vector


Photon = namedtuple('Photon', 'pos vel')

UP = Vector([-1, 0])
DOWN = Vector([1, 0])
LEFT = Vector([0, -1])
RIGHT = Vector([0, 1])


def main():
    photons = set()
    new_photons = {Photon(Vector([0, 0]), RIGHT)}
    world = open('./ex-16-2023.txt').read().splitlines()

    while new_photons:
        photons |= new_photons
        new_photons = {
            p2
            for p1 in new_photons
            for p2 in step(p1, world)
        } - photons

    answer = len({p.pos for p in photons})
    assert answer == 46
    print('(correct)', answer)


def step(photon, world):
    HEIGHT = len(world)
    WIDTH = len(world[0])

    r, c = photon.pos
    ch = world[r][c]

    if ch == '.':
        new_photons = [photon._replace(pos = photon.pos + photon.vel)]
    elif ch in '/\\':
        new_photons = reflect(photon, ch)
    elif ch in '-|':
        new_photons = split(photon, ch)

    # Exclude any photons that fall off the edge of the world
    return [
        p
        for p in new_photons
        if 0 <= p.pos[0] < HEIGHT
        and 0 <= p.pos[1] < WIDTH
    ]


def reflect(photon, ch):
    case = photon.vel, ch
    if case == (RIGHT, '/'):
        vel = UP
    elif case == (RIGHT, '\\'):
        vel = DOWN
    elif case == (LEFT, '/'):
        vel = DOWN
    elif case == (LEFT, '\\'):
        vel = UP
    elif case == (UP, '/'):
        vel = RIGHT
    elif case == (UP, '\\'):
        vel = LEFT
    elif case == (DOWN, '/'):
        vel = LEFT
    elif case == (DOWN, '\\'):
        vel = RIGHT
    else:
        raise Exception('unreachable case')
    return [photon._replace(
        pos = photon.pos + vel,
        vel = vel
    )]


def split(photon, ch):
    if (
        photon.vel in [LEFT, RIGHT] and ch == '-' or
        photon.vel in [UP, DOWN] and ch == '|'
    ):
        return [photon._replace(pos = photon.pos + photon.vel)]
    elif ch == '-':
        assert photon.vel in [UP, DOWN]
        return [
            photon._replace(
                pos = photon.pos + LEFT,
                vel = LEFT
            ),
            photon._replace(
                pos = photon.pos + RIGHT,
                vel = RIGHT
            ),
        ]
    elif ch == '|':
        assert photon.vel in [LEFT, RIGHT]
        return [
            photon._replace(
                pos = photon.pos + UP,
                vel = UP
            ),
            photon._replace(
                pos = photon.pos + DOWN,
                vel = DOWN
            ),
        ]
    else:
        raise Exception('unreachable case')


if __name__ == '__main__':
    main()
