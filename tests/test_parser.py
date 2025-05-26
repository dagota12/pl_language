import sys
import os
import unittest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser

class TestParser(unittest.TestCase):
    def test_arithmetic_expression(self):
        source_code = "2 + 3 * 4"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Expected: 2 + (3 * 4) due to operator precedence
        expected_ast = [{
            'type': 'BinaryOperation',
            'operator': '+',
            'left': {'type': 'Number', 'value': '2'},
            'right': {
                'type': 'BinaryOperation',
                'operator': '*',
                'left': {'type': 'Number', 'value': '3'},
                'right': {'type': 'Number', 'value': '4'}
            }
        }]
        
        self.assertEqual(ast, expected_ast)
    
    def test_assignment(self):
        source_code = "x = 42"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        expected_ast = [{
            'type': 'Assignment',
            'identifier': 'x',
            'value': {'type': 'Number', 'value': '42'}
        }]
        
        self.assertEqual(ast, expected_ast)
    
    def test_if_statement(self):
        source_code = "if x == 42: y = 1"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        expected_ast = [{
            'type': 'IfStatement',
            'condition': {
                'type': 'Comparison',
                'operator': '==',
                'left': {'type': 'Identifier', 'value': 'x'},
                'right': {'type': 'Number', 'value': '42'}
            },
            'true_branch': {
                'type': 'Block',
                'statements': [
                    {
                        'type': 'Assignment',
                        'identifier': 'y',
                        'value': {'type': 'Number', 'value': '1'}
                    }
                ]
            },
            'false_branch': None
        }]
        
        self.assertEqual(ast, expected_ast)
    
    def test_if_else_statement(self):
        source_code = "if x > 0: y = 1 else: y = 0"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        expected_ast = [{
            'type': 'IfStatement',
            'condition': {
                'type': 'Comparison',
                'operator': '>',
                'left': {'type': 'Identifier', 'value': 'x'},
                'right': {'type': 'Number', 'value': '0'}
            },
            'true_branch': {
                'type': 'Block',
                'statements': [
                    {
                        'type': 'Assignment',
                        'identifier': 'y',
                        'value': {'type': 'Number', 'value': '1'}
                    }
                ]
            },
            'false_branch': {
                'type': 'Block',
                'statements': [
                    {
                        'type': 'Assignment',
                        'identifier': 'y',
                        'value': {'type': 'Number', 'value': '0'}
                    }
                ]
            }
        }]
        
        self.assertEqual(ast, expected_ast)
    
    def test_while_loop(self):
        source_code = "while i < 10: i = i + 1"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        expected_ast = [{
            'type': 'WhileStatement',
            'condition': {
                'type': 'Comparison',
                'operator': '<',
                'left': {'type': 'Identifier', 'value': 'i'},
                'right': {'type': 'Number', 'value': '10'}
            },
            'body': {
                'type': 'Block',
                'statements': [
                    {
                        'type': 'Assignment',
                        'identifier': 'i',
                        'value': {
                            'type': 'BinaryOperation',
                            'operator': '+',
                            'left': {'type': 'Identifier', 'value': 'i'},
                            'right': {'type': 'Number', 'value': '1'}
                        }
                    }
                ]
            }
        }]
        
        self.assertEqual(ast, expected_ast)
    
    def test_function_definition(self):
        source_code = "def add(a, b): return a + b"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        expected_ast = [{
            'type': 'FunctionDefinition',
            'name': 'add',
            'parameters': ['a', 'b'],
            'body': {
                'type': 'Block',
                'statements': [
                    {
                        'type': 'ReturnStatement',
                        'value': {
                            'type': 'BinaryOperation',
                            'operator': '+',
                            'left': {'type': 'Identifier', 'value': 'a'},
                            'right': {'type': 'Identifier', 'value': 'b'}
                        }
                    }
                ]
            }
        }]
        
        self.assertEqual(ast, expected_ast)
    
    def test_function_call(self):
        source_code = "result = add(2, 3)"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        expected_ast = [{
            'type': 'Assignment',
            'identifier': 'result',
            'value': {
                'type': 'FunctionCall',
                'name': 'add',
                'arguments': [
                    {'type': 'Number', 'value': '2'},
                    {'type': 'Number', 'value': '3'}
                ]
            }
        }]
        
        self.assertEqual(ast, expected_ast)
    
    def test_spit_function(self):
        source_code = "spit(42)"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        expected_ast = [{
            'type': 'SpitFunction',
            'arguments': [
                {'type': 'Number', 'value': '42'}
            ]
        }]
        
        self.assertEqual(ast, expected_ast)

if __name__ == '__main__':
    unittest.main()