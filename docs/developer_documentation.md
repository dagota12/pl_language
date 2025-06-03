# Developer Documentation

## AmhPy Programming Language

AmhPy is a custom programming language designed specifically for educational purposes, targeting Ethiopian developers who are new to programming. The language combines English and Amharic (አማርኛ) keywords, making programming concepts more accessible to Ethiopian students while teaching fundamental programming principles.

## Architecture Overview

This document explains the design and implementation of AmhPy. The language implementation consists of four main components:

1. **Lexer**: Converts source code into tokens
2. **Parser**: Transforms tokens into an Abstract Syntax Tree (AST)
3. **Interpreter**: Executes the AST directly
4. **Transpiler**: Converts the AST into equivalent Python code

```
Source Code → Lexer → Tokens → Parser → AST → Interpreter/Transpiler → Results
```

## Educational Design Goals

AmhPy was created with the following educational objectives:

- **Cultural Accessibility**: Use Amharic keywords alongside English to make programming more familiar to Ethiopian developers
- **Learning Bridge**: Serve as a stepping stone to mainstream programming languages like Python
- **Conceptual Clarity**: Provide clear, simple syntax that emphasizes programming fundamentals
- **Bilingual Support**: Allow mixing of English and Amharic keywords for gradual transition

## Components

### 1. Lexer (`src/lexer/lexer.py`)

The lexer performs lexical analysis, converting raw source code into a stream of meaningful tokens. Each token has a type and a value.

Key features:

- Identifies bilingual keywords (`if`/`ከሆነ`, `else`/`ካልሆነ`, `while`/`እስከሆነ_ድረስ`, `def`/`ግለጽ`, `return`/`መልስ`)
- Recognizes operators (`+`, `-`, `*`, `/`, `%`, `==`, `!=`, `<`, `>`, etc.)
- Handles Unicode identifiers (supports Amharic variable names)
- Skips whitespace and comments
- Supports multi-word Amharic keywords

Example token output for AmhPy code:

```python
[('IDENTIFIER', 'ስም'), ('ASSIGN', '='), ('STRING', 'ዮሐንስ')]
```

#### Implementation Details

The lexer implements a simple state machine that scans the source code character by character, recognizing patterns and emitting tokens. It handles both English and Amharic operators, keywords, identifiers, and literals according to AmhPy's bilingual syntax rules.

**Unicode Support**: The lexer includes special handling for Amharic Unicode ranges (U+1200–U+137F) to properly recognize Amharic identifiers and keywords.

### 2. Parser (`src/parser/parser.py`)

The parser converts a stream of tokens into an Abstract Syntax Tree (AST), which represents the structure of the program. The parser implements a recursive descent algorithm with the following grammar components:

- Statements (assignments, if/else, while loops, function definitions)
- Expressions (arithmetic, comparison, logical operations)
- Blocks (groups of statements)

#### AST Structure

The AST consists of nested dictionaries, each representing a node with a specific type and relevant properties.

Example AST for `ውጤት = a + b`:

```python
{
    'type': 'Assignment',
    'identifier': 'ውጤት',
    'value': {
        'type': 'BinaryOperation',
        'operator': '+',
        'left': {'type': 'Identifier', 'value': 'a'},
        'right': {'type': 'Identifier', 'value': 'b'}
    }
}
```

#### Block Structure

Blocks are an important concept in AmhPy, representing groups of statements in control structures and function bodies. The parser creates Block nodes that contain arrays of statement nodes:

```python
{
    'type': 'Block',
    'statements': [
        {'type': 'Assignment', 'identifier': 'ድምር', 'value': {...}},
        {'type': 'Assignment', 'identifier': 'i', 'value': {...}}
    ]
}
```

Statements within blocks are separated by semicolons, which is particularly important for complex if-else constructs in AmhPy.

### 3. Interpreter (`src/interpreter/__init__.py`)

The interpreter evaluates the AST to execute the program. It maintains an environment (variable and function space) and processes each node according to its type.

Key features:

- Evaluates expressions with bilingual operators
- Handles variable assignments and lookups (supports Unicode variable names)
- Executes control flow logic (if/else, while loops) in both languages
- Manages function calls and returns
- Implements the `አውጣ` (Amharic print) function alongside `spit`
- Implements short-circuit evaluation for logical operations

#### Function Handling

Functions are treated as first-class values with closures. When a function is defined using either `def` or `ግለጽ`, it captures its current environment, allowing for proper scoping.

### 4. Transpiler (`src/transpiler/__init__.py`)

The transpiler converts the AST into equivalent Python code. It walks the AST and generates appropriate Python syntax for each node type.

Key features:

- Maintains proper indentation
- Translates expressions and operators
- Creates appropriate Python control structures
- Handles bilingual function definitions and calls
- Converts Amharic keywords to Python equivalents

Example transpiled output for `ግለጽ ደምር(a, b): መልስ a + b`:

```python
def ደምር(a, b):
    return (a + b)
```

## Educational Features

### Bilingual Programming Support

AmhPy allows students to write programs using familiar Amharic terms:

```amhpy
# Students can use Amharic keywords
ከሆነ ቁጥር > 0:
    አውጣ("አዎንታዊ ቁጥር")
ካልሆነ:
    አውጣ("አሉታዊ ቁጥር")
```

### Gradual Transition

Students can mix languages as they become more comfortable:

```amhpy
# Mixed English and Amharic
if ቁጥር > 0:
    spit("Positive number")
else:
    አውጣ("አሉታዊ ቁጥር")
```

## Error Handling

The current implementation provides basic error messages for syntax errors, undefined variables, and runtime errors. For educational purposes, error messages could be enhanced to include:

- Bilingual error messages (English and Amharic)
- Line and column information
- Suggestions for common mistakes
- Learning resources for specific errors

## Testing Infrastructure

The project includes comprehensive tests for all components:

- `tests/test_lexer.py`: Tests for token generation (including Amharic keywords)
- `tests/test_parser.py`: Tests for AST construction with bilingual syntax
- `tests/test_interpreter.py`: Tests for program execution in both languages
- `tests/test_transpiler.py`: Tests for Python code generation

## Extension Points for Educational Enhancement

Potential areas for extending AmhPy for better educational outcomes:

1. **Educational Standard Library**: Built-in functions for common learning exercises
2. **Interactive Learning Mode**: Step-by-step execution with variable visualization
3. **Amharic Error Messages**: Localized error reporting for better comprehension
4. **Educational Examples**: Curated problem sets for Ethiopian computer science curriculum
5. **IDE Integration**: Syntax highlighting and auto-completion for Amharic keywords
6. **Cultural Examples**: Programming exercises using Ethiopian contexts and data

## Implementation Challenges

During development of AmhPy, we faced several educational-specific challenges:

1. **Unicode Handling**: Properly supporting Amharic text in all components
2. **Keyword Ambiguity**: Handling potential conflicts between languages
3. **Cultural Context**: Ensuring examples and variable names are culturally appropriate
4. **Learning Curve**: Balancing simplicity with programming completeness
5. **Parser Complexity**: Managing semicolon-separated statements in if-else, scoping blocks are challenging

## Performance Considerations

AmhPy is designed for educational simplicity rather than performance. For teaching purposes, the interpreter provides immediate feedback, while the transpiler allows students to see equivalent Python code, facilitating their transition to mainstream programming languages.

## Educational Impact

AmhPy serves as a bridge between Ethiopian students' native language and international programming standards, making computer science education more accessible while preparing students for global software development careers.
