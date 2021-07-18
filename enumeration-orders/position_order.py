from types import SimpleNamespace as obj


def main(options, length):
    state = obj(nodes=0, results=[])
    dfs((), options, length, state)
    return state


def dfs(node, options, length, state):
    state.nodes += 1
    if len(node) == length:
        state.results.append(node)
        return
    for child in children(node, options):
        dfs(child, options, length, state)


def children(node, options):
    for o in options:
        yield node + (o,)
