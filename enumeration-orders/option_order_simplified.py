from types import SimpleNamespace as obj


def main(options, length):
    state = obj(nodes=0, results=[])
    dfs((), options, length, state)
    return state


def dfs(node, options, length, state):
    state.nodes += 1
    if len(node) == length:
        result = node_to_result(node, length)
        state.results.append(result)
        return
    for child in children(node, options, length):
        dfs(child, options, length, state)


def children(node, options, length):
    if len(node) == 0:
        pass  # All options are available
    else:
        option, _ = node[-1]
        index = options.index(option)
        options = options[index:]

    occupied = {pos for _, pos in node}
    unoccupied = [pos for pos in range(length) if pos not in occupied]

    if len(options) == 0:
        return

    # option 0
    if len(node) == 0:
        option = options[0]
        possible_positions = unoccupied
    else:
        _, last_position = node[-1]
        possible_positions = [pos for pos in unoccupied if pos > last_position]
    yield from children_helper(node, option, possible_positions)

    # other options
    for other_option in options[1:]:
        yield from children_helper(node, other_option, unoccupied)


def children_helper(node, option, possible_positions):
    for position in possible_positions:
        yield node + ((option, position),)



def node_to_result(node, length):
    '''
    Think of it like this:
    >>> node_to_result((('A', 1), ('A', 2), ('B', 0)), 3)
    ('B', 'A', 'A')

    Edge case (non-leaf node):
    >>> node_to_result((), 3)
    (None, None, None)
    >>> node_to_result((('A', 1),), 3)
    (None, 'A', None)
    '''
    result = [None] * length
    for option, location in node:
        result[location] = option
    return tuple(result)
