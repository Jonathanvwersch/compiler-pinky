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


class Decl(Stmt):
    """
    Declarations are statements to declare a new name
    (in our case, functions)
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


class WhileStmt(Stmt):
    """
    "while" <expr> "do" <while_stmt> "end"
    """

    def __init__(self, test, while_stmts, line):
        assert isinstance(test, Expr), test
        assert isinstance(while_stmts, Stmts), while_stmts
        self.test = test
        self.while_stmts = while_stmts
        self.line = line

    def __repr__(self):
        return f"whileStmt({self.test}, do:{self.while_stmts})"


class ForStmt(Stmt):
    """
    "for" <identifier> ":=" <start> "," <end> ("," <increment>)? "do" <for_stmts> "end"
    """

    def __init__(self, identifier, start, end, step, for_stmts, line):
        assert isinstance(identifier, Identifier), identifier
        assert isinstance(start, Expr), start
        assert isinstance(end, Expr), end
        assert isinstance(step, Expr), step
        assert isinstance(for_stmts, Stmts), for_stmts
        self.step = step
        self.for_stmts = for_stmts
        self.start = start
        self.end = end
        self.line = line
        self.identifier = identifier

    def __repr__(self):
        return f"ForStmt({self.identifier}, {self.start}, {self.end}, {self.step}, {self.for_stmts})"


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


class FuncDecl(Stmt):
    """
    "func" <name> "(" <params>? ")" <body_stmts> "end"
    """

    def __init__(self, name, params, body_stmts, line):
        assert isinstance(name, str), name
        assert isinstance(body_stmts, Stmts), body_stmts
        assert all(isinstance(param, Param) for param in params), params
        self.name = name
        self.params = params
        self.line = line
        self.body_stmts = body_stmts

    def __repr__(self):
        return f"FuncDecl(name: {self.name}, params: {self.params}, stmts: {self.body_stmts})"


class Param(Decl):
    """
    A single function parameter
    """

    def __init__(self, name, line):
        assert isinstance(name, str), name
        self.name = name
        self.line = line

    def __repr__(self):
        return f"Param({self.name!r})"


class FuncCall(Expr):
    """
    <name> "(" <args>? ")"
    <args> ::= <expr> ( ',' <expr> )*
    """

    def __init__(self, name, args, line):
        self.name = name
        self.args = args
        self.line = line

    def __repr__(self):
        return f"FuncCall({self.name!r}, {self.args})"


class FuncCallStmt(Stmt):
    """
    A special type of statement used to wrap FuncCall expressions
    """

    def __init__(self, expr):
        assert isinstance(expr, FuncCall), expr
        self.expr = expr

    def __repr__(self):
        return f"FuncCallStmt({self.expr})"
