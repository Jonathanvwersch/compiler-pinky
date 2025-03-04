from model import *


class Interpreter:
    def __init__(self):
        pass

    def interpret(self, node):
        if isinstance(node, Integer):
            return node.value
        elif isinstance(node, Float):
            return node.value
        elif isinstance(node, Grouping):
            return self.interpret(node.value)
        elif isinstance(node, BinOp):
            left_val = self.interpret(node.left)
            right_val = self.interpret(node.right)
            if node.op.token_type == TokenType.PLUS:
                return left_val + right_val
            if node.op.token_type == TokenType.STAR:
                return left_val * right_val
            if node.op.token_type == TokenType.MINUS:
                return left_val - right_val
            if node.op.token_type == TokenType.SLASH:
                return left_val / right_val
        elif isinstance(node, UnOp):
            operand = self.interpret(node.operand)
            if node.op.token_type == TokenType.PLUS:
                return +operand
            if node.op.token_type == TokenType.MINUS:
                return -operand
            # if node.op.token_type == TokenType.NOT:
            #     return ~operand
