from interpreter import TYPE_BOOL, TYPE_NUMBER, TYPE_STRING
from model import *
from tokens import *
from utils import *


class Compiler:
    def __init__(self):
        self.code = []

    def emit(self, instruction):
        self.code.append(instruction)

    def compile(self, node):
        if isinstance(node, Integer):
            value = (TYPE_NUMBER, float(node.value))
            self.emit(("PUSH", value))

        elif isinstance(node, Float):
            value = (TYPE_NUMBER, float(node.value))
            self.emit(("PUSH", value))

        elif isinstance(node, Bool):
            value = (
                TYPE_BOOL,
                True if node.value == True or node.value == "true" else False,
            )
            self.emit(("PUSH", value))

        elif isinstance(node, String):
            value = (TYPE_STRING, stringify(node.value))
            self.emit(("PUSH", value))

        elif isinstance(node, BinOp):
            self.compile(node.left)
            self.compile(node.right)
            if node.op.token_type == TokenType.PLUS:
                self.emit(("ADD",))
            elif node.op.token_type == TokenType.MINUS:
                self.emit(("SUB",))
            elif node.op.token_type == TokenType.STAR:
                self.emit(("MUL",))
            elif node.op.token_type == TokenType.SLASH:
                self.emit(("DIV",))
            elif node.op.token_type == TokenType.CARET:
                self.emit(("EXP",))
            elif node.op.token_type == TokenType.MOD:
                self.emit(("MOD",))
            elif node.op.token_type == TokenType.LT:
                self.emit(("LT",))
            elif node.op.token_type == TokenType.GT:
                self.emit(("GT",))
            elif node.op.token_type == TokenType.LE:
                self.emit(("LE",))
            elif node.op.token_type == TokenType.GE:
                self.emit(("GE",))
            elif node.op.token_type == TokenType.EQ:
                self.emit(("EQ",))
            elif node.op.token_type == TokenType.NE:
                self.emit(("NE",))
            else:
                raise Exception(f"Unsupported binary operator: {node.op.token_type}")

        elif isinstance(node, Stmts):
            for stmt in node.stmts:
                self.compile(stmt)

        elif isinstance(node, PrintStmt):
            self.compile(node.value)
            if node.end == "":
                self.emit(("PRINT",))
            else:
                self.emit(("PRINTLN"))

    def compile_code(self, node):
        self.emit(("LABEL", "START"))
        self.compile(node)
        self.emit(("HALT",))
        return self.code
