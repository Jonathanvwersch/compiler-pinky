import sys
from parser import Parser
from tokens import *
from lexer import *
from utils import Colors, pretty_print_ast

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 pinky.py <filename>")

    filename = sys.argv[1]
    with open(filename) as file:
        source = file.read()

        print(f"{Colors.GREEN}**************************************")
        print(f"{Colors.GREEN}SOURCE:{Colors.WHITE}")
        print(f"{Colors.GREEN}**************************************{Colors.WHITE}")
        print("")

        print(source)

        print("")
        print(f"{Colors.GREEN}**************************************")
        print(f"{Colors.GREEN}TOKENS:{Colors.WHITE}")
        print(f"{Colors.GREEN}**************************************{Colors.WHITE}")

        tokens = Lexer(source).tokenize()
        for token in tokens:
            print(token)

        print("")
        print(f"{Colors.GREEN}**************************************")
        print(f"{Colors.GREEN}AST:{Colors.WHITE}")
        print(f"{Colors.GREEN}**************************************{Colors.WHITE}")
        ast = Parser(tokens).parse()
        pretty_print_ast(ast)
