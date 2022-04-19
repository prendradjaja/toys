# https://www.youtube.com/watch?v=vhp3d9XXDcQ

import random


def main():
    n = 100_000

    # 1-2-3
    roll_die = lambda: random.choice([1, 2, 3])
    xs = []
    for _ in range(n):
        rolls = roll_until(3, roll_die)
        xs.append(len(rolls))
    print(sum(xs) / len(xs))

    # 2-4-6
    roll_die = lambda: random.choice([1, 2, 3, 4, 5, 6])
    xs = []
    for _ in range(n):
        rolls = roll_until(6, roll_die)
        if set(rolls) <= {2, 4, 6}:
            xs.append(len(rolls))
    print(sum(xs) / len(xs))


def roll_until(desired_roll, roll_die):
    '''
    Given a function ROLL_DIE, roll the die until DESIRED_ROLL comes up.

    Return a list of all the rolls that were done.
    '''
    rolls = []
    while True:
        roll = roll_die()
        rolls.append(roll)
        if roll == desired_roll:
            return rolls


if __name__ == '__main__':
    main()
