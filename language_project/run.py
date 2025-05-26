#!/usr/bin/env python3
"""
Script to run programs written in our custom language using the interpreter.
"""

import os
import sys
import argparse
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter import Interpreter

def run_program(file_path):
    """
    Run a program written in our custom language.
    
    Args:
        file_path (str): Path to the source code file
    """
    print(f"Running program: {file_path}")
    
    # Read the source code
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    try:
        # Create tokens
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        # Parse the tokens into an AST
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Print the AST if verbose output is enabled
        if args.verbose:
            print("\nAbstract Syntax Tree (AST):")
            import json
            print(json.dumps(ast, indent=2))
        
        # Execute the program
        interpreter = Interpreter()
        for node in ast:
            interpreter.evaluate(node)
        
        # Print the final state of variables
        print("\nFinal variable values:")
        for var_name, var_value in interpreter.variables.items():
            print(f"{var_name} = {var_value}")
        
    except Exception as e:
        print(f"Error executing program: {e}")
        return

def main():
    parser = argparse.ArgumentParser(description='Run programs written in our custom language')
    parser.add_argument('file', help='Path to the source code file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output (AST)')
    
    global args
    args = parser.parse_args()
    
    run_program(args.file)

if __name__ == '__main__':
    main()