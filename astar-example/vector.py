# Copy-pasted from repo with tests and documentation:
# https://github.com/prendradjaja/toys/tree/master/vector

class Vector:
    def __init__(self, elements):
        self.elements = tuple(elements)

    def __add__(self, other):
        return Vector(a + b for a, b in zip(self, other))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return Vector(a - b for a, b in zip(self, other))

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        return Vector(a * other for a in self)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return f'Vector([{", ".join(repr(el) for el in self.elements)}])'

    def __getitem__(self, key):
        return self.elements[key]

    def __eq__(self, other):
        return self.elements == other.elements

    def __hash__(self):
        return hash(self.elements)

    @classmethod
    def enumerate2d(cls, grid):
        for r, row in enumerate(grid):
            for c, value in enumerate(row):
                yield cls([r, c]), value
