import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter import Interpreter

def main():
    # Test 1: If-else statement
    print("\n========== TEST 1: IF-ELSE STATEMENT ==========")
    source_code = "if x == 42: x = x + 1 else: x = x - 1"
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    print("Tokens:", tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)

    interpreter = Interpreter()
    # Set initial value for x
    interpreter.variables['x'] = 42
    print("Initial state:", interpreter.variables)
    
    for node in ast:
        result = interpreter.evaluate(node)
        print("Result:", result)
        print("Final state:", interpreter.variables)
        
    # Test 2: While loop
    print("\n========== TEST 2: WHILE LOOP ==========")
    source_code = "i = 1 while i <= 5: i = i + 1"
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    print("Tokens:", tokens)
    
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)
    
    interpreter = Interpreter()
    print("Initial state:", interpreter.variables)
    
    for node in ast:
        result = interpreter.evaluate(node)
        print("Result:", result)
        print("Final state:", interpreter.variables)
        
    # Test 3: Function definition and call
    print("\n========== TEST 3: FUNCTION DEFINITION AND CALL ==========")
    # Define function first
    source_code = "def factorial(n): if n <= 1: return 1 else: return n * factorial(n - 1)"
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    print("Function Definition Tokens:", tokens)
    
    parser = Parser(tokens)
    ast = parser.parse()
    print("Function Definition AST:", ast)
    
    interpreter = Interpreter()
    print("Initial state:", interpreter.variables)
    
    # Evaluate function definition
    for node in ast:
        result = interpreter.evaluate(node)
        print("Function Definition Result:", result)
    
    # Now call the function
    source_code = "result = factorial(5)"
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    print("Function Call Tokens:", tokens)
    
    parser = Parser(tokens)
    ast = parser.parse()
    print("Function Call AST:", ast)
    
    # Evaluate function call
    for node in ast:
        result = interpreter.evaluate(node)
        print("Function Call Result:", result)
    
    print("Final state:", interpreter.variables)

if __name__ == "__main__":
    main()