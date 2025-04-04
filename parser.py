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
        if self.curr >= len(self.tokens):
            return False
        return self.peek().token_type == expected_type

    def expect(self, expected_type):
        if self.curr >= len(self.tokens):
            parse_error(
                f"Found {self.previous_token().lexeme!r} at the end of parsing",
                self.previous_token().line,
            )
        elif self.peek().token_type == expected_type:
            token = self.advance()
            return token
        else:
            parse_error(
                f"Expected {expected_type!r}, found {self.peek().lexeme!r}.",
                self.peek().line,
            )

    def previous_token(self):
        return self.tokens[self.curr - 1]

    def match(self, expected_type):
        if self.curr >= len(self.tokens):
            return False
        if self.peek().token_type != expected_type:
            return False
        self.curr = (
            self.curr + 1
        )  # If it is a match, we return True and also comsume that token
        return True

    def args(self):
        args = []
        while not self.is_next(TokenType.RPAREN):
            args.append(self.expr())
            if not self.is_next(TokenType.RPAREN):
                self.expect(TokenType.COMMA)
        return args

    # <primary>  ::=  <integer>
    #              |  <float>
    #              |  <bool>
    #              |  <string>
    #              | '(' <expr> ')'
    def primary(self):
        if self.match(TokenType.INTEGER):
            return Integer(
                int(self.previous_token().lexeme), line=self.previous_token().line
            )
        elif self.match(TokenType.FLOAT):
            return Float(
                float(self.previous_token().lexeme), line=self.previous_token().line
            )
        elif self.match(TokenType.TRUE):
            return Bool(True, line=self.previous_token().line)
        elif self.match(TokenType.FALSE):
            return Bool(False, line=self.previous_token().line)
        elif self.match(TokenType.STRING):
            return String(
                str(self.previous_token().lexeme[1:-1]), line=self.previous_token().line
            )  # Remove the quotes at the beginning and at the end of the lexeme
        elif self.match(TokenType.LPAREN):
            expr = self.expr()
            if not self.match(TokenType.RPAREN):
                parse_error(f'Error: ")" expected.', self.previous_token().line)
            else:
                return Grouping(expr, line=self.previous_token().line)
        else:
            identifier = self.expect(TokenType.IDENTIFIER)
            if self.match(TokenType.LPAREN):
                args = self.args()
                self.expect(TokenType.RPAREN)
                return FuncCall(
                    identifier.lexeme, args, line=self.previous_token().line
                )
            else:
                return Identifier(identifier.lexeme, line=self.previous_token().line)

    # <exponent> ::= <primary> ( "^" <exponent> )*
    def exponent(self):
        expr = self.primary()
        while self.match(TokenType.CARET):
            op = self.previous_token()
            right = self.exponent()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    # <unary>  ::=  ('+'|'-'|'~')* <exponent>
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

    # <multiplication>  ::=  <modulo> ( ('*'|'/') <modulo> )*
    def multiplication(self):
        expr = self.modulo()
        while self.match(TokenType.STAR) or self.match(TokenType.SLASH):
            op = self.previous_token()
            right = self.modulo()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    # <addition>  ::=  <multiplication> ( ('+'|'-') <multiplication> )*
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
            self.match(TokenType.GT)
            or self.match(TokenType.GE)
            or self.match(TokenType.LT)
            or self.match(TokenType.LE)
        ):
            op = self.previous_token()
            right = self.addition()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    # <equality>  ::=  <comparison> ( ( "~=" | "==" ) <comparison> )*
    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.NE) or self.match(TokenType.EQEQ):
            op = self.previous_token()
            right = self.comparison()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    # <logical_and> ::= <equality> ( "and" <equality> )*
    def logical_and(self):
        expr = self.equality()
        while self.match(TokenType.AND):
            op = self.previous_token()
            right = self.equality()
            expr = LogicalOp(op, expr, right, line=op.line)
        return expr

    # <logical_or> ::= <logical_and> ( "or" <logical_and> )*
    def logical_or(self):
        expr = self.logical_and()
        while self.match(TokenType.OR):
            op = self.previous_token()
            right = self.logical_and()
            expr = LogicalOp(op, expr, right, line=op.line)
        return expr

    def expr(self):
        return self.logical_or()

    # <print_stmt>  ::=  ( "print" | "println" ) <expr>
    def print_stmt(self, end):
        if self.match(TokenType.PRINT) or self.match(TokenType.PRINTLN):
            val = self.expr()
            return PrintStmt(val, end, line=self.previous_token().line)

    def while_stmt(self):
        self.expect(TokenType.WHILE)
        test = self.expr()
        self.expect(TokenType.DO)
        while_stmts = self.stmts()
        self.expect(TokenType.END)
        return WhileStmt(test, while_stmts, line=self.previous_token().line)

    def for_stmt(self):
        self.expect(TokenType.FOR)
        identifier = self.primary()
        self.expect(TokenType.ASSIGN)
        start = self.expr()
        self.expect(TokenType.COMMA)
        end = self.expr()
        if self.is_next(TokenType.COMMA):
            self.advance()
            step = self.expr()
        else:
            step = None
        self.expect(TokenType.DO)
        for_stmts = self.stmts()
        self.expect(TokenType.END)
        return ForStmt(
            identifier, start, end, step, for_stmts, line=self.previous_token().line
        )

    # <if_stmt> ::= "if" <expr> "then" <stmts> ( "else" <stmts> )? "end"
    def if_stmt(self):
        self.expect(TokenType.IF)
        test = self.expr()
        self.expect(TokenType.THEN)
        then_stmts = self.stmts()
        if self.is_next(TokenType.ELSE):
            self.advance()  # consume the else
            else_stmts = self.stmts()
        else:
            else_stmts = None
        self.expect(TokenType.END)
        return IfStmt(test, then_stmts, else_stmts, line=self.previous_token().line)

    def params(self):
        params = []
        while not self.is_next(TokenType.RPAREN):
            name = self.expect(TokenType.IDENTIFIER)
            params.append(Param(name.lexeme, line=self.previous_token().line))
            if len(params) > 255:
                parse_error(
                    f"Functions cannot have more than 255 parameters", name.line
                )
            if not self.is_next(TokenType.RPAREN):
                self.expect(TokenType.COMMA)
        return params

    def func_decl(self):
        self.expect(TokenType.FUNC)
        name = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.LPAREN)
        params = self.params()
        self.expect(TokenType.RPAREN)
        body_stmts = self.stmts()
        self.expect(TokenType.END)
        return FuncDecl(
            name.lexeme, params, body_stmts, line=self.previous_token().line
        )

    def ret_stmt(self):
        self.expect(TokenType.RET)
        value = self.expr()
        return RetStmt(value, line=self.previous_token().line)

    def local_assign(self):
        self.expect(TokenType.LOCAL)
        left = self.expr()
        self.expect(TokenType.ASSIGN)
        right = self.expr()
        return LocalAssignment(left, right, line=self.previous_token().line)

    def stmt(self):
        if self.peek().token_type == TokenType.PRINT:
            return self.print_stmt(end="")
        if self.peek().token_type == TokenType.PRINTLN:
            return self.print_stmt(end="\n")
        elif self.peek().token_type == TokenType.IF:
            return self.if_stmt()
        elif self.peek().token_type == TokenType.WHILE:
            return self.while_stmt()
        elif self.peek().token_type == TokenType.FOR:
            return self.for_stmt()
        elif self.peek().token_type == TokenType.FUNC:
            return self.func_decl()
        elif self.peek().token_type == TokenType.RET:
            return self.ret_stmt()
        elif self.peek().token_type == TokenType.LOCAL:
            return self.local_assign()
        else:
            left = self.expr()
            if self.match(TokenType.ASSIGN):
                right = self.expr()
                return Assignment(left, right, line=self.previous_token().line)
            else:
                return FuncCallStmt(left)

    def stmts(self):
        stmts = []
        # Loop all statements of the current block (meaning until we find an "end", or "else", or EOF
        while (
            self.curr < len(self.tokens)
            and not self.is_next(TokenType.ELSE)
            and not self.is_next(TokenType.END)
        ):
            stmt = self.stmt()
            stmts.append(stmt)
        return Stmts(stmts, line=self.previous_token().line)

    def program(self):
        return self.stmts()

    def parse(self):
        ast = self.program()
        return ast
