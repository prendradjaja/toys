from random_letter import random_letter
from legal_words import legal_words
from collections import Counter
import itertools


def main():
    rack = [random_letter() for _ in range(7)]
    score = 0
    while True:
        valid = False
        print(''.join(rack), score)
        while not valid:
            word = input('> ')
            valid = is_valid(word.upper(), rack) and word.lower() in legal_words
        score += 1
        rack = list(word.upper()[1:])
        rack.append(random_letter())
        if game_over(rack):
            print(''.join(rack), 'Game over! Final score:', score)
            return


def is_valid(word, rack):
    '''
    >>> is_valid('APEX', list('XPEA'))
    True
    >>> is_valid('APEX', list('XPEAA'))
    True
    >>> is_valid('APEX', list('XPE'))
    False
    '''
    rack_counts = Counter(rack)
    rack_counts.subtract(Counter(word))
    return all(count >= 0 for count in rack_counts.values())


def game_over(rack):
    return not any(''.join(word).lower() in legal_words for word in itertools.permutations(rack))


if __name__ == '__main__':
    main()
