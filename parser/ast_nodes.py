from dataclasses import dataclass

@dataclass
class Number:
    value: ...  # int

@dataclass
class Variable:
    name: ...  # string

@dataclass
class BinOp:
    op: ...  # TokenType
    left: ...  # a Number, Variable, or BinOp
    right: ...  # a Number, Variable, or BinOp
