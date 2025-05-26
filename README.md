# Custom Programming Language Project

This project implements a simple custom programming language with a lexer, parser, interpreter, and transpiler.

## Features

- Variables and assignments
- Arithmetic, comparison, and logical operations
- Control structures (if-else statements, while loops)
- Functions with parameters and return values
- Recursion support
- Python transpilation

## Project Structure

```
language-project/
├── docs/                     # Documentation files
│   ├── developer_documentation.md  # For developers
│   ├── grammar.md            # Formal grammar specification
│   ├── reflection.md         # Project reflection
│   └── user_manual.md        # User guide
├── examples/                 # Example programs
│   ├── factorial.lang
│   ├── fibonacci.lang
│   ├── gcd_calculator.lang
│   ├── prime_checker.lang
│   ├── sum_calculator.lang
│   └── python/              # Transpiled Python equivalents
├── language_project/        # Main package
│   ├── run.py               # Interpreter runner
│   └── transpile.py         # Transpiler runner
├── scripts/                 # Helper scripts
│   └── transpile_examples.py # Batch transpile examples
├── src/                     # Source code
│   ├── interpreter/         # Interpreter module
│   ├── lexer/               # Lexer module
│   ├── parser/              # Parser module
│   └── transpiler/          # Transpiler module
└── tests/                   # Unit tests
    ├── test_interpreter.py
    ├── test_lexer.py
    ├── test_parser.py
    └── test_transpiler.py
```

## Getting Started

### Prerequisites

- Python 3.6 or higher

### Installation

1. Clone the repository
2. Install dependencies:

```
pip install -r requirements.txt
```

### Running Programs

To run a program using the interpreter:

```
python language_project/run.py examples/factorial.lang
```

To transpile a program to Python:

```
python language_project/transpile.py examples/factorial.lang output.py
```

### Running Tests

To run all tests:

```
python tests/run_tests.py
```

## Documentation

- [User Manual](docs/user_manual.md)
- [Developer Documentation](docs/developer_documentation.md)
- [Grammar Specification](docs/grammar.md)
- [Project Reflection](docs/reflection.md)

## Example Programs

The `examples/` directory contains several example programs demonstrating different language features:

1. `factorial.lang` - Calculates the factorial of a number
2. `fibonacci.lang` - Generates Fibonacci numbers
3. `sum_calculator.lang` - Computes the sum of numbers from 1 to n
4. `prime_checker.lang` - Checks if a number is prime
5. `gcd_calculator.lang` - Calculates the greatest common divisor of two numbers

## License

This project is licensed under the MIT License - see the LICENSE file for details.
