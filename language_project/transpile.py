#!/usr/bin/env python3
"""
Script to transpile programs written in our custom language to Python.
"""

import os
import sys
import argparse
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.transpiler import Transpiler

def transpile_program(input_file, output_file):
    """
    Transpile a program from our custom language to Python.
    
    Args:
        input_file (str): Path to the input file in our language
        output_file (str): Path to the output Python file
    """
    print(f"Transpiling {input_file} to {output_file}")
    
    # Read the source code
    try:
        with open(input_file, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {input_file}")
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
        
        # Transpile the AST to Python
        transpiler = Transpiler()
        python_code = transpiler.transpile(ast)
        
        # Check if we need to import math (for factorial operations)
        needs_math = 'math.factorial' in python_code
        
        # Write the Python code to the output file
        with open(output_file, 'w') as f:
            f.write("# This file was automatically generated from {}\n".format(os.path.basename(input_file)))
            f.write("# by the language transpiler\n\n")
            if needs_math:
                f.write("import math\n\n")
            f.write(python_code)
        
        print(f"Successfully transpiled to {output_file}")
        
    except Exception as e:
        print(f"Error transpiling program: {e}")
        return

def main():
    parser = argparse.ArgumentParser(description='Transpile programs from our custom language to Python')
    parser.add_argument('input_file', help='Path to the input source code file')
    parser.add_argument('output_file', help='Path to the output Python file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output (AST)')
    
    global args
    args = parser.parse_args()
    
    transpile_program(args.input_file, args.output_file)

if __name__ == '__main__':
    main()