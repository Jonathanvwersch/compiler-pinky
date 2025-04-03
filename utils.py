from model import (
    Assignment,
    BinOp,
    Float,
    ForStmt,
    FuncCall,
    FuncCallStmt,
    FuncDecl,
    Grouping,
    Identifier,
    IfStmt,
    Integer,
    LocalAssignment,
    LogicalOp,
    Param,
    PrintStmt,
    RetStmt,
    Stmts,
    String,
    UnOp,
    WhileStmt,
)


def pretty_print_ast(node, prefix="", is_root=True, is_last=True):
    """
    Pretty-print the AST with tree-like prefixes.

    :param node: The AST node to print.
    :param prefix: The current prefix string based on nesting level.
    :param is_root: Whether this node is the root of the print call.
    :param is_last: Whether this node is the last child at its level.
    :return: None
    """
    if not node:
        return

    # --- Helper for prefix formatting ---
    # If this node is the root, we keep the exact 'prefix' for children.
    # If this node is last, children get '    ', else children get '│   '
    def get_child_prefix(curr_prefix, is_root_node, is_last_node):
        if is_root_node:
            return curr_prefix
        elif is_last_node:
            return curr_prefix + "    "
        else:
            return curr_prefix + "│   "

    # --- Standard label printing: node header line ---
    def print_label(label):
        if is_root:
            print(f"{prefix}{label}")
        elif is_last:
            print(f"{prefix}└── {label}")
        else:
            print(f"{prefix}├── {label}")

    # BinOp / LogicalOp / etc. share some similar structure, so we handle them first.
    if isinstance(node, BinOp):
        print_label(f"BinOp({node.op.lexeme})")
        child_prefix = get_child_prefix(prefix, is_root, is_last)
        pretty_print_ast(node.left, child_prefix, False, False)
        pretty_print_ast(node.right, child_prefix, False, True)
        return

    elif isinstance(node, UnOp):
        print_label(f"UnOp({node.op.lexeme})")
        child_prefix = get_child_prefix(prefix, is_root, is_last)
        pretty_print_ast(node.operand, child_prefix, False, True)
        return

    elif isinstance(node, Grouping):
        print_label("Grouping")
        child_prefix = get_child_prefix(prefix, is_root, is_last)
        pretty_print_ast(node.value, child_prefix, False, True)
        return

    elif isinstance(node, LogicalOp):
        print_label(f"LogicalOp({node.op.lexeme})")
        child_prefix = get_child_prefix(prefix, is_root, is_last)
        pretty_print_ast(node.left, child_prefix, False, False)
        pretty_print_ast(node.right, child_prefix, False, True)
        return

    elif isinstance(node, Integer):
        print_label(f"Integer({node.value})")
        return

    elif isinstance(node, Float):
        print_label(f"Float({node.value})")
        return

    elif isinstance(node, String):
        print_label(f"String({repr(node.value)})")
        return

    elif isinstance(node, Identifier):
        print_label(f"Identifier({node.name})")
        return

    elif isinstance(node, Param):
        print_label(f"Param({node.name})")
        return

    elif isinstance(node, FuncCall):
        # Example format: FuncCall('myFunc', [arg1, arg2])
        print_label(f"FuncCall({repr(node.name)})")
        child_prefix = get_child_prefix(prefix, is_root, is_last)
        if not node.args:
            return
        for i, arg in enumerate(node.args):
            is_arg_last = i == len(node.args) - 1
            pretty_print_ast(arg, child_prefix, False, is_arg_last)
        return

    elif isinstance(node, Assignment):
        # We label the assignment, then print the name and value parts
        print_label("Assignment")
        child_prefix = get_child_prefix(prefix, is_root, is_last)

        # Left side
        print(f"{child_prefix}├── Name:")
        pretty_print_ast(node.left, child_prefix + "│   ", False, True)

        # Right side
        print(f"{child_prefix}└── Value:")
        pretty_print_ast(node.right, child_prefix + "    ", False, True)
        return

    elif isinstance(node, PrintStmt):
        # We'll show 'PrintStmt' or 'PrintStmt end="\n"' based on the node
        print_label("PrintStmt")
        child_prefix = get_child_prefix(prefix, is_root, is_last)

        # The expression to print
        pretty_print_ast(node.value, child_prefix, False, True)
        return

    elif isinstance(node, LocalAssignment):
        print_label(f"LocalAssignment")
        child_prefix = get_child_prefix(prefix, is_root, is_last)
        pretty_print_ast(node.left, child_prefix, False, False)
        pretty_print_ast(node.right, child_prefix, False, True)
        return

    elif isinstance(node, RetStmt):
        print_label("RetStmt")
        child_prefix = get_child_prefix(prefix, is_root, is_last)

        # The expression to print
        pretty_print_ast(node.value, child_prefix, False, True)
        return

    elif isinstance(node, IfStmt):
        print_label("IfStmt")
        child_prefix = get_child_prefix(prefix, is_root, is_last)

        # Condition
        print(f"{child_prefix}├── Condition:")
        pretty_print_ast(node.test, child_prefix + "│   ", False, True)

        # Then branch
        print(f"{child_prefix}├── Then:")
        if isinstance(node.then_stmts, Stmts):
            for i, stmt in enumerate(node.then_stmts.stmts):
                is_last_stmt = i == len(node.then_stmts.stmts) - 1
                pretty_print_ast(stmt, child_prefix + "│   ", False, is_last_stmt)
        else:
            pretty_print_ast(node.then_stmts, child_prefix + "│   ", False, True)

        # Else branch
        print(f"{child_prefix}└── Else:")
        if isinstance(node.else_stmts, Stmts):
            for i, stmt in enumerate(node.else_stmts.stmts):
                is_last_stmt = i == len(node.else_stmts.stmts) - 1
                pretty_print_ast(stmt, child_prefix + "    ", False, is_last_stmt)
        else:
            pretty_print_ast(node.else_stmts, child_prefix + "    ", False, True)
        return

    elif isinstance(node, ForStmt):
        print_label("ForStmt")
        child_prefix = get_child_prefix(prefix, is_root, is_last)

        # Initialization: var name, start, end
        print(f"{child_prefix}├── Initialization:")
        pretty_print_ast(node.identifier, child_prefix + "│   ", False, True)
        pretty_print_ast(node.start, child_prefix + "│   ", False, True)
        pretty_print_ast(node.end, child_prefix + "│   ", False, True)

        # Increment
        print(f"{child_prefix}├── Increment:")
        pretty_print_ast(node.step, child_prefix + "│   ", False, True)

        # Body
        print(f"{child_prefix}└── Do:")
        if isinstance(node.for_stmts, Stmts):
            for i, stmt in enumerate(node.for_stmts.stmts):
                is_last_stmt = i == len(node.for_stmts.stmts) - 1
                pretty_print_ast(stmt, child_prefix + "    ", False, is_last_stmt)
        else:
            pretty_print_ast(node.for_stmts, child_prefix + "    ", False, True)
        return

    elif isinstance(node, WhileStmt):
        print_label("WhileStmt")
        child_prefix = get_child_prefix(prefix, is_root, is_last)

        # Condition
        print(f"{child_prefix}├── Condition:")
        pretty_print_ast(node.test, child_prefix + "│   ", False, True)

        # Body
        print(f"{child_prefix}└── Do:")
        if isinstance(node.while_stmts, Stmts):
            for i, stmt in enumerate(node.while_stmts.stmts):
                is_last_stmt = i == len(node.while_stmts.stmts) - 1
                pretty_print_ast(stmt, child_prefix + "    ", False, is_last_stmt)
        else:
            pretty_print_ast(node.while_stmts, child_prefix + "    ", False, True)
        return

    elif isinstance(node, FuncCallStmt):
        print_label("FuncCallStmt")
        child_prefix = get_child_prefix(prefix, is_root, is_last)
        print(f"{child_prefix}└──")
        pretty_print_ast(node.expr, child_prefix + "    ")
        return

    elif isinstance(node, FuncDecl):
        # Print function declaration: name, params, body
        print_label("FuncDecl")
        child_prefix = get_child_prefix(prefix, is_root, is_last)

        # Name
        print(f"{child_prefix}├── Name: {node.name}")

        # Params
        print(f"{child_prefix}├── Params:")
        for i, param in enumerate(node.params):
            is_last_param = i == len(node.params) - 1
            pretty_print_ast(param, child_prefix + "│   ", False, is_last_param)

        # Body
        print(f"{child_prefix}└── Body:")
        if isinstance(node.body_stmts, Stmts):
            for i, stmt in enumerate(node.body_stmts.stmts):
                is_last_stmt = i == len(node.body_stmts.stmts) - 1
                pretty_print_ast(stmt, child_prefix + "    ", False, is_last_stmt)
        else:
            pretty_print_ast(node.body_stmts, child_prefix + "    ", False, True)
        return

    elif isinstance(node, Stmts):
        # For a list of statements, print each child.
        for i, stmt in enumerate(node.stmts):
            is_last_stmt = i == len(node.stmts) - 1
            pretty_print_ast(stmt, prefix, is_root, is_last_stmt)
        return

    print_label("? (Unknown Node)")


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


def vm_error(message, pc):
    print(f"{Colors.RED}[PC {pc}]: {message}{Colors.WHITE}")


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
