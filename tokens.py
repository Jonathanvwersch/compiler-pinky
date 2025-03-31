###############################################################################
# Constants for different token types
###############################################################################
# Single-char tokens
from enum import Enum


class TokenType(Enum):
    # Single-char tokens
    LPAREN = "("
    RPAREN = ")"
    LCURLY = "{"
    RCURLY = "}"
    LSQUAR = "["
    RSQUAR = "]"
    COMMA = ","
    DOT = "."
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    CARET = "^"
    MOD = "%"
    COLON = ":"
    SEMICOLON = ";"
    QUESTION = "?"
    NOT = "~"
    GT = ">"
    LT = "<"
    EQ = "="

    # Two-char tokens
    GE = ">="
    LE = "<="
    NE = "~="
    EQEQ = "=="
    ASSIGN = ":="
    GTGT = ">>"
    LTLT = "<<"

    # Literals
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"

    # Keywords
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    TRUE = "TRUE"
    FALSE = "FALSE"
    AND = "AND"
    OR = "OR"
    WHILE = "WHILE"
    DO = "DO"
    FOR = "FOR"
    FUNC = "FUNC"
    NULL = "NULL"
    END = "END"
    PRINT = "PRINT"
    PRINTLN = "PRINTLN"
    RET = "RET"
    LOCAL = "LOCAL"


keywords = {
    "if": TokenType.IF,
    "then": TokenType.THEN,
    "else": TokenType.ELSE,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "while": TokenType.WHILE,
    "do": TokenType.DO,
    "for": TokenType.FOR,
    "func": TokenType.FUNC,
    "null": TokenType.NULL,
    "end": TokenType.END,
    "print": TokenType.PRINT,
    "println": TokenType.PRINTLN,
    "ret": TokenType.RET,
    "local": TokenType.LOCAL,
}


class Token:
    def __init__(self, token_type, lexeme, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line

    def __repr__(self):
        return f"({self.token_type}, {self.lexeme!r}, {self.line})"
