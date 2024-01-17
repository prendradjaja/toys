from dataclasses import dataclass
import math


@dataclass
class LinearEquation:
    m: ...  # slope
    b: ...  # y-intercept

    def __call__(self, x):
        return self.m * x + self.b

    @classmethod
    def from_points(cls, p1, p2):
        '''
        >>> LinearEquation.from_points((1, 2), (3, 3))
        LinearEquation(m=0.5, b=1.5)
        '''
        x1, y1 = p1
        x2, y2 = p2
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        return LinearEquation(m, b)
