#!/usr/bin/env python3
"""
REPL (Read-Eval-Print-Loop) for our custom language.
This script provides an interactive environment to write and execute code in our language.
"""

import os
import sys
import readline  # For history and line editing
import traceback

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter import Interpreter

class LanguageREPL:
    def __init__(self):
        self.interpreter = Interpreter()
        self.history = []
        self.multiline_input = False
        self.buffer = []
        self.prompt = ">>> "
        self.continuation_prompt = "... "
        
        # Welcome message
        print("Custom Language REPL - Interactive Environment")
        print("Type 'exit()' or press Ctrl+D to exit")
        print("Type 'help()' for help")
        print("Type 'clear()' to clear interpreter state")
        print("Type 'vars()' to show all variables")
        print("Enter a blank line to execute in multiline mode\n")
    
    def run(self):
        """
        Start the REPL loop
        """
        while True:
            try:
                # Get the current prompt
                current_prompt = self.continuation_prompt if self.multiline_input else self.prompt
                
                # Get user input
                user_input = input(current_prompt)
                
                # Handle special commands
                if not self.multiline_input:
                    if user_input.strip() == 'exit()':
                        break
                    elif user_input.strip() == 'help()':
                        self._show_help()
                        continue
                    elif user_input.strip() == 'clear()':
                        self.interpreter = Interpreter()
                        print("Interpreter state cleared.")
                        continue
                    elif user_input.strip() == 'vars()':
                        self._show_variables()
                        continue
                    elif user_input.strip().startswith('load('):
                        # Handle loading files
                        filename = user_input.strip()[5:-1].strip("'\"")
                        self._load_file(filename)
                        continue
                    
                # Handle multiline input
                if self.multiline_input:
                    if user_input.strip() == "":
                        # Empty line ends multiline input
                        self.multiline_input = False
                        code_to_execute = '\n'.join(self.buffer)
                        self.buffer = []
                        self._execute(code_to_execute)
                    else:
                        # Add to buffer
                        self.buffer.append(user_input)
                else:
                    if user_input.strip().endswith(':'):
                        # Start multiline input
                        self.multiline_input = True
                        self.buffer.append(user_input)
                    elif user_input.strip() != "":
                        # Execute single line
                        self._execute(user_input)
            
            except EOFError:  # Ctrl+D
                print("\nExiting...")
                break
            except KeyboardInterrupt:  # Ctrl+C
                print("\nOperation interrupted")
                self.multiline_input = False
                self.buffer = []
            except Exception as e:
                print(f"Error: {e}")
                if '--debug' in sys.argv:
                    traceback.print_exc()
                self.multiline_input = False
                self.buffer = []
    
    def _execute(self, code):
        """
        Execute the given code.
        
        Args:
            code (str): Code to execute
        """
        try:
            # Create tokens
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            
            # Parse tokens into AST
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Execute the AST
            result = None
            for node in ast:
                result = self.interpreter.evaluate(node)
            
            # Print the result if it's not None
            if result is not None:
                print(repr(result))
                
        except Exception as e:
            print(f"Error: {e}")
            if '--debug' in sys.argv:
                traceback.print_exc()
    
    def _show_help(self):
        """
        Show help information
        """
        print("\nREPL Help:")
        print("  - Enter code to execute it")
        print("  - For multiline blocks, end a line with ':' and finish with an empty line")
        print("  - exit() - Exit the REPL")
        print("  - help() - Show this help message")
        print("  - clear() - Clear the interpreter state (variables and functions)")
        print("  - vars() - Show all defined variables")
        print("  - load('filename.lang') - Load and execute a file\n")
        print("Examples:")
        print("  >>> x = 42")
        print("  >>> if x > 10:")
        print("  ...     result = \"Greater than 10\"")
        print("  ...     ")
        print("  \"Greater than 10\"")
        print("")
        print("  >>> def factorial(n):")
        print("  ...     if n <= 1: return 1")
        print("  ...     return n * factorial(n - 1)")
        print("  ...     ")
        print("  >>> factorial(5)")
        print("  120")
    
    def _show_variables(self):
        """
        Show all defined variables
        """
        variables = self.interpreter.variables
        if not variables:
            print("No variables defined.")
            return
        
        print("\nDefined variables:")
        for name, value in variables.items():
            if callable(value):
                print(f"{name} = <function>")
            else:
                print(f"{name} = {repr(value)}")
        print("")
    
    def _load_file(self, filename):
        """
        Load and execute a file
        
        Args:
            filename (str): Path to the file
        """
        try:
            file_path = filename
            if not os.path.isabs(file_path):
                # If not absolute, try relative to current directory
                file_path = os.path.join(os.getcwd(), filename)
            
            with open(file_path, 'r') as file:
                code = file.read()
            
            print(f"Loading file: {file_path}")
            self._execute(code)
            print(f"Successfully executed: {filename}")
        except FileNotFoundError:
            print(f"Error: File not found: {filename}")
        except Exception as e:
            print(f"Error loading file: {e}")
            if '--debug' in sys.argv:
                traceback.print_exc()

def main():
    # Check for debug flag
    debug_mode = '--debug' in sys.argv
    if debug_mode:
        print("Debug mode enabled. Stack traces will be shown for errors.")
    
    repl = LanguageREPL()
    repl.run()

if __name__ == "__main__":
    main()