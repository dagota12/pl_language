import sys
import os
import unittest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.lexer import Lexer

class TestLexer(unittest.TestCase):
    def test_arithmetic_operators(self):
        source_code = "2 + 3 - 4 * 5 / 6"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        expected_tokens = [
            ('NUMBER', '2'),
            ('PLUS', '+'),
            ('NUMBER', '3'),
            ('MINUS', '-'),
            ('NUMBER', '4'),
            ('MULTIPLY', '*'),
            ('NUMBER', '5'),
            ('DIVIDE', '/'),
            ('NUMBER', '6')
        ]
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_comparison_operators(self):
        source_code = "x == y != z < a <= b > c >= d"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        expected_tokens = [
            ('IDENTIFIER', 'x'),
            ('EQUALS', '=='),
            ('IDENTIFIER', 'y'),
            ('NOT_EQUALS', '!='),
            ('IDENTIFIER', 'z'),
            ('LESS', '<'),
            ('IDENTIFIER', 'a'),
            ('LESS_EQUALS', '<='),
            ('IDENTIFIER', 'b'),
            ('GREATER', '>'),
            ('IDENTIFIER', 'c'),
            ('GREATER_EQUALS', '>='),
            ('IDENTIFIER', 'd')
        ]
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_keywords(self):
        source_code = "if else while def return"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        expected_tokens = [
            ('IF', 'if'),
            ('ELSE', 'else'),
            ('WHILE', 'while'),
            ('DEF', 'def'),
            ('RETURN', 'return')
        ]
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_assignment(self):
        source_code = "x = 42"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        expected_tokens = [
            ('IDENTIFIER', 'x'),
            ('ASSIGN', '='),
            ('NUMBER', '42')
        ]
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_function_definition(self):
        source_code = "def add(a, b): return a + b"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        expected_tokens = [
            ('DEF', 'def'),
            ('IDENTIFIER', 'add'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'a'),
            ('COMMA', ','),
            ('IDENTIFIER', 'b'),
            ('RPAREN', ')'),
            ('COLON', ':'),
            ('RETURN', 'return'),
            ('IDENTIFIER', 'a'),
            ('PLUS', '+'),
            ('IDENTIFIER', 'b')
        ]
        
        self.assertEqual(tokens, expected_tokens)

if __name__ == '__main__':
    unittest.main()