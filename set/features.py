from collections import OrderedDict


# Any number of features and choices is allowed (edit this dict to customize).

FEATURES = OrderedDict([
    ('count', [1, 2, 3]),
    ('shape', ['diam', 'squig', 'oval']),
    ('shading', ['solid', 'stripe', 'open']),
    ('color', ['red', 'green', 'purple']),
])

# Each feature must have an equal number of choices
assert len(set(len(options) for options in FEATURES.values())) == 1


FEATURE_NAMES = list(FEATURES.keys())


# Despite the variable names, any number of features and any number of choices
# is possible. These names are just easier to think about than COUNT_FEATURES
# and COUNT_CHOICES.
FOUR = len(FEATURES)  # how many features?
THREE = len(next(iter(FEATURES.values())))  # how many choices for each feature?
