import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter import Interpreter

def main():
    source_code = "x = 42 + (5 * 3) - 7 / 2"
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    print("Tokens:", tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)

    interpreter = Interpreter()
    for node in ast:
        result = interpreter.evaluate(node)
        print("Result:", result)

if __name__ == "__main__":
    main()