from dataclasses import dataclass
import dataclasses
from types import SimpleNamespace


_CDEFGAB = 'CDEFGAB'


@dataclass(frozen=True)
class Pitch:
    '''
    Construct a pitch:
    >>> Pitch('C', 0, 4)
    Pitch(letter='C', modifier=0, octave=4)

    Or get it from PITCHES:
    >>> from music import PITCHES as P
    >>> P.C4
    Pitch(letter='C', modifier=0, octave=4)
    '''
    letter: ...  # 'A' | 'B' | ... | 'G'
    modifier: ...  # -2 (double flat) to 2 (double sharp)
    octave: ...  # int - n.b. edge case, see midi_number()

    def midi_number(self):
        '''
        >>> from music import PITCHES as P
        >>> P.C4.midi_number()
        60
        >>> P.A4.midi_number()
        69
        '''
        return (
            [12, 14, 16, 17, 19, 21, 23][_CDEFGAB.index(self.letter)]
            + self.modifier
            + self.octave * 12
        )

    def __str__(self):
        if self.modifier >= 0:
            modifier = 's' * self.modifier
        else:
            modifier = 'f' * abs(self.modifier)
        return f'{self.letter}{modifier}{self.octave}'

    def __add__(self, other):
        '''
        >>> from music import PITCHES as P, INTERVALS as I
        >>> print(P.C4 + I.M3)
        E4
        >>> print(P.Ef4 + I.M3)
        G4
        >>> print(P.Bs4 + I.M3)
        Dss5
        '''
        if not isinstance(other, Interval):
            return NotImplemented

        interval = other
        idx = _CDEFGAB.index(self.letter)
        letter = _CDEFGAB[(idx + interval.number - 1) % len(_CDEFGAB)]

        result = Pitch(letter, 0, self.octave)
        if result.midi_number() < self.midi_number():
            result = dataclasses.replace(result, octave=result.octave + 1)

        modifier = interval.half_steps() - result.midi_number() + self.midi_number()
        result = dataclasses.replace(result, modifier=modifier)
        return result

    # def __sub__(self, other):
    #     # todo: Support "pitch - pitch = interval"?
    #     if not isinstance(other, Interval):
    #         return NotImplemented


_LEGAL_INTERVALS = [
    (quality, number)
    for number in [1, 4, 5]
    for quality in 'dPA'
] + [
    (quality, number)
    for number in [2, 3, 6, 7]
    for quality in 'dmMA'
]

@dataclass(frozen=True)
class Interval:
    '''
    Construct an interval:
    >>> Interval('M', 3)
    Interval(quality='M', number=3)

    Or get it from INTERVALS:
    >>> from music import INTERVALS as I
    >>> I.M3
    Interval(quality='M', number=3)
    '''
    quality: ...
    number: ...  # 1 | 2 | 3 | 4 | 5 | 6 | 7, but not 8 (just use 1)

    def __post_init__(self):
        if (self.quality, self.number) not in _LEGAL_INTERVALS:
            raise ValueError('Invalid interval')

    def __str__(self):
        return f'{self.quality}{self.number}'

    def half_steps(self):
        if self.number in [1, 4, 5]:
            modifier = {
                'd': -1,
                'P': 0,
                'A': 1,
            }[self.quality]
        else:
            assert self.number in [2, 3, 6, 7]
            modifier = {
                'd': -2,
                'm': -1,
                'M': 0,
                'A': 1,
            }[self.quality]

        return modifier + {
            1: 0,
            2: 2,
            3: 4,
            4: 5,
            5: 7,
            6: 9,
            7: 11,
        }[self.number]

    # todo: Support invert()?


_pitches = [
    Pitch(letter, modifier, octave)
    for letter in _CDEFGAB
    for modifier in [-1, 0, 1]
    for octave in range(9)
]
PITCHES = SimpleNamespace(**{str(each): each for each in _pitches})


_intervals = [
    Interval(quality, number)
    for quality, number in _LEGAL_INTERVALS
]
INTERVALS = SimpleNamespace(**{str(each): each for each in _intervals})
