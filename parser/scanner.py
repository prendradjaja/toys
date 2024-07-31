from tokens import Token, TokenType as tt
from string import digits, ascii_lowercase


_DIGITS = set(digits)
_LETTERS = set(ascii_lowercase)


def scan_tokens(text):
    return Scanner(text).scan_tokens()


class Scanner:
    def __init__(self, text):
        self.text = text
        self.current = 0
        self.tokens = []

    def scan_tokens(self):
        while not self.is_at_end():
            self.scan_token()
        return self.tokens

    def scan_token(self):
        if self.match_advance(' '):
            return  # Ignore whitespace
        elif self.match_advance('+'):
            self.tokens.append(Token(tt.PLUS))
            return
        elif self.match_advance('-'):
            self.tokens.append(Token(tt.MINUS))
            return
        elif self.match_advance('*'):
            self.tokens.append(Token(tt.STAR))
            return
        elif self.match_advance('/'):
            self.tokens.append(Token(tt.SLASH))
            return
        elif self.match_advance('('):
            self.tokens.append(Token(tt.LEFT_PAREN))
            return
        elif self.match_advance(')'):
            self.tokens.append(Token(tt.RIGHT_PAREN))
            return

        ch = self.peek()
        if ch in _DIGITS:
            self.scan_number()
        elif ch in _LETTERS:
            self.scan_variable()
        else:
            raise Exception('scanner error: unexpected character ' + repr(ch))

    def scan_number(self):
        lexeme = ''
        while self.peek() in _DIGITS:
            lexeme += self.consume()
        value = int(lexeme)
        token = Token(tt.NUMBER, number_value=value)
        self.tokens.append(token)

    def scan_variable(self):
        name = ''
        while self.peek() in _LETTERS:
            name += self.consume()
        token = Token(tt.VARIABLE, variable_name=name)
        self.tokens.append(token)

    def consume(self):
        if not self.is_at_end():
            result = self.peek()
            self.current += 1
            return result
        else:
            raise Exception('scanner error: tried to consume beyond end of input')

    def peek(self):
        if self.is_at_end():
            return None
        else:
            return self.text[self.current]

    def match_advance(self, ch):
        if self.peek() == ch:
            self.consume()
            return True
        else:
            return False

    def is_at_end(self):
        if self.current >= len(self.text):
            assert self.current == len(self.text)
            return True
        else:
            return False
