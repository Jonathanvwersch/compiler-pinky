import codecs
from model import *
from state import Environment
from utils import runtime_error


TYPE_NUMBER = "TYPE_NUMBER"
TYPE_STRING = "TYPE_STRING"
TYPE_BOOL = "TYPE_BOOL"


class Interpreter:
    def interpret(self, node, env):
        if isinstance(node, Integer):
            return (TYPE_NUMBER, float(node.value))
        elif isinstance(node, Float):
            return (TYPE_NUMBER, float(node.value))
        elif isinstance(node, String):
            return (TYPE_STRING, str(node.value))
        elif isinstance(node, Grouping):
            return self.interpret(node.value, env)
        elif isinstance(node, Identifier):
            value = env.get_var(node.name)
            if value is None:
                runtime_error(f"Undeclared identifier {node.name!r}", node.line)
            if value[1] is None:
                runtime_error(f"Uninitialized identifier {node.name!r}", node.line)
            return value
        elif isinstance(node, Assignment):
            right_type, right_val = self.interpret(node.right, env)

            env.set_var(node.left.name, (right_type, right_val))

        elif isinstance(node, Bool):
            return (TYPE_BOOL, node.value)
        elif isinstance(node, BinOp):
            left_type, left_val = self.interpret(node.left, env)
            right_type, right_val = self.interpret(node.right, env)

            if node.op.token_type == TokenType.PLUS:
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_val + right_val)
                elif left_type == TYPE_STRING or right_type == TYPE_STRING:
                    return (TYPE_STRING, str(left_val) + str(right_val))
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} between {left_type} and {right_type}",
                        node.op.line,
                    )
            if node.op.token_type == TokenType.GT:
                if (
                    left_type == TYPE_NUMBER
                    and right_type == TYPE_NUMBER
                    or (left_type == TYPE_STRING and right_type == TYPE_STRING)
                ):
                    return (TYPE_BOOL, left_val > right_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} between {left_type} and {right_type}",
                        node.op.line,
                    )
            if node.op.token_type == TokenType.GE:
                if (
                    left_type == TYPE_NUMBER
                    and right_type == TYPE_NUMBER
                    or (left_type == TYPE_STRING and right_type == TYPE_STRING)
                ):
                    return (TYPE_BOOL, left_val >= right_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} between {left_type} and {right_type}",
                        node.op.line,
                    )
            if node.op.token_type == TokenType.LE:
                if (
                    left_type == TYPE_NUMBER
                    and right_type == TYPE_NUMBER
                    or (left_type == TYPE_STRING and right_type == TYPE_STRING)
                ):
                    return (TYPE_BOOL, left_val <= right_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} between {left_type} and {right_type}",
                        node.op.line,
                    )

            if node.op.token_type == TokenType.LT:
                if (
                    left_type == TYPE_NUMBER
                    and right_type == TYPE_NUMBER
                    or (left_type == TYPE_STRING and right_type == TYPE_STRING)
                ):
                    return (TYPE_BOOL, left_val < right_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} between {left_type} and {right_type}",
                        node.op.line,
                    )

            if node.op.token_type == TokenType.EQEQ:
                if (
                    left_type == TYPE_NUMBER
                    and right_type == TYPE_NUMBER
                    or (left_type == TYPE_STRING and right_type == TYPE_STRING)
                    or (left_type == TYPE_BOOL and right_type == TYPE_BOOL)
                ):
                    return (TYPE_BOOL, left_val == right_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} between {left_type} and {right_type}",
                        node.op.line,
                    )

            if node.op.token_type == TokenType.NE:
                if (
                    left_type == TYPE_NUMBER
                    and right_type == TYPE_NUMBER
                    or (left_type == TYPE_STRING and right_type == TYPE_STRING)
                ):
                    return (TYPE_BOOL, left_val != right_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} between {left_type} and {right_type}",
                        node.op.line,
                    )

            if node.op.token_type == TokenType.STAR:
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_val * right_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} between {left_type} and {right_type}",
                        node.op.line,
                    )

            if node.op.token_type == TokenType.MINUS:
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_val - right_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} between {left_type} and {right_type}",
                        node.op.line,
                    )
            if node.op.token_type == TokenType.SLASH:
                if right_val == 0:
                    runtime_error(f"Division by zero.", node.line)
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_val / right_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} between {left_type} and {right_type}",
                        node.op.line,
                    )
            if node.op.token_type == TokenType.MOD:
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_val % right_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} between {left_type} and {right_type}",
                        node.op.line,
                    )
            if node.op.token_type == TokenType.CARET:
                if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, left_val**right_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} between {left_type} and {right_type}",
                        node.op.line,
                    )
        elif isinstance(node, LogicalOp):
            left_type, left_val = self.interpret(node.left, env)

            if node.op.token_type == TokenType.OR:
                if left_val:
                    return (left_type, left_val)
            elif node.op.token_type == TokenType.AND:
                if not left_val:
                    return (left_type, left_val)

            return self.interpret(node.right)
        elif isinstance(node, UnOp):
            operand_type, operand_val = self.interpret(node.operand, env)
            if node.op.token_type == TokenType.PLUS:
                if operand_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, +operand_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} with {operand_type}",
                        node.op.line,
                    )
            if node.op.token_type == TokenType.MINUS:
                if operand_type == TYPE_NUMBER:
                    return (TYPE_NUMBER, -operand_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} with {operand_type}",
                        node.op.line,
                    )
            if node.op.token_type == TokenType.NOT:
                if operand_type == TYPE_BOOL:
                    return (TYPE_BOOL, not operand_val)
                else:
                    runtime_error(
                        f"Unsupported operator {node.op.lexeme} {operand_type}",
                        node.op.line,
                    )
        elif isinstance(node, Stmts):
            for stmt in node.stmts:
                self.interpret(stmt, env)
        elif isinstance(node, PrintStmt):
            _, expr_value = self.interpret(node.value, env)
            print(
                codecs.escape_decode(bytes(str(expr_value), "utf-8"))[0].decode(
                    "utf-8"
                ),
                end=node.end,
            )
        elif isinstance(node, WhileStmt):
            new_env = env.new_env()
            while True:
                test_type, test_val = self.interpret(node.test, env)
                if test_type != TYPE_BOOL:
                    runtime_error(f"While test is not a boolean expression", node.line)

                if not test_val:
                    break

                self.interpret(node.while_stmts, new_env)

        elif isinstance(node, IfStmt):
            test_type, test_val = self.interpret(node.test, env)
            if test_type != TYPE_BOOL:
                runtime_error("Condition test is not a boolean expression", node.line)
            if test_val:
                self.interpret(node.then_stmts, env.new_env())
            else:
                self.interpret(node.else_stmts, env.new_env())

    def interpret_ast(self, node):
        # entry point for interpreter, creating a brand new global/parent environment
        env = Environment()
        self.interpret(node, env)
