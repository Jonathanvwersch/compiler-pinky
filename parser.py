from typing import List
from model import *
from tokens import *
from utils import parse_error


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
        if self.is_index_out_of_bounds(self.curr):
            return
        return self.tokens[self.curr]

    def is_next(self, expected_type):
        if self.is_index_out_of_bounds(self.curr + 1):
            return False

        return self.tokens[self.curr + 1].token_type == expected_type

    def expect(self, expected_type):
        if self.is_index_out_of_bounds(self.curr):
            parse_error(
                f"Unexpected end of input, expected {expected_type!r}",
                self.previous_token().line,
            )
        elif self.peek().token_type == expected_type:
            token = self.advance()
            return token
        else:
            parse_error(
                f"Expected {expected_type!r}, found {self.peek().lexeme!r}",
                self.peek().line,
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

    # <primary> ::= <integer> | <float> | '(' <expr> ') | <bool> | <string>'
    def primary(self):
        if self.match(TokenType.INTEGER):
            return Integer(
                int(self.previous_token().lexeme), line=self.previous_token().line
            )
        if self.match(TokenType.FLOAT):
            return Float(
                float(self.previous_token().lexeme), line=self.previous_token().line
            )

        if self.match(TokenType.TRUE):
            return Bool(True, line=self.previous_token().line)

        if self.match(TokenType.STRING):
            # remove quotes from string during lexing
            return String(
                str(self.previous_token().lexeme[1:-1]), line=self.previous_token().line
            )

        if self.match(TokenType.FALSE):
            return Bool(False, line=self.previous_token().line)

        if self.match(TokenType.LPAREN):
            expr = self.expr()
            if not self.match(TokenType.RPAREN):
                parse_error('Error: ")" expected.', self.previous_token().line)

            return Grouping(expr, line=self.previous_token().line)

    # <exponent> ::= <primary> ( "^" <primary> )*
    def exponent(self):
        expr = self.primary()
        while self.match(TokenType.CARET):
            op = self.previous_token()
            right = self.exponent()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    # <unary> ::= ('+'|'-'|'~')* <exponent>
    def unary(self):
        if (
            self.match(TokenType.NOT)
            or self.match(TokenType.MINUS)
            or self.match(TokenType.PLUS)
        ):
            op = self.previous_token()
            operand = self.unary()
            return UnOp(op, operand, line=op.line)
        return self.exponent()

    # <modulo> ::= <unary> ( "%" <unary> )*
    def modulo(self):
        expr = self.unary()

        while self.match(TokenType.MOD):
            op = self.previous_token()
            right = self.unary()
            expr = BinOp(op, expr, right, line=op.line)

        return expr

    # <multiplication> ::= <unary> ( ('*'|'/') <unary> )*
    def multiplication(self):
        expr = self.modulo()
        while self.match(TokenType.STAR) or self.match(TokenType.SLASH):
            op = self.previous_token()
            right = self.modulo()
            expr = BinOp(op, expr, right, line=op.line)

        return expr

    # <expr> ::= <multiplication> ('+' | '-') <multiplication> )*
    def addition(self):
        expr = self.multiplication()
        while self.match(TokenType.PLUS) or self.match(TokenType.MINUS):
            op = self.previous_token()
            right = self.multiplication()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    # <comparison> ::= <addition> (( ">" | ">=" | "<" | "<=" ) <addition>)*
    def comparison(self):
        expr = self.addition()
        while (
            self.match(TokenType.LT)
            or self.match(TokenType.GE)
            or self.match(TokenType.GT)
            or self.match(TokenType.LE)
        ):
            op = self.previous_token()
            right = self.addition()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    # <equality> ::= <comparison> ( ( "~=" | "==" ) <comparison> )*
    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.NE) or self.match(TokenType.EQEQ):
            op = self.previous_token()
            right = self.comparison()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    def logical_and(self):
        expr = self.equality()
        while self.match(TokenType.AND):
            op = self.previous_token()
            right = self.equality()
            expr = LogicalOp(op, expr, right, line=op.line)
        return expr

    def logical_or(self):
        expr = self.logical_and()
        while self.match(TokenType.OR):
            op = self.previous_token()
            right = self.logical_and()
            expr = LogicalOp(op, expr, right, line=op.line)
        return expr

    def expr(self):
        return self.logical_or()

    # <print_stmt> ::= "print" <expr>
    def print_stmt(self, end):
        if self.match(TokenType.PRINT) or self.match(TokenType.PRINTLN):
            val = self.expr()
            return PrintStmt(val, end, line=self.previous_token().line)

    def stmt(self):
        # predictive parsing, where the next token predicts what is the next statement
        if self.peek().token_type == TokenType.PRINT:
            return self.print_stmt(end="")
        if self.peek().token_type == TokenType.PRINTLN:
            return self.print_stmt(end="\n")
        # elif self.peek().token_type == TokenType.IF:
        #     return self.if_stmt()
        # elif self.peek().token_type == TokenType.WHILE:
        #     return self.if_stmt()
        # elif self.peek().token_type == TokenType.FOR:
        #     return self.if_stmt()
        # elif self.peek().token_type == TokenType.FUNC:
        #     return self.if_stmt()
        # else:
        #     pass

    def stmts(self):
        stmts = []
        # TODO: loop all the statements, creating Stmt() for each one
        while self.curr < len(self.tokens):
            stmt = self.stmt()
            stmts.append(stmt)

        return Stmts(stmts, line=self.previous_token().line)

    def program(self):
        return self.stmts()

    def parse(self):
        ast = self.program()
        return ast
