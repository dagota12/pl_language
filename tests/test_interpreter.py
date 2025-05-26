import sys
import os
import unittest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    def _interpret(self, source_code, initial_vars=None):
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        if initial_vars:
            interpreter.variables = initial_vars
        
        results = []
        for node in ast:
            result = interpreter.evaluate(node)
            results.append(result)
        
        return results, interpreter.variables
    
    def test_arithmetic(self):
        results, variables = self._interpret("2 + 3 * 4")
        self.assertEqual(results[0], 14)
    
    def test_variables(self):
        results, variables = self._interpret("x = 5 y = 10 z = x + y")
        self.assertEqual(variables['x'], 5)
        self.assertEqual(variables['y'], 10)
        self.assertEqual(variables['z'], 15)
    
    def test_if_true(self):
        results, variables = self._interpret("x = 10 if x > 5: y = 1", {'x': 10})
        self.assertEqual(variables['y'], 1)
    
    def test_if_false(self):
        results, variables = self._interpret("x = 3 if x > 5: y = 1", {'x': 3})
        self.assertNotIn('y', variables)
    
    def test_if_else(self):
        results, variables = self._interpret("if x > 5: y = 1 else: y = 0", {'x': 3})
        self.assertEqual(variables['y'], 0)
        
        results, variables = self._interpret("if x > 5: y = 1 else: y = 0", {'x': 10})
        self.assertEqual(variables['y'], 1)
    
    def test_while_loop(self):
        # Using semicolons to include multiple statements in the while loop body
        source_code = "i = 1; sum = 0; while i <= 5: sum = sum + i; i = i + 1"
        results, variables = self._interpret(source_code)
        # Sum of 1 + 2 + 3 + 4 + 5 = 15
        self.assertEqual(variables['sum'], 15)
        self.assertEqual(variables['i'], 6)
    
    def test_simple_function(self):
        source_code = "def add(a, b): return a + b result = add(2, 3)"
        results, variables = self._interpret(source_code)
        self.assertEqual(variables['result'], 5)
    
    def test_recursive_function(self):
        source_code = "def factorial(n): if n <= 1: return 1 else: return n * factorial(n - 1) result = factorial(5)"
        results, variables = self._interpret(source_code)
        self.assertEqual(variables['result'], 120)  # 5! = 5 * 4 * 3 * 2 * 1 = 120
    
    def test_nested_function_calls(self):
        source_code = """
        def add(a, b): return a + b
        def multiply(a, b): return a * b
        result = add(multiply(2, 3), multiply(4, 5))
        """
        results, variables = self._interpret(source_code)
        # add(2*3, 4*5) = add(6, 20) = 26
        self.assertEqual(variables['result'], 26)
    
    def test_function_with_variables(self):
        source_code = """
        x = 10
        def addX(a): return a + x
        result = addX(5)
        """
        results, variables = self._interpret(source_code)
        self.assertEqual(variables['result'], 15)

if __name__ == '__main__':
    unittest.main()