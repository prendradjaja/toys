from operator import methodcaller as dot


class F:
    def __init__(self, fn):
        self.fn = fn
    def __ror__(self, other):
        return self.fn(other)


class map_:
    def __init__(self, fn):
        self.fn = fn
    def __ror__(self, other):
        return [self.fn(x) for x in other]


class filter_:
    def __init__(self, fn):
        self.fn = fn
    def __ror__(self, other):
        return [x for x in other if self.fn(x)]


class join:
    def __init__(self, sep):
        self.sep = sep
    def __ror__(self, other):
        return self.sep.join(other)


class sort:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    def __ror__(self, other):
        other = other[:]
        other.sort(**self.kwargs)
        return other
