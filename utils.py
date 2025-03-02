from model import BinOp, Float, Grouping, Integer, UnOp


def get_tree_lines(node, level=0):
    if not node:
        return []

    if isinstance(node, BinOp):
        node_str = node.op.lexeme
    elif isinstance(node, UnOp):
        node_str = node.op.lexeme
    elif isinstance(node, Grouping):
        node_str = "(group)"
    elif isinstance(node, (Integer, Float)):
        node_str = node.value
    else:
        node_str = "?"

    ## get left and right trees (recursively)
    left = (
        get_tree_lines(
            node.left,
            level + 1,
        )
        if isinstance(node, BinOp)
        else []
    )
    right = get_tree_lines(node.right, level + 1) if isinstance(node, BinOp) else []

    body = []

    if left and right:
        body = left + right
        print("body", body)

    return [node_str] + body


def pretty_print_ast(ast_text):
    lines = get_tree_lines(ast_text)

    for line in lines:
        print(line)
