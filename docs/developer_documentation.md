# Developer Documentation

## Architecture Overview

This document explains the design and implementation of our custom programming language. The language implementation consists of four main components:

1. **Lexer**: Converts source code into tokens
2. **Parser**: Transforms tokens into an Abstract Syntax Tree (AST)
3. **Interpreter**: Executes the AST directly
4. **Transpiler**: Converts the AST into equivalent Python code

```
Source Code → Lexer → Tokens → Parser → AST → Interpreter/Transpiler → Results
```

## Components

### 1. Lexer (`src/lexer/lexer.py`)

The lexer performs lexical analysis, converting raw source code into a stream of meaningful tokens. Each token has a type and a value.

Key features:

- Identifies keywords (`if`, `else`, `while`, `def`, `return`)
- Recognizes operators (`+`, `-`, `*`, `/`, `%`, `==`, `!=`, `<`, `>`, etc.)
- Handles identifiers, numbers, and delimiters
- Skips whitespace and comments

Example token output:

```python
[('IDENTIFIER', 'x'), ('ASSIGN', '='), ('NUMBER', '42')]
```

#### Implementation Details

The lexer implements a simple state machine that scans the source code character by character, recognizing patterns and emitting tokens. It handles operators, keywords, identifiers, and literals according to the language's syntax rules.

### 2. Parser (`src/parser/parser.py`)

The parser converts a stream of tokens into an Abstract Syntax Tree (AST), which represents the structure of the program. The parser implements a recursive descent algorithm with the following grammar components:

- Statements (assignments, if/else, while loops, function definitions)
- Expressions (arithmetic, comparison, logical operations)
- Blocks (groups of statements)

#### AST Structure

The AST consists of nested dictionaries, each representing a node with a specific type and relevant properties.

Example AST for `x = a + b`:

```python
{
    'type': 'Assignment',
    'identifier': 'x',
    'value': {
        'type': 'BinaryOperation',
        'operator': '+',
        'left': {'type': 'Identifier', 'value': 'a'},
        'right': {'type': 'Identifier', 'value': 'b'}
    }
}
```

#### Block Structure

Blocks are an important concept in the language, representing groups of statements in control structures and function bodies. The parser creates Block nodes that contain arrays of statement nodes:

```python
{
    'type': 'Block',
    'statements': [
        {'type': 'Assignment', 'identifier': 'sum', 'value': {...}},
        {'type': 'Assignment', 'identifier': 'i', 'value': {...}}
    ]
}
```

Statements within blocks are separated by semicolons.

### 3. Interpreter (`src/interpreter/__init__.py`)

The interpreter evaluates the AST to execute the program. It maintains an environment (variable and function space) and processes each node according to its type.

Key features:

- Evaluates expressions
- Handles variable assignments and lookups
- Executes control flow logic (if/else, while loops)
- Manages function calls and returns
- Implements short-circuit evaluation for logical operations

#### Function Handling

Functions are treated as first-class values with closures. When a function is defined, it captures its current environment, allowing for proper scoping.

### 4. Transpiler (`src/transpiler/__init__.py`)

The transpiler converts the AST into equivalent Python code. It walks the AST and generates appropriate Python syntax for each node type.

Key features:

- Maintains proper indentation
- Translates expressions and operators
- Creates appropriate Python control structures
- Handles function definitions and calls

Example transpiled output for `def add(a, b): return a + b`:

```python
def add(a, b):
    return (a + b)
```

## Error Handling

The current implementation provides basic error messages for syntax errors, undefined variables, and runtime errors. Error handling could be enhanced in future versions to include:

- Line and column information
- More descriptive error messages
- Recovery mechanisms for better error reporting

## Testing Infrastructure

The project includes comprehensive tests for all components:

- `tests/test_lexer.py`: Tests for token generation
- `tests/test_parser.py`: Tests for AST construction
- `tests/test_interpreter.py`: Tests for program execution
- `tests/test_transpiler.py`: Tests for Python code generation

## Extension Points

Potential areas for extending the language:

1. **Data Structures**: Add support for arrays, dictionaries
2. **String Operations**: Implement string manipulation functions
3. **Standard Library**: Create built-in functions for common operations
4. **Error Handling**: Add try/catch mechanisms
5. **Type System**: Implement static typing with type checking
6. **Module System**: Add support for importing code from other files

## Implementation Challenges

During development, we faced several challenges:

1. **Block Structure**: Properly handling blocks of statements in control structures
2. **Operator Precedence**: Ensuring correct evaluation order for expressions
3. **Variable Scoping**: Managing variable environments for function calls
4. **Recursive Functions**: Supporting proper recursion with environment capturing

## Performance Considerations

The interpreter is designed for simplicity rather than performance. For performance-critical applications, the transpiler should be used to generate Python code, which can then benefit from Python's optimizations.
