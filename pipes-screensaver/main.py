import itertools
import curses
import random
from random import randint
import time


# TODO:
# - Gracefully handle resizing terminal
# - Exit on keypress, not ctrl-c
# - Maybe have some minimum travel distance before turning (so pipes look nicer)?
# - Similar: Maybe some minimum pipe length before ending


def main(stdscr):
    global DOUBLE_HEIGHT, WIDTH

    stdscr.clear()

    # Hack: Usually characters in a terminal are taller than they are wide, so
    # divide y coordinate by 2 to avoid pipes travelling vertically much faster
    # than horizontally
    HEIGHT = curses.LINES
    DOUBLE_HEIGHT = curses.LINES * 2
    WIDTH = curses.COLS

    RAW_COLORS = [
        curses.COLOR_BLUE, curses.COLOR_CYAN, curses.COLOR_GREEN,
        curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_WHITE,
        curses.COLOR_YELLOW
    ]
    COLORS = []
    for n, color in zip(itertools.count(1), RAW_COLORS):
        curses.init_pair(n, color, curses.COLOR_BLACK)
        COLORS.append(curses.color_pair(n))

    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    random_pos = lambda: (randint(1, DOUBLE_HEIGHT), randint(1, WIDTH))
    random_color = lambda: random.choice(COLORS)
    random_direction = lambda: random.choice(DIRECTIONS)

    pos = random_pos()
    color = random_color()
    direction = random_direction()

    while True:
        pos = addvec(pos, direction)

        if in_bounds(pos):
            stdscr.addstr(
                pos[0] // 2,
                pos[1],
                '█',
                color
            )

        if random.random() < 1/5:
            direction = random_direction()

        if (
            random.random() < 1/80 or
            # Don't spend too much time off-screen
            (not in_bounds(pos) and random.random() < 1/4)
        ):
            pos = random_pos()
            color = random_color()

        if random.random() < 1/2000:
            stdscr.clear()

        stdscr.addstr(HEIGHT-1, WIDTH-1, '')  # Keep cursor in the corner
        stdscr.refresh()
        time.sleep(0.025)


def addvec(a, b):
    return (
        a[0] + b[0],
        a[1] + b[1],
    )


def in_bounds(pos):
    r, c = pos
    return (
        0 <= r < DOUBLE_HEIGHT and
        0 <= c < WIDTH
    )


curses.wrapper(main)
