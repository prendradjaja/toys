def is_cycle(directions, *, verbose=False):
    '''
    >>> is_cycle('RRRRR')
    True
    >>> is_cycle('LLLLL')
    True
    >>> is_cycle('LRLRLRLRLR')
    True
    >>> is_cycle('RRLRRLRRL')
    True
    >>> is_cycle('R')
    False
    >>> is_cycle('LLLLLL')
    False
    >>> is_cycle('RLLLLR', verbose=True)  # returns to initial edge but opposite direction
    ('1a', '2a')
    ('2a', '3a')
    ('3a', '3b')
    ('3b', '2c')
    ('2c', '2b')
    ('2b', '2a')
    ('2a', '1a')
    False
    '''
    start = ('1a', '2a')
    g = make_dodecahedron()
    pos = start
    if verbose:
        print(pos)
    for d in directions:
        pos = make_turn(g, pos, d)
        if verbose:
            print(pos)
    return pos == start


def make_turn(g, e, direction):
    '''
    e is an oriented edge

    >>> make_turn(make_dodecahedron(), ('1a', '2a'), 'R')
    ('2a', '3a')
    >>> make_turn(make_dodecahedron(), ('4a', '3a'), 'L')
    ('3a', '2a')
    '''
    f = [
        f for f in get_next_edges_from_oriented_edge(g, e)
        if g.get_turn_direction(e, f) == direction
    ][0]
    if g.normalize_edge(*e) in get_next_edges_from_oriented_edge(g, f):
        f = f[::-1]
        assert g.normalize_edge(*e) not in get_next_edges_from_oriented_edge(g, f)
    return f


def get_expected_number_of_turns():
    g = make_dodecahedron()
    turns = set()
    for e in g.edges:
        forwards_edges = get_next_edges_from_oriented_edge(g, e)
        backwards_edges = get_next_edges_from_oriented_edge(g, e[::-1])
        for f in forwards_edges + backwards_edges:
            normalized = g.normalize_turn(e, f)
            turns.add(normalized)
    return len(turns)


def get_next_edges_from_oriented_edge(g, e):
    v, w = e
    return [edge for edge in g.get_edges_from(w) if g.normalize_edge(*e) != g.normalize_edge(*edge)]


def make_dodecahedron():
    '''
    >>> g = make_dodecahedron()
    >>> len(g.vertices)
    20
    >>> len(g.edges)
    30
    >>> [len(g.get_edges_from(v)) for v in g.vertices]
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    >>> (g.has_edge('2a', '2b')  # TODO Maybe delete this test
    ... and g.has_edge('2b', '2c')
    ... and g.has_edge('2c', '3b')
    ... and g.has_edge('3b', '3a')
    ... and g.has_edge('3a', '2a'))
    True
    >>> len(g.turn_directions) == get_expected_number_of_turns() == 60
    True

    Turns
    >>> g.get_turn_direction(('1a', '1b'), ('1b', '1c'))
    'R'
    >>> g.get_turn_direction(('1b', '1c'), ('1a', '1b'))
    'L'
    '''
    A_VERTICES = ['1a', '2a', '3a', '4a', '5a']  # Top layer
    B_VERTICES = ['1b', '2b', '3b', '4b', '5b']  # B and C make up the equator
    C_VERTICES = ['1c', '2c', '3c', '4c', '5c']
    D_VERTICES = ['1d', '2d', '3d', '4d', '5d']  # Bottom layer
    VERTICES = A_VERTICES + B_VERTICES + C_VERTICES + D_VERTICES

    g = GraphWithTurns(VERTICES)

    ### EDGES -----------------------------------------------------------------

    top_layer_edges = []
    for v, w in consecutives(A_VERTICES + A_VERTICES[:1]):
        g.add_edge(v, w)
        top_layer_edges.append( (v, w) )
    bottom_layer_edges = []
    for v, w in consecutives(D_VERTICES + D_VERTICES[:1]):
        g.add_edge(v, w)
        bottom_layer_edges.append( (v, w) )

    top_to_equator_edges = []
    for v, w in zip(A_VERTICES, B_VERTICES):
        g.add_edge(v, w)
        top_to_equator_edges.append( (v, w) )
    bottom_to_equator_edges = []
    for v, w in zip(D_VERTICES, C_VERTICES):
        g.add_edge(v, w)
        bottom_to_equator_edges.append( (v, w) )

    equator_edges = []
    EQUATOR = ['1b', '1c', '2b', '2c', '3b', '3c', '4b', '4c', '5b', '5c']
    for v, w in consecutives(EQUATOR + EQUATOR[:1]):
        g.add_edge(v, w)
        equator_edges.append( (v, w) )

    ### TURNS -----------------------------------------------------------------

    def set_other_turn_direction(g, e, f, direction):
        # Set the direction of e (so that it points to f)
        if g.normalize_edge(*f) not in get_next_edges_from_oriented_edge(g, e):
            e = e[::-1]
        assert g.normalize_edge(*f) in get_next_edges_from_oriented_edge(g, e)

        other_f = [edge for edge in get_next_edges_from_oriented_edge(g, e) if g.normalize_edge(*edge) != g.normalize_edge(*f)][0]
        g.set_turn_direction(e, other_f, other(direction))

    # Turns within top layer
    assert top_layer_edges == [('1a', '2a'), ('2a', '3a'), ('3a', '4a'), ('4a', '5a'), ('5a', '1a')]
    for e, f in consecutives(top_layer_edges + top_layer_edges[:1]):
        g.set_turn_direction(e, f, 'R')
        set_other_turn_direction(g, e, f, 'R')
    # Turns within bottom layer
    assert bottom_layer_edges == [('1d', '2d'), ('2d', '3d'), ('3d', '4d'), ('4d', '5d'), ('5d', '1d')]
    for e, f in consecutives(bottom_layer_edges + bottom_layer_edges[:1]):
        g.set_turn_direction(e, f, 'L')
        set_other_turn_direction(g, e, f, 'L')

    # Turns from top layer to equator
    assert top_to_equator_edges == [('1a', '1b'), ('2a', '2b'), ('3a', '3b'), ('4a', '4b'), ('5a', '5b')]
    for e, f in zip(top_layer_edges, top_to_equator_edges):
        g.set_turn_direction(e, f, 'R')
        set_other_turn_direction(g, e, f, 'R')
    # Turns from bottom layer to equator
    assert bottom_to_equator_edges == [('1d', '1c'), ('2d', '2c'), ('3d', '3c'), ('4d', '4c'), ('5d', '5c')]
    for e, f in zip(bottom_layer_edges, bottom_to_equator_edges):
        g.set_turn_direction(e, f, 'L')
        set_other_turn_direction(g, e, f, 'L')

    # Turns within equator
    assert equator_edges == [('1b', '1c'), ('1c', '2b'), ('2b', '2c'), ('2c', '3b'), ('3b', '3c'), ('3c', '4b'), ('4b', '4c'), ('4c', '5b'), ('5b', '5c'), ('5c', '1b')]
    direction = 'R'
    for e, f in consecutives(equator_edges + equator_edges[:1]):
        g.set_turn_direction(e, f, direction)
        set_other_turn_direction(g, e, f, direction)
        direction = other(direction)

    # Turns from top-to-equator edges to equator edges
    for e, f in zip(top_to_equator_edges, equator_edges[0::2]):
        g.set_turn_direction(e, f, 'R')
        set_other_turn_direction(g, e, f, 'R')
    # Turns from bottom-to-equator edges to equator edges
    for e, f in zip(bottom_to_equator_edges, equator_edges[1::2]):
        g.set_turn_direction(e, f, 'L')
        set_other_turn_direction(g, e, f, 'L')

    for e in g.edges:
        assert ['L', 'R'] == sorted(g.get_turn_direction(e, f) for f in get_next_edges_from_oriented_edge(g, e))
        assert ['L', 'R'] == sorted(g.get_turn_direction(e, f) for f in get_next_edges_from_oriented_edge(g, e[::-1]))

    return g


def other(direction):
    assert direction in ['L', 'R']
    if direction == 'L':
        return 'R'
    else:
        return 'L'


class GraphWithTurns:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = set()
        self.turn_directions = {}

    def add_edge(self, v, w):
        assert v in self.vertices and w in self.vertices
        edge = self._normalize_edge(v, w)
        self.edges.add(edge)

    def has_edge(self, v, w):
        edge = self._normalize_edge(v, w)
        return edge in self.edges

    def get_edges_from(self, v):
        return [edge for edge in self.edges if v in edge]

    def set_turn_direction(self, e, f, direction):
        assert direction in ['L', 'R']
        normalized = self._normalize_turn(e, f, _was_reversed := [])
        was_reversed = _was_reversed[0]

        old_value = self.turn_directions.get(normalized)
        if was_reversed:
            self.turn_directions[normalized] = other(direction)
        else:
            self.turn_directions[normalized] = direction

        if old_value:
            assert old_value == self.turn_directions[normalized]

    def get_turn_direction(self, e, f):
        normalized = self._normalize_turn(e, f, _was_reversed := [])
        was_reversed = _was_reversed[0]

        direction = self.turn_directions[normalized]
        if was_reversed:
            return other(direction)
        else:
            return direction

    def normalize_edge(self, v, w):
        return self._normalize_edge(v, w)

    def _normalize_edge(self, v, w):
        assert v in self.vertices and w in self.vertices
        return tuple(sorted([v, w]))

    def normalize_turn(self, e, f):
        return self._normalize_turn(e, f)

    def _normalize_turn(self, e, f, _was_reversed=None):
        e = self._normalize_edge(*e)
        f = self._normalize_edge(*f)
        e1, e2 = e
        f1, f2 = f
        assert all(v in self.vertices for v in [e1, e2, f1, f2])
        original_order = (e, f)
        result = tuple(sorted(original_order))
        if _was_reversed is not None:
            was_reversed = original_order != result
            _was_reversed.append(was_reversed)
        return result


def consecutives(lst):
    '''
    >>> list(''.join(tup) for tup in consecutives('abcd'))
    ['ab', 'bc', 'cd']
    '''
    for a, b in zip(lst, lst[1:]):
        yield a, b
