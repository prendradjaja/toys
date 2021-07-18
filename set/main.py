import itertools
import random

from features import FEATURES, FEATURE_NAMES, FOUR, THREE


def main():
    deck = make_deck()
    board = []
    matches = []

    print('Deck\tBoard\tMatched')

    def display_state():
        print(len(deck), len(board), f'{len(matches)}*{THREE}={len(matches)*THREE}', sep='\t')

    for _ in range(THREE * FOUR):
        board.append(deck.pop())
    display_state()

    while True:
        match = find_match(board)
        while deck and not match:
            board.append(deck.pop())
            match = find_match(board)
        if match:
            for card in match:
                board.remove(card)
            matches.append(match)
            display_state()
        else:
            break

    if board:
        display_state()
        print()
        print('Leftover cards:')
        for card in board:
            display_card(card)
    else:
        print()
        print('Perfect game! (No cards left)')


def find_match(board):
    for cards in itertools.combinations(board, THREE):
        if is_match(cards):
            return cards
    return None


def make_deck():
    deck = list(itertools.product(range(THREE), repeat=FOUR))
    random.shuffle(deck)
    return deck


def is_match(cards):
    assert len(cards) == THREE
    return all(is_match_in_feature(cards, n) for n in range(FOUR))


def is_match_in_feature(cards, feature_index):
    assert len(cards) == THREE
    values = [card[feature_index] for card in cards]
    return len(set(values)) in [1, THREE]


def display_card(card):
    choices = [
        str(FEATURES[FEATURE_NAMES[feature_index]][option_index])
        for feature_index, option_index in enumerate(card)
    ]
    string = ',\t'.join(choices)
    print(string)


if __name__ == '__main__':
    main()
