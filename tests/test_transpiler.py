import sys
import os
import unittest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.transpiler import Transpiler

class TestTranspiler(unittest.TestCase):
    def _transpile(self, source_code):
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        transpiler = Transpiler()
        python_code = transpiler.transpile(ast)
        
        return python_code
    
    def test_assignment(self):
        code = "x = 42"
        result = self._transpile(code)
        self.assertEqual(result, "x = 42")
    
    def test_arithmetic(self):
        code = "result = 2 + 3 * 4"
        result = self._transpile(code)
        self.assertEqual(result, "result = (2 + (3 * 4))")
    
    def test_if_statement(self):
        code = "if x > 10: y = 1"
        result = self._transpile(code)
        expected = "if (x > 10):\n    y = 1"
        self.assertEqual(result, expected)
    
    def test_if_else_statement(self):
        code = "if x > 0: y = 1 else: y = 0"
        result = self._transpile(code)
        expected = "if (x > 0):\n    y = 1\nelse:\n    y = 0"
        self.assertEqual(result, expected)
    
    def test_while_loop(self):
        code = "i = 1; while i <= 5: sum = sum + i; i = i + 1"
        result = self._transpile(code)
        expected = "i = 1\nwhile (i <= 5):\n    sum = (sum + i)\n    i = (i + 1)"
        self.assertEqual(result, expected)
    
    def test_function_definition(self):
        code = "def add(a, b): return a + b"
        result = self._transpile(code)
        expected = "def add(a, b):\n    return (a + b)"
        self.assertEqual(result, expected)
    
    def test_function_call(self):
        code = "result = add(2, 3)"
        result = self._transpile(code)
        self.assertEqual(result, "result = add(2, 3)")
    
    def test_recursive_function(self):
        code = "def factorial(n): if n <= 1: return 1 else: return n * factorial(n - 1)"
        result = self._transpile(code)
        expected = "def factorial(n):\n    if (n <= 1):\n        return 1\n    else:\n        return (n * factorial((n - 1)))"
        self.assertEqual(result, expected)
    
    def test_complex_program(self):
        code = """def fibonacci(n): if n <= 1: return n else: return fibonacci(n - 1) + fibonacci(n - 2) result = fibonacci(10)"""
        result = self._transpile(code)
        expected = "def fibonacci(n):\n    if (n <= 1):\n        return n\n    else:\n        return (fibonacci((n - 1)) + fibonacci((n - 2)))\nresult = fibonacci(10)"
        self.assertEqual(result.strip(), expected.strip())

if __name__ == '__main__':
    unittest.main()