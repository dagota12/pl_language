# User Manual

## Introduction

This document provides instructions on how to install, write, and run programs in our custom programming language. This language was designed to be simple yet powerful, combining elements of imperative and functional programming paradigms.

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/language-project.git
cd language-project
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Install the package in development mode:

```bash
pip install -e .
```

## Writing Programs

### File Extension

Programs written in our language should use the `.lang` file extension, e.g., `factorial.lang`.

### Syntax Basics

#### Variables and Assignments

Variables are dynamically typed and defined through assignment:

```
x = 42
name = "John"
```

#### Arithmetic Operations

The language supports basic arithmetic operations:

```
result = 5 + 3 * 2  # Result: 11 (follows precedence rules)
remainder = 10 % 3  # Result: 1 (modulo operation)
```

#### Control Flow

##### If-Else Statements

```
if x > 0:
    result = "positive"
else:
    result = "non-positive"
```

##### While Loops

```
i = 1
sum = 0
while i <= 10:
    sum = sum + i
    i = i + 1
```

Note: Use semicolons to separate multiple statements in a block:

```
while i <= 5:
    sum = sum + i;
    i = i + 1
```

#### Functions

Define functions using the `def` keyword:

```
def add(a, b):
    return a + b

result = add(3, 4)  # Result: 7
```

Functions support recursion:

```
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
```

#### Comments

Use the `#` character for single-line comments:

```
# This is a comment
x = 42  # This is also a comment
```

## Running Programs

### Using the Interpreter

To run a program with the interpreter:

```bash
python -m language_project.run <your_file.lang>
```

Example:

```bash
python -m language_project.run examples/factorial.lang
```

### Using the Transpiler

To transpile a program to Python:

```bash
python -m language_project.transpile <your_file.lang> <output_file.py>
```

Example:

```bash
python -m language_project.transpile examples/factorial.lang factorial.py
```

Then run the generated Python file:

```bash
python factorial.py
```

## Examples

The `examples/` directory contains several example programs:

1. `factorial.lang` - Calculates the factorial of a number
2. `fibonacci.lang` - Generates Fibonacci numbers
3. `sum_calculator.lang` - Computes the sum of numbers from 1 to n
4. `prime_checker.lang` - Checks if a number is prime
5. `gcd_calculator.lang` - Calculates the greatest common divisor of two numbers

## Limitations

- No support for classes or object-oriented programming
- No built-in data structures like lists or dictionaries
- Limited error reporting and debugging tools
- No module system for code organization

## Troubleshooting

### Common Errors

1. **Syntax Errors**: Check your code for missing colons, parentheses, or invalid syntax.
2. **Undefined Variables**: Ensure variables are assigned before use.
3. **Infinite Loops**: Make sure your while loops have a proper exit condition.

For more assistance, please open an issue on the project's GitHub repository.
