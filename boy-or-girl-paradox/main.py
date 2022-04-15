# https://www.youtube.com/watch?v=go3xtDdsNQM
# https://en.wikipedia.org/wiki/Boy_or_Girl_paradox

import random
from collections import namedtuple


Child = namedtuple('Child', 'gender birthday')


def main():
    n = 10_000
    families = [(get_child(), get_child()) for _ in range(n)]

    print('Mr. Jones has two children. What is the probability he has a girl if...')

    print('\n...he has a boy?')
    families_with_boy = [fam for fam in families if has_boy(fam)]
    print('About', percentage(families_with_boy, has_girl))

    print('\n...he has a boy born on Tuesday?')
    families_with_tuesday_boy = [fam for fam in families if has_tuesday_boy(fam)]
    print('About', percentage(families_with_tuesday_boy, has_girl))


def get_child():
    return Child(
        gender = random.choice('BG'),
        birthday = random.randint(0, 6),
    )


def percentage(lst, pred):
    m = len([x for x in lst if pred(x)])
    n = len(lst)
    return f'{m/n:.2%} ({m} of {n})'


def has_girl(family):
    return any(child.gender == 'G' for child in family)


def has_boy(family):
    return any(child.gender == 'B' for child in family)


def has_tuesday_boy(family):
    return any(
        child.gender == 'B' and child.birthday == 2
        for child in family
    )


if __name__ == '__main__':
    main()
