## Position-order and option-order enumeration

How many ways are there to build a string of length N from K characters? K\^N.

How can we enumerate all of these?

----

One simple way (`position_order.py`) is to build it character-by-character
from left to right. This corresponds to a tree. For example, if N = 2 and K =
2 (with characters, say, A and B), the tree would look like this:

```
     ??
   /    \
  A?     B?
 / \     / \
AA AB   BA BB
```

The leaves of the tree are the completed strings.

(In terms of performance, this is probably not the best approach for solving
the enumeration problem, since we have to walk the whole tree and we're only
interested in the leaf nodes. See below for my motivation for looking at
this.)

Let's zoom in on just one node. At the node `A?`, we want to decide what the
next character will be, and we have two choices, so there are two children.

A position-order enumeration corresponds to a very regular tree: Every node
has K children.

Before moving on to option-order enumeration, let's look at one more example
of position-order. Say N = 5 and K = 3. We won't draw the whole tree this
time, but again we'll look at a single node.

**What are the children of node `AC???`?**
- `ACA??`, `ACB??`, `ACC??`

So this node has 3 children. (This corresponds to each of the K = 3 choices
for the next character.)

----

Another approach (`option_order.py`) is to decide where to place all the `A`s,
then all the `B`s, and so on. (That is: Once you've placed some letter, you
can never place an earlier letter.)

To prevent reaching the same node from multiple paths, we must always place
`A`s from left to right (but we can skip "slots"), `B`s from left to right,
and so on. (That is: Within each letter, once you've placed that letter in
some position, you can never make a placement in an earlier position.)

Examples with N = 4, K = 3:

We won't draw the whole tree, but we can look at a few individual nodes to get
an idea of what the tree might look like (and to make sure the idea I've
described is comprehensible!)

**`????` has 12 children:**
- You can place an `A` in any position:
    - `A???`, `?A??`, `??A?`, `???A`
- You can place a `B` in any position:
    - `B???`, `?B??`, `??B?`, `???B`
- You can place a `C` in any position:
    - `C???`, `?C??`, `??C?`, `???C`

**`?A??` has these children:**
- You can place an `A` in any **later** position:
    - `?AA?`, `?A?A`
- You can place a `B` in any position:
    - `BA??`, `?AB?`, `?A?B`
- You can place a `C` in any position:
    - `CA??`, `?AC?`, `?A?C`

**`?B??` has these children:**
- You can't place an `A` (because you've already placed a `B`)
- You can place a `B` in any later position:
    - `?BB?` ,`?B?B`
- You can place a `C` in any position:
    - `CB??`, `?BC?`, `?B?C`

In comparison to position-order enumeration, the corresponding tree would be
very unbalanced. Most nodes have so many children -- the tree must be huge!
This is somewhat mitigated by the fact that if you choose a "later" child
(later position in the string and/or later character in the alphabet), that
child will necessarily have fewer children.

## So many nodes! ...how many?

This repo explores just how many more nodes an option-order enumeration tree
has when compared to a position-order enumeration tree.

The option-order enumeration definitely requires more nodes, but the
difference is maybe smaller than one might expect. Here are some of the
results from this exploration.

```console
$ python3 main.py
Length (N) = 4
Options = ABCD (K = 4)

Position order:
  Nodes: 341	Results: 256

Option order:
  Nodes: 431	Results: 256
```

```console
$ python3 main.py ABCD 8
Length (N) = 8
Options = ABCD (K = 4)

Position order:
  Nodes: 87,381	Results: 65,536

Option order:
  Nodes: 124,511	Results: 65,536
```

## Why?

I'm thinking about [backtracking search][backtracking], used for solving
Constraint Satisfaction Problems (CSPs). If you consider e.g. backtracking to
solve a Sudoku, this corresponds to searching a subset of the position-order
enumeration tree.

The full enumeration tree may not be a practical thing, when enumeration can
be done without creating the whole tree and its internal nodes, but the
relevant part here is that backtracking searches a much smaller space than the
full tree.

Actually, it searches a smaller space than even just the leaf nodes.
(Searching just the leaf nodes would correspond to solving a Sudoku by brute
force -- with e.g. 50 empty spaces, 9\^50 possibilities would take
prohibitively long! But backtracking can solve a typical Sudoku in less than a
second.)

I'm currently (July 2021) interested in a different CSP (Project Euler #161).
Such "position-order backtracking" might not be possible (there may not be a
concept of "position-order" here), but it should be possible to do an
"option-order backtracking."

But it's very possible that that would take too long! I might be barking down
the completely wrong tree. 🌳


[backtracking]: https://en.wikipedia.org/wiki/Backtracking
