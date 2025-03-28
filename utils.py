from model import (
    Assignment,
    BinOp,
    Float,
    ForStmt,
    Grouping,
    Identifier,
    IfStmt,
    Integer,
    LogicalOp,
    PrintStmt,
    Stmts,
    String,
    UnOp,
    WhileStmt,
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
    elif isinstance(node, Assignment):
        if is_root:
            print(f"{prefix}Assignment")
        elif is_last:
            print(f"{prefix}└── Assignment")
        else:
            print(f"{prefix}├── Assignment")

        if is_root:
            child_prefix = prefix
        elif is_last:
            child_prefix = prefix + "    "
        else:
            child_prefix = prefix + "│   "

        # Print left (identifier) and right (value) parts of assignment
        print(f"{child_prefix}├── Name:")
        pretty_print_ast(node.left, child_prefix + "│   ", False, True)

        print(f"{child_prefix}└── Value:")
        pretty_print_ast(node.right, child_prefix + "    ", False, True)

        return  # Add return to prevent fallthrough
    elif isinstance(node, Identifier):
        node_str = f"Identifier({node.name})"  # Assuming name is the attribute to print
        left = right = None
    elif isinstance(node, IfStmt):
        if is_root:
            print(f"{prefix}IfStmt")
        elif is_last:
            print(f"{prefix}└── IfStmt")
        else:
            print(f"{prefix}├── IfStmt")

        if is_root:
            child_prefix = prefix
        elif is_last:
            child_prefix = prefix + "    "
        else:
            child_prefix = prefix + "│   "

        print(f"{child_prefix}├── Condition:")
        pretty_print_ast(node.test, child_prefix + "│   ", False, True)

        print(f"{child_prefix}├── Then:")
        if isinstance(node.then_stmts, Stmts):
            then_stmts_prefix = child_prefix + "│   "
            for i, stmt in enumerate(node.then_stmts.stmts):
                is_last_stmt = i == len(node.then_stmts.stmts) - 1
                pretty_print_ast(stmt, then_stmts_prefix, False, is_last_stmt)
        else:
            pretty_print_ast(node.then_stmts, child_prefix + "│   ", False, True)

        print(f"{child_prefix}└── Else:")
        if isinstance(node.else_stmts, Stmts):
            else_stmts_prefix = child_prefix + "    "
            for i, stmt in enumerate(node.else_stmts.stmts):
                is_last_stmt = i == len(node.else_stmts.stmts) - 1
                pretty_print_ast(stmt, else_stmts_prefix, False, is_last_stmt)
        else:
            pretty_print_ast(node.else_stmts, child_prefix + "    ", False, True)

        return

    elif isinstance(node, ForStmt):
        if is_root:
            print(f"{prefix}ForStmt")
        elif is_last:
            print(f"{prefix}└── ForStmt")
        else:
            print(f"{prefix}├── ForStmt")

        if is_root:
            child_prefix = prefix
        elif is_last:
            child_prefix = prefix + "    "
        else:
            child_prefix = prefix + "│   "

        print(f"{child_prefix}├── Initialization:")
        pretty_print_ast(node.identifier, child_prefix + "│   ", False, True)
        pretty_print_ast(node.start, child_prefix + "│   ", False, True)
        pretty_print_ast(node.end, child_prefix + "│   ", False, True)

        print(f"{child_prefix}├── Increment:")
        pretty_print_ast(node.step, child_prefix + "│   ", False, True)

        print(f"{child_prefix}└── Do:")
        if isinstance(node.for_stmts, Stmts):
            for i, stmt in enumerate(node.for_stmts.stmts):
                is_last_stmt = i == len(node.for_stmts.stmts) - 1
                pretty_print_ast(stmt, child_prefix + "    ", False, is_last_stmt)
        else:
            pretty_print_ast(node.for_stmts, child_prefix + "    ", False, True)

        return

    elif isinstance(node, WhileStmt):
        if is_root:
            print(f"{prefix}WhileStmt")
        elif is_last:
            print(f"{prefix}└── WhileStmt")
        else:
            print(f"{prefix}├── WhileStmt")

        if is_root:
            child_prefix = prefix
        elif is_last:
            child_prefix = prefix + "    "
        else:
            child_prefix = prefix + "│   "

        print(f"{child_prefix}├── Condition:")
        pretty_print_ast(node.test, child_prefix + "│   ", False, True)

        print(f"{child_prefix}└── Do:")

        if isinstance(node.while_stmts, Stmts):
            for i, stmt in enumerate(node.while_stmts.stmts):
                is_last_stmt = i == len(node.while_stmts.stmts) - 1
                pretty_print_ast(stmt, child_prefix + "    ", False, is_last_stmt)
        else:
            pretty_print_ast(node.while_stmts, child_prefix + "    ", False, True)

        return

    elif isinstance(node, Float):
        node_str = f"Float({node.value})"
        left = right = None
    elif isinstance(node, String):
        node_str = f"String({repr(node.value)})"
        left = right = None
    elif isinstance(node, Stmts):
        for i, stmt in enumerate(node.stmts):
            is_last_stmt = i == len(node.stmts) - 1
            pretty_print_ast(stmt, prefix, is_root, is_last_stmt)
        return
    elif isinstance(node, PrintStmt):
        if is_root:
            print(f"{prefix}PrintStmt")
        elif is_last:
            print(f"{prefix}└── PrintStmt")
        else:
            print(f"{prefix}├── PrintStmt")

        if is_root:
            child_prefix = prefix
        elif is_last:
            child_prefix = prefix + "    "
        else:
            child_prefix = prefix + "│   "

        pretty_print_ast(node.value, child_prefix, False, True)
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


def stringify(val):
    if isinstance(val, bool):
        return "true" if val == True else False
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val)


class Colors:
    WHITE = "\033[0m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
