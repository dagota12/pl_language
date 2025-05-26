#!/usr/bin/env python3
"""
Script to transpile all example programs from our language to Python.
This demonstrates the transpiler functionality by converting all example
programs in the examples/ directory to their Python equivalents.
"""

import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.transpiler import Transpiler

def transpile_file(input_file, output_file):
    """
    Transpile a file from our language to Python.
    
    Args:
        input_file (str): Path to the input file in our language
        output_file (str): Path to the output Python file
    """
    print(f"Transpiling {input_file} to {output_file}")
    
    # Read the source code
    with open(input_file, 'r') as f:
        source_code = f.read()
    
    # Create tokens
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    # Parse the tokens into an AST
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Transpile the AST to Python
    transpiler = Transpiler()
    python_code = transpiler.transpile(ast)
    
    # Write the Python code to the output file
    with open(output_file, 'w') as f:
        f.write("# This file was automatically generated from {}\n".format(os.path.basename(input_file)))
        f.write("# by the language transpiler\n\n")
        f.write(python_code)
    
    print(f"Successfully transpiled to {output_file}")

def main():
    # Get the directory containing the example programs
    examples_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'examples'))
    
    # Create the directory for the transpiled Python files if it doesn't exist
    python_dir = os.path.join(examples_dir, 'python')
    os.makedirs(python_dir, exist_ok=True)
    
    # Find all .lang files in the examples directory
    lang_files = Path(examples_dir).glob('*.lang')
    
    for lang_file in lang_files:
        # Create the output Python file path
        python_file = os.path.join(python_dir, f"{lang_file.stem}.py")
        
        # Transpile the file
        transpile_file(lang_file, python_file)

if __name__ == '__main__':
    main()