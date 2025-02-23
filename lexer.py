from typing import List, Tuple
from tokens import Token, TokenType, keywords

TokenTuple = Tuple[TokenType, str, int]
Tokens = List[TokenTuple]


class Lexer:
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.curr = 0
        self.line = 1
        self.tokens: Tokens = []
        pass

    def advance(self):
        if self.is_index_out_of_bounds():
            return "\0"
        char = self.source[self.curr]
        self.curr = self.curr + 1
        return char

    def peek(self):
        if self.is_index_out_of_bounds():
            return "\0"
        return self.source[self.curr]

    def lookahead(self, n=1):
        if self.curr >= len(self.source):
            return "\0"

        return self.source[self.curr + n]

    def is_index_out_of_bounds(self):
        return self.curr >= len(self.source)

    def match(self, expected):
        if self.is_index_out_of_bounds():
            return False
        if self.source[self.curr] != expected:
            return False
        self.curr = self.curr + 1
        return True

    def add_token(self, token_type: TokenType):
        self.tokens.append(
            Token(token_type, self.source[self.start : self.curr], self.line)
        )

    def handle_number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == "." and self.lookahead().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
            self.add_token(TokenType.FLOAT)
        else:
            self.add_token(TokenType.INTEGER)

    def handle_string(self, start_quote):
        while self.peek() != start_quote and not self.is_index_out_of_bounds():
            self.advance()

        if self.is_index_out_of_bounds():
            raise SyntaxError(f"Line {self.line}: Unterminated string")

        self.advance()
        self.add_token(TokenType.STRING)

    def handle_identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        ## check if identifier matches a key in the keywords dict
        text = self.source[self.start : self.curr]
        keyword_type = keywords.get(text)
        if keyword_type == None:
            self.add_token(TokenType.IDENTIFIER)
        else:
            self.add_token(keyword_type)

    def tokenize(self):
        while self.curr < len(self.source):
            self.start = self.curr
            ch = self.advance()
            if ch == "\n":
                self.line = self.line + 1
            elif ch == " ":
                pass
            elif ch == "\t":
                pass
            elif ch == "\r":
                pass
            elif ch == "#":
                while self.peek() != "\n" and not self.curr >= len(self.source):
                    self.advance()
            elif ch == "(":
                self.add_token(TokenType.LPAREN)
            elif ch == ")":
                self.add_token(TokenType.RPAREN)
            elif ch == "{":
                self.add_token(TokenType.LCURLY)
            elif ch == "}":
                self.add_token(TokenType.RCURLY)
            elif ch == "[":
                self.add_token(TokenType.LSQUAR)
            elif ch == "]":
                self.add_token(TokenType.RSQUAR)
            elif ch == ".":
                self.add_token(TokenType.DOT)
            elif ch == ",":
                self.add_token(TokenType.COMMA)
            elif ch == "+":
                self.add_token(TokenType.PLUS)
            elif ch == "-":
                if self.peek() == "-":
                    while self.peek() != "\n" and not self.is_index_out_of_bounds():
                        self.advance()
                    self.advance()
                else:
                    self.add_token(TokenType.MINUS)
            elif ch == "*":
                self.add_token(TokenType.STAR)
            elif ch == "^":
                self.add_token(TokenType.CARET)
            elif ch == "/":
                self.add_token(TokenType.SLASH)
            elif ch == ";":
                self.add_token(TokenType.SEMICOLON)
            elif ch == "?":
                self.add_token(TokenType.QUESTION)
            elif ch == "%":
                self.add_token(TokenType.MOD)
            elif ch == "=":
                if self.match("="):
                    self.add_token(TokenType.EQEQ)
                else:
                    self.add_token(TokenType.EQ)
            elif ch == "~":
                if self.match("="):
                    self.add_token(TokenType.NE)
                else:
                    self.add_token(TokenType.NOT)
            elif ch == "<":
                if self.match("="):
                    self.add_token(TokenType.LE)
                else:
                    self.add_token(TokenType.LT)
            elif ch == ">":
                if self.match("="):
                    self.add_token(TokenType.GE)
                else:
                    self.add_token(TokenType.GT)
            elif ch == ":":
                if self.match("="):
                    self.add_token(TokenType.ASSIGN)
                else:
                    self.add_token(TokenType.COLON)
            elif ch.isdigit():
                self.handle_number()
            elif ch == '"' or ch == "'":
                self.handle_string(ch)
            elif ch.isalpha() or ch == "_":
                self.handle_identifier()
            else:
                raise SyntaxError(
                    f"[Line ${self.line}] Error at {ch}: Unexpected character"
                )

        return self.tokens
