from enum import Enum, auto
from dataclasses import dataclass, field

class TokenType(Enum):
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    NUMBER = auto()
    VARIABLE = auto()
    EOF = auto()

@dataclass
class Token:
    type: ...  # TokenType
    number_value: ... = field(default=None, kw_only=True)  # int
    variable_name: ... = field(default=None, kw_only=True)  # str
    def __post_init__(self):
        if self.type == TokenType.NUMBER:
            assert self.number_value is not None
        elif self.type == TokenType.VARIABLE:
            assert self.variable_name is not None
