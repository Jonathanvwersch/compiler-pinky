import unittest
from utils import *
from tokens import *
from lexer import *
from parser import *
from interpreter import *


class TestExpressions(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_number_primary(self):
        source = """7.7"""
        expected_output = (TYPE_NUMBER, 7.7)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_bool_primary(self):
        source = """false"""
        expected_output = (TYPE_BOOL, False)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_add(self):
        source = """2 + 2"""
        expected_output = (TYPE_NUMBER, 4)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_mul(self):
        source = """2 * 9"""
        expected_output = (TYPE_NUMBER, 18)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_div(self):
        source = """9 / 2"""
        expected_output = (TYPE_NUMBER, 4.5)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_precedence(self):
        source = """2 * 9 + 13"""
        expected_output = (TYPE_NUMBER, 31)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_unary_minus(self):
        source = """2 * 9 - -5"""
        expected_output = (TYPE_NUMBER, 23)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_caret(self):
        source = """2^3^3 - 1"""
        expected_output = (TYPE_NUMBER, 134217727)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_mod(self):
        source = """(2^3^3-1) % 2"""
        expected_output = (TYPE_NUMBER, 1)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_paren_1(self):
        source = """2 * (9 + 13) / 2"""
        expected_output = (TYPE_NUMBER, 22)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_paren_2(self):
        source = """2 * (9 + 13) + 2^2 + (((3 * 3) - 3) + 3.324) / 2.1"""
        expected_output = (TYPE_NUMBER, 52.44)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_paren_3(self):
        source = """14 / (12 / 2) / 2"""
        expected_output = (TYPE_NUMBER, 1.1666666666666667)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_bool_or(self):
        source = """true or false"""
        expected_output = (TYPE_BOOL, True)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_bool_or_and(self):
        source = """(44 >= 2) or false and 1 > 0"""
        expected_output = (TYPE_BOOL, True)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_not(self):
        source = """~(44 >= 2)"""
        expected_output = (TYPE_BOOL, False)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_noteq(self):
        source = """~(3 ~= 2)"""
        expected_output = (TYPE_BOOL, False)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)

    def test_eqeq(self):
        source = """(3 == 2 + 1)"""
        expected_output = (TYPE_BOOL, True)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter().interpret(ast)
        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
