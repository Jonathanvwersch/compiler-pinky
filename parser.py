from model import *
from tokens import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = 0

    def factor(self):
        pass

    def unary(self):
        pass

    def term(self):
        pass

    def primary(self):
        pass

    def expr(self):
        pass

    def parse(self):
        ast = self.expr
        return ast
