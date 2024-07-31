A very simple parser for a very simple language, to illustrate the key ideas of
recursive descent parsing.

It's based on the parser and scanner from chapters 4-6 of [Crafting
Interpreters](https://craftinginterpreters.com/contents.html), available free
online from the author (Robert Nystrom).

(See also: [My fork of Crafting
Interpreters](https://github.com/prendradjaja/craftinginterpreters), which
includes Nystrom's code as it looks at the end of each chapter.)


## Table of Contents

- [What we're parsing](#what-were-parsing)
- [About greediness etc](#about-greediness-etc)
- [The grammar](#the-grammar)
- [Usage, entry point, etc](#usage-entry-point-etc)
- [Some differences from the _Crafting Interpreters_ parser and scanner](#some-differences-from-the-crafting-interpreters-parser-and-scanner)
- [Some theory](#some-theory)


## What we're parsing

We want to parse expressions like these:

    0
    123
    x
    height
    1 + 2
    a * b
    20 / width
    1 + 2 + 3
    a - b * c
    (a - b) * c

i.e.

- int literals (but no negative-int literals or unary minus!)
- variables
- `+` `-` `*` `/` with operator precedence
- `()` for grouping
- non-significant whitespace

We also should reject strings NOT in this grammar, e.g.

    1 +
    2 * * 3
    3 3
    (4


## About greediness etc

This parser greedily parses one expression, then expects end of input.

I _think_ greedy parsing is a realistic, normal thing in parsing; even without
e.g. a statement terminator `;` if we're given the input `1 + 2 + 3` we want
to parse the whole thing, not just stop at `1 + 2` or even `1`.

Nystrom's parser is also greedy in this way.


## The grammar

In order to implement operator precedence, we "stratify" the grammar, "[defining]
a separate rule for each precedence level." (_Crafting Interpreters_, [chapter
6](https://craftinginterpreters.com/parsing-expressions.html))

    program -> expression ;
    expression -> term ( ("+" | "-") term)* ;
    term -> primary ( ("*" | "/") primary)* ;
    primary -> VARIABLE
             | NUMBER
             | "(" expression ")" ;


## Usage, entry point, etc

See `test_parser.txt` for parser usage. For implementation, see `parser.py`. Run the tests with:

    python3.12 -m doctest -f test_parser.txt

This repo also contains a scanner (aka lexer aka tokenizer) used by the parser.

You can run all tests (parser and scanner) with:

    make test


## Some differences from the _Crafting Interpreters_ parser and scanner

I don't think any of these change any fundamental concepts, but in case it's
helpful to point them out, here are some differences:

Various names are changed, notably: (Nystrom's choice -> my choice)

- In the grammar:
    - `factor` -> `term` (I think this was actually just a mistake from Nystrom)
- In the scanner and parser:
    - `match()` -> `match_advance()` (I don't want to forget that this method also does an `advance()`)
    - `advance()` -> `consume()` (I just think this is more descriptive)

Some other changes:

- In e.g. `consume()` (Nystrom's `advance()`), I raise an exception if we're already at the end of input. I think this sort of behavior makes it easier to reason about state.
    - We could go farther than this; `peek()` returns `None` where we might
      also expect to raise an exception. In this example, that seemed
      simplest, but for future uses I might consider raising an exception
      and/or replacing `peek()` with something like Nystrom's `check()`, which
      is what we often want `peek()` for anyway.
(We could go farther than this; `peek()` also could raise an exception instead of returning `None`. For this example, returning `None` seemed simplest.)
- Nystrom's scanner has both `current` and `start`, allowing `addToken()` to use those indices to find the current lexeme (as a substring of the source code). This is a great idea! I didn't need it in this case, so I left it out for simplicity.


## Some theory

[Chomsky hierarchy](https://en.wikipedia.org/wiki/Chomsky_hierarchy):
regular -> context-free -> context-sensitive -> recursively enumerable

----

This lexical grammar / scanner is **regular** (no recursion in the grammar).
It requires only **one character of lookahead.**

This syntactic grammar / parser is **context-free**. Similarly, the grammar
requires only **one token of lookahead.** It uses **recursive descent,**
specifically **predictive parsing** i.e. this is an **LL(k) grammar**,
specifically **LL(1)** (because one token of lookahead).

[From Wikipedia:](https://en.wikipedia.org/w/index.php?title=Recursive_descent_parser&oldid=1237251514)

> A predictive parser is a recursive descent parser that does not require
> backtracking.[3] Predictive parsing is possible only for the class of LL(k)
> grammars, which are the context-free grammars for which there exists some
> positive integer k that allows a recursive descent parser to decide which
> production to use by examining only the next k tokens of input. ... A
> predictive parser runs in linear time.
