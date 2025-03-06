from model import BinOp, Float, Grouping, Integer, UnOp


def pretty_print_ast(node, prefix="", is_root=True, is_last=True):
    if not node:
        return

    if isinstance(node, BinOp):
        node_str = node.op.lexeme
        left, right = node.left, node.right
    elif isinstance(node, UnOp):
        node_str = node.op.lexeme
        left, right = node.operand, None
    elif isinstance(node, Grouping):
        node_str = "(group)"
        left, right = node.value, None
    elif isinstance(node, (Integer, Float)):
        node_str = str(node.value)
        left = right = None
    else:
        node_str = "?"
        left = right = None

    if is_root:
        print(f"{prefix}{node_str}")
    elif is_last:
        print(f"{prefix}{'└── '}{node_str}")
    else:
        print(f"{prefix}{'├── '}{node_str}")

    if is_root:
        child_prefix = prefix
    elif is_last:
        child_prefix = prefix + "    "
    else:
        child_prefix = prefix + "│   "

    if isinstance(node, BinOp):
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
