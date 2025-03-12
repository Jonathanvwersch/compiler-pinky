from model import (
    BinOp,
    Float,
    Grouping,
    Integer,
    LogicalOp,
    PrintStmt,
    Stmts,
    String,
    UnOp,
)


def pretty_print_ast(node, prefix="", is_root=True, is_last=True):
    if not node:
        return

    if isinstance(node, BinOp):
        node_str = f"BinOp({node.op.lexeme})"
        left, right = node.left, node.right
    elif isinstance(node, UnOp):
        node_str = f"UnOp({node.op.lexeme})"
        left, right = node.operand, None
    elif isinstance(node, Grouping):
        node_str = "Grouping"
        left, right = node.value, None
    elif isinstance(node, LogicalOp):
        node_str = f"LogicalOp({node.op.lexeme})"
        left, right = node.left, node.right
    elif isinstance(node, Integer):
        node_str = f"Integer({node.value})"
        left = right = None
    elif isinstance(node, Float):
        node_str = f"Float({node.value})"
        left = right = None
    elif isinstance(node, String):
        node_str = f"String({repr(node.value)})"
        left = right = None
    elif isinstance(node, Stmts):
        for stmt in node.stmts:
            pretty_print_ast(stmt)
        return  # No need to print anything at this level
    elif isinstance(node, PrintStmt):
        print("PrintStmt")
        pretty_print_ast(node.value, prefix + "    ", False, True)
        return
    else:
        node_str = "?"
        left = right = None

    if is_root:
        print(f"{prefix}{node_str}")
    elif is_last:
        print(f"{prefix}└── {node_str}")
    else:
        print(f"{prefix}├── {node_str}")

    if is_root:
        child_prefix = prefix
    elif is_last:
        child_prefix = prefix + "    "
    else:
        child_prefix = prefix + "│   "

    if isinstance(node, (LogicalOp, BinOp)):
        pretty_print_ast(left, child_prefix, False, False)
        pretty_print_ast(right, child_prefix, False, True)
    elif isinstance(node, (UnOp, Grouping)):
        pretty_print_ast(left, child_prefix, False, True)


def parse_error(message, line_num):
    print(f"{Colors.RED}[Line {line_num}]: {message}{Colors.WHITE}")
    import sys

    sys.exit(1)


def lexing_error(message, line_num):
    print(f"{Colors.RED}[Line {line_num}]: {message}{Colors.WHITE}")
    import sys

    sys.exit(1)


def runtime_error(message, line_num):
    print(f"{Colors.RED}[Line {line_num}]: {message}{Colors.WHITE}")


class Colors:
    WHITE = "\033[0m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
