from tokens import Token, TokenType


class Node:
    """
    The parent class for every node in the AST
    """


class Expr(Node):
    """
    Expressions evaluate to a result, like x + (3 * y) >= 6
    """

    pass


class Stmt(Node):
    """
    Statements perform an action
    """

    pass


class Integer(Expr):
    """
    Example: 17
    """

    def __init__(self, value, line):
        assert isinstance(value, int), value
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Integer[{self.value}]"


class Float(Expr):
    """
    Example 1.234
    """

    def __init__(self, value, line):
        assert isinstance(value, float), value
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Float[{self.value}]"


class UnOp(Expr):
    """
    Example -operand
    """

    def __init__(self, op: Token, operand: Expr, line):
        assert isinstance(op, Token), op
        assert isinstance(operand, Expr), operand
        self.line = line

        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"UnOp({self.op.lexeme}, {self.operand})"


class BinOp(Expr):
    """
    Example x + y
    """

    def __init__(self, op: Token, left: Expr, right: Expr, line):
        assert isinstance(op, Token), op
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right

        self.op = op
        self.left = left
        self.right = right
        self.line = line

    def __repr__(self):
        return f"BinOp({self.op.lexeme}, {self.left}, {self.right})"


class LogicalOp(Expr):
    """
    Example: x and y, x or y
    """

    def __init__(self, op: Token, left: Expr, right: Expr, line):
        assert isinstance(op, Token), op
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right

        self.op = op
        self.left = left
        self.right = right
        self.line = line

    def __repr__(self):
        return f"LogicalOp({self.op.lexeme}, {self.left}, {self.right})"


class Grouping(Expr):
    """
    Example: ( <expr> )
    """

    def __init__(self, value, line):
        assert isinstance(value, Expr), value
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Grouping({self.value})"


class Bool(Expr):
    """
    Example: true, false
    """

    def __init__(self, value, line):
        assert isinstance(value, bool), value
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Grouping({self.value})"


class String(Expr):
    """
    Example: 'this is a string'
    """

    def __init__(self, value, line):
        assert isinstance(value, str), value
        self.value = value
        self.line = line

    def __repr__(self):
        return f"String({self.value})"


class Stmts(Node):
    """
    A list of statements
    """

    def __init__(self, stmts, line):
        assert all(isinstance(stmt, Stmt) for stmt in stmts), stmts
        self.stmts = stmts
        self.line = line

    def __repr__(self):
        return f"Stmts({self.stmts})"


class PrintStmt(Stmt):
    """
    Example: print value
    """

    def __init__(self, value, end, line):
        assert isinstance(value, Expr), value
        self.value = value
        self.line = line
        self.end = end

    def __repr__(self):
        return f"PrintStmt({self.value}), end={self.end!r}"


class IfStmt(Stmt):
    """
    "if" <expr> "then" <then_stmts> ("else" <else_stmts>)? "end"
    """

    def __init__(self, test, then_stmts, else_stmts, line):
        assert isinstance(test, Expr), test
        assert isinstance(then_stmts, Stmts), then_stmts
        assert else_stmts is None or isinstance(else_stmts, Stmts), else_stmts
        self.test = test
        self.then_stmts = then_stmts
        self.else_stmts = else_stmts
        self.line = line

    def __repr__(self):
        return f"IfStmt({self.test}, then:{self.then_stmts}, else:{self.else_stmts})"


class Identifier(Expr):
    """
    Example: x, PI, y
    """

    def __init__(self, name, line):
        assert isinstance(name, str), name
        self.name = name
        self.line = line

    def __repr__(self):
        return f"Identifier({self.name})"


class Assignment(Stmt):
    """
    left := right
    x := 12 + 34 + (3 - y)
    12 := x
    """

    def __init__(self, left, right, line):
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right
        self.left = left
        self.right = right
        self.line = line

    def __repr__(self):
        return f"Assignment(left: {self.left}, right: {self.right})"
