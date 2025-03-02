from typing import List
from model import *
from tokens import *


class Parser:
    def __init__(self, tokens):
        self.tokens: List[Token] = tokens
        self.curr = 0

    def is_index_out_of_bounds(self, index):
        return index >= len(self.tokens)

    def advance(self):
        if self.is_index_out_of_bounds(self.curr):
            raise IndexError("Attempted to advance past the end of the token stream.")
        char = self.tokens[self.curr]
        self.curr += 1
        return char

    def peek(self):
        return self.tokens[self.curr]

    def is_next(self, expected_type):
        if self.is_index_out_of_bounds(self.curr + 1):
            return False

        return self.tokens[self.curr + 1].token_type == expected_type

    def expect(self, expected_type):
        if self.is_index_out_of_bounds(self.curr):
            raise SyntaxError(f"Unexpected end of input, expected {expected_type!r}")
        elif self.peek().token_type == expected_type:
            token = self.advance()
            return token
        else:
            raise SyntaxError(
                f"Expected {expected_type!r}, found {self.peek().lexeme!r}"
            )

    def match(self, expected_type):
        if self.is_index_out_of_bounds(self.curr):
            return False
        if self.peek().token_type != expected_type:
            return False
        self.advance()
        return True

    def previous_token(self):
        return self.tokens[self.curr - 1]

    # <primary> ::= <integer> | <float> | '(' <expr> ')'
    def primary(self):
        if self.match(TokenType.INTEGER):
            return Integer(int(self.previous_token().lexeme))
        if self.match(TokenType.FLOAT):
            return Float(float(self.previous_token().lexeme))
        if self.match(TokenType.LPAREN):
            expr = self.expr()
            if not self.match(TokenType.RPAREN):
                raise SyntaxError(f'Error: ")" expected.')

            return Grouping(expr)

    # <unary> ::= ('+'|'-'|'~') <unary> | primary
    def unary(self):
        if (
            self.match(TokenType.NOT)
            or self.match(TokenType.MINUS)
            or self.match(TokenType.PLUS)
        ):

            op = self.previous_token()
            operand = self.unary()
            return UnOp(op, operand)
        return self.primary()

    # <factor> ::= <unary>
    def factor(self):
        return self.unary()

    # <term> ::= <factor> ( ('*'|'/') <factor> )*
    def term(self):
        expr = self.factor()

        while self.match(TokenType.STAR) or self.match(TokenType.SLASH):
            op = self.previous_token()
            right = self.factor()
            expr = BinOp(op, expr, right)

        return expr

    # <expr> ::= <term> ('+' | '-') <term> )*
    def expr(self):
        expr = self.term()
        while self.match(TokenType.PLUS) or self.match(TokenType.MINUS):
            op = self.previous_token()
            right = self.term()
            expr = BinOp(op, expr, right)
        return expr

    def parse(self):
        ast = self.expr()
        return ast
