#!/usr/bin/env python3
"""
REPL (Read-Eval-Print Loop) for our custom programming language.
This provides an interactive shell where users can type and execute
language statements one at a time.
"""

import os
import sys
import traceback

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter import Interpreter

class REPL:
    def __init__(self):
        self.interpreter = Interpreter()
        self.multiline_buffer = []
        self.in_multiline = False
        
    def print_banner(self):
        """Print the welcome banner"""
        print("=" * 60)
        print("  Custom Programming Language REPL")
        print("  Supports both English and Amharic keywords")
        print("  Type 'help' for commands, 'exit' to quit")
        print("=" * 60)
        
    def print_help(self):
        """Print help information"""
        print("\nCommands:")
        print("  help       - Show this help message")
        print("  exit       - Exit the REPL")
        print("  clear      - Clear all variables")
        print("  vars       - Show current variables")
        print("  funcs      - Show defined functions")
        print("  reset      - Reset the interpreter state")
        print("\nLanguage Features:")
        print("  Variables:     x = 42")
        print("  Arithmetic:    2 + 3 * 4")
        print("  Comparisons:   x > 10")
        print("  If statements: if x > 0: y = 1 else: y = 0")
        print("  While loops:   while i < 5: i = i + 1")
        print("  Functions:     def add(a, b): return a + b")
        print("  Print output:  spit(42) or አውጣ(42)")
        print("  Factorial:     5!")
        print("\nAmharic Keywords:")
        print("  ከሆነ (if), ካልሆነ (else), እስከሆነ ድረስ (while)")
        print("  ግለጽ (def), መልስ (return), አውጣ (print)")
        print("  እና (and), ወይም (or), ይሁን (assignment)")
        
    def show_variables(self):
        """Show current variables"""
        if self.interpreter.variables:
            print("\nCurrent variables:")
            for name, value in self.interpreter.variables.items():
                print(f"  {name} = {value}")
        else:
            print("\nNo variables defined.")
            
    def show_functions(self):
        """Show defined functions"""
        if self.interpreter.functions:
            print("\nDefined functions:")
            for name, func in self.interpreter.functions.items():
                params = ', '.join(func.parameters)
                print(f"  {name}({params})")
        else:
            print("\nNo functions defined.")
            
    def reset_interpreter(self):
        """Reset the interpreter state"""
        self.interpreter = Interpreter()
        print("\nInterpreter state reset.")
        
    def is_multiline_start(self, line):
        """Check if this line starts a multiline statement"""
        line = line.strip()
        return (line.endswith(':') and 
                any(line.startswith(keyword) for keyword in 
                    ['if', 'else', 'while', 'def', 'ከሆነ', 'ካልሆነ', 'እስከሆነ ድረስ', 'ግለጽ']))
    
    def execute_code(self, code):
        """Execute a piece of code and handle errors gracefully"""
        try:
            # Tokenize
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            
            if not tokens:
                return
            
            # Parse
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Execute
            for node in ast:
                result = self.interpreter.evaluate(node)
                # Only print result if it's not None and not an assignment
                if (result is not None and 
                    node.get('type') not in ['Assignment', 'FunctionDefinition', 'SpitFunction']):
                    print(f"=> {result}")
                    
        except Exception as e:
            print(f"Error: {e}")
            # Uncomment the line below for debugging
            # traceback.print_exc()
    
    def run(self):
        """Run the REPL"""
        self.print_banner()
        
        while True:
            try:
                if self.in_multiline:
                    prompt = "... "
                else:
                    prompt = ">>> "
                    
                line = input(prompt).strip()
                
                # Handle commands
                if line.lower() == 'exit':
                    print("Goodbye!")
                    break
                elif line.lower() == 'help':
                    self.print_help()
                    continue
                elif line.lower() == 'clear':
                    self.interpreter.variables.clear()
                    print("Variables cleared.")
                    continue
                elif line.lower() == 'vars':
                    self.show_variables()
                    continue
                elif line.lower() == 'funcs':
                    self.show_functions()
                    continue
                elif line.lower() == 'reset':
                    self.reset_interpreter()
                    continue
                elif not line:
                    if self.in_multiline:
                        # Empty line ends multiline input
                        code = ' '.join(self.multiline_buffer)
                        self.multiline_buffer = []
                        self.in_multiline = False
                        self.execute_code(code)
                    continue
                
                # Handle multiline input
                if self.in_multiline:
                    self.multiline_buffer.append(line)
                    if not line.endswith(':') and not line.startswith(' '):
                        # End of multiline block
                        code = ' '.join(self.multiline_buffer)
                        self.multiline_buffer = []
                        self.in_multiline = False
                        self.execute_code(code)
                elif self.is_multiline_start(line):
                    self.multiline_buffer = [line]
                    self.in_multiline = True
                else:
                    # Single line execution
                    self.execute_code(line)
                    
            except KeyboardInterrupt:
                print("\n\nUse 'exit' to quit the REPL.")
                self.multiline_buffer = []
                self.in_multiline = False
            except EOFError:
                print("\nGoodbye!")
                break

def main():
    repl = REPL()
    repl.run()

if __name__ == '__main__':
    main()