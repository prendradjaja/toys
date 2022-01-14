'''
1. A simple game: Start with a random rack of Scrabble tiles, e.g.

  SATUDRE

2. Make a word out of them. This is your new rack.

  STARED

3. Remove the first letter and draw a random tile from the (infinite) bag.

  TAREDH

4. Go back to step 2 and repeat until you can no longer make a word, e.g.

  DEARTH -> EARTHX
  HEART -> EARTP
  PART -> ARTD
  DART -> ARTZ
  TAR -> ARX
  A -> E
  (game over)


REMARKS:

A small amount of animation in a GUI environment would probably make it more
obvious what happens at each turn.

This is not a very fun game.
'''


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
