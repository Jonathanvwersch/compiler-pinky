from tokens import (
    TOK_CARET,
    TOK_COMMA,
    TOK_DOT,
    TOK_LCURLY,
    TOK_LPAREN,
    TOK_LSQUAR,
    TOK_MINUS,
    TOK_MOD,
    TOK_PLUS,
    TOK_QUESTION,
    TOK_RCURLY,
    TOK_RPAREN,
    TOK_RSQUAR,
    TOK_SEMICOLON,
    TOK_SLASH,
    TOK_STAR,
    Token,
)


CHARS = {"plus": "+", "minus": "-"}


class Lexer:
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.curr = 0
        self.line = 1
        self.tokens = []
        pass

    def advance(self):
        char = self.source[self.curr]
        self.curr = self.curr + 1
        return char

    def peek(self):
        return self.source[self.curr]

    def lookahead(self, n=1):
        if self.curr + n < len(self.source):
            return self.source[self.curr + n]

    def match(self, expected):
        if self.curr >= len(self.source):
            return False
        if self.source[self.curr] != expected:
            return False
        self.curr = self.curr + 1
        return True

    def add_token(self, token_type):
        self.tokens.append(Token(token_type, self.source[self.start : self.curr]))

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
                while self.peek() != "\n":
                    self.advance()
            elif ch == "(":
                self.add_token(TOK_LPAREN)
            elif ch == ")":
                self.add_token(TOK_RPAREN)
            elif ch == "{":
                self.add_token(TOK_LCURLY)
            elif ch == "}":
                self.add_token(TOK_RCURLY)
            elif ch == "[":
                self.add_token(TOK_LSQUAR)
            elif ch == "]":
                self.add_token(TOK_RSQUAR)
            elif ch == ".":
                self.add_token(TOK_DOT)
            elif ch == ",":
                self.add_token(TOK_COMMA)
            elif ch == "+":
                self.add_token(TOK_PLUS)
            elif ch == "-":
                self.add_token(TOK_MINUS)
            elif ch == "*":
                self.add_token(TOK_STAR)
            elif ch == "^":
                self.add_token(TOK_CARET)
            elif ch == "/":
                self.add_token(TOK_SLASH)
            elif ch == ";":
                self.add_token(TOK_SEMICOLON)
            elif ch == "?":
                self.add_token(TOK_QUESTION)
            elif ch == "%":
                self.add_token(TOK_MOD)

        return self.tokens
