import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter import Interpreter

def main():
    # Test a while loop with multiple statements in the block, using semicolons as separators
    source_code = "i = 1; sum = 0; while i <= 5: sum = sum + i; i = i + 1"
    
    print("Source code:", source_code)
    
    # Tokenize
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    print("\nTokens:", tokens)
    
    # Parse
    parser = Parser(tokens)
    ast = parser.parse()
    print("\nAST:", ast)
    
    # Interpret
    interpreter = Interpreter()
    print("\nInitial state:", interpreter.variables)
    
    # Execute each AST node
    print("\nExecution:")
    for i, node in enumerate(ast):
        print(f"Node {i}:", node)
        try:
            result = interpreter.evaluate(node)
            print(f"Result {i}:", result)
            print(f"Variables after node {i}:", interpreter.variables)
        except Exception as e:
            print(f"Error executing node {i}:", e)
    
    print("\nFinal state:", interpreter.variables)

if __name__ == "__main__":
    main()