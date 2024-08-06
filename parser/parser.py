from tokens import TokenType as tt
from ast_nodes import Number, Variable, BinOp


def parse(tokens):
    return Parser(tokens).parse()


# Like any recursive descent parser, the structure of the code closely matches
# the structure of the grammar. See README.md for the grammar.
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        result = self.parse_program()
        assert self.is_at_end()
        return result

    def parse_program(self):
        return self.parse_expression()

    def parse_expression(self):
        expression = self.parse_term()
        while self.match_advance(tt.PLUS, tt.MINUS):
            op = self.previous().type
            right = self.parse_term()
            expression = BinOp(expression, op, right)
        return expression

    def parse_term(self):
        term = self.parse_primary()
        while self.match_advance(tt.STAR, tt.SLASH):
            op = self.previous().type
            right = self.parse_primary()
            term = BinOp(term, op, right)
        return term

    def parse_primary(self):
        if self.match_advance(tt.VARIABLE):
            return Variable(self.previous().variable_name)
        elif self.match_advance(tt.NUMBER):
            return Number(self.previous().number_value)
        elif self.match_advance(tt.LEFT_PAREN):
            expression = self.parse_expression()
            if not self.match_advance(tt.RIGHT_PAREN):  # Could create an expect() helper
                raise Exception('parser error: expected ")"')
            return expression
        else:
            token = self.peek()
            if token:
                raise Exception('parser error: unexpected token ' + str(token.type))
            else:
                raise Exception('parser error: unexpected end of input')

    def consume(self):
        if not self.is_at_end():
            result = self.peek()
            self.current += 1
            return result
        else:
            raise Exception('parser error: tried to consume beyond end of input')

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def match_advance(self, *token_types):
        token = self.peek()
        if token and token.type in token_types:
            self.consume()
            return True
        else:
            return False

    def is_at_end(self):
        token = self.peek()
        return token and token.type == tt.EOF
