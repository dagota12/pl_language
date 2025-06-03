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

    def test_amharic_keywords(self):
        # Test Amharic IF keyword
        source_code = "ከሆነ x == 42: y = 1"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        expected_tokens = [
            ('IF', 'ከሆነ'),
            ('IDENTIFIER', 'x'),
            ('EQUALS', '=='),
            ('NUMBER', '42'),
            ('COLON', ':'),
            ('IDENTIFIER', 'y'),
            ('ASSIGN', '='),
            ('NUMBER', '1')
        ]
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_amharic_multi_word_keyword(self):
        # Test multi-word Amharic WHILE keyword
        source_code = "እስከሆነ ድረስ i < 10: i = i + 1"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        expected_tokens = [
            ('WHILE', 'እስከሆነ ድረስ'),
            ('IDENTIFIER', 'i'),
            ('LESS', '<'),
            ('NUMBER', '10'),
            ('COLON', ':'),
            ('IDENTIFIER', 'i'),
            ('ASSIGN', '='),
            ('IDENTIFIER', 'i'),
            ('PLUS', '+'),
            ('NUMBER', '1')
        ]
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_amharic_print_function(self):
        # Test Amharic print function
        source_code = "አውጣ(42)"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        expected_tokens = [
            ('PRINT', 'አውጣ'),
            ('LPAREN', '('),
            ('NUMBER', '42'),
            ('RPAREN', ')')
        ]
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_amharic_assignment(self):
        # Test Amharic assignment keyword
        source_code = "x ይሁን 42"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        expected_tokens = [
            ('IDENTIFIER', 'x'),
            ('ASSIGN_KW', 'ይሁን'),
            ('NUMBER', '42')
        ]
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_amharic_logical_operators(self):
        # Test Amharic logical operators
        source_code = "x እና y ወይም z"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        expected_tokens = [
            ('IDENTIFIER', 'x'),
            ('AND', 'እና'),
            ('IDENTIFIER', 'y'),
            ('OR', 'ወይም'),
            ('IDENTIFIER', 'z')
        ]
        
        self.assertEqual(tokens, expected_tokens)

if __name__ == '__main__':
    unittest.main()