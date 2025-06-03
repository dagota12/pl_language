# User Manual

## Introduction

This document provides instructions on how to install, write, and run programs in our custom programming language. This language was designed to be simple yet powerful, combining elements of imperative and functional programming paradigms. The language supports both English and Amharic (አማርኛ) keywords, making it accessible to Ethiopian developers.

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

Programs written in our language should use the `.lang` file extension, e.g., `factorial.lang` or `amharic_example.lang`.

### Syntax Basics

#### Variables and Assignments

Variables are dynamically typed and defined through assignment using the `=` operator:

**English:**

```
x = 42
name = "John"
```

**Amharic (አማርኛ):**

```
x = 42
ስም = "ዮሐንስ"
እድሜ = 25
```

#### Arithmetic Operations

The language supports basic arithmetic operations:

**English:**

```
result = 5 + 3 * 2  # Result: 11 (follows precedence rules)
remainder = 10 % 3  # Result: 1 (modulo operation)
```

**Amharic (አማርኛ):**

```
ውጤት = 5 + 3 * 2   # ውጤት: 11 (የማስላት ቅደም ተከተል ይከተላል)
ቀሪ = 10 % 3       # ውጤት: 1 (modulo አሰራር)
```

#### Control Flow

##### If-Else Statements

**English:**

```
if x > 0:
    result = "positive"
else:
    result = "non-positive"
```

**Amharic (አማርኛ):**

```
ከሆነ x > 0:
    ውጤት = "አዎንታዊ"
ካልሆነ:
    ውጤት = "አሉታዊ"
```

##### While Loops

**English:**

```
i = 1
sum = 0
while i <= 10:
    sum = sum + i
    i = i + 1
```

**Amharic (አማርኛ):**

```
i = 1
ድምር = 0
እስከሆነ_ድረስ i <= 10:
    ድምር = ድምር + i;
    i = i + 1
```

Note: Use semicolons to separate multiple statements in a block:

**English:**

```
while i <= 5:
    sum = sum + i;
    i = i + 1
```

**Amharic (አማርኛ):**

```
እስከሆነ_ድረስ i <= 5:
    ድምር = ድምር + i;
    i = i + 1
```

#### Functions

Define functions using the `def` keyword (English) or `ግለጽ` (Amharic):

**English:**

```
def add(a, b):
    return a + b

result = add(3, 4)  # Result: 7
```

**Amharic (አማርኛ):**

```
ግለጽ ደምር(a, b):
    መልስ a + b

ውጤት = ደምር(3, 4)  # ውጤት: 7
```

Functions support recursion:

**English:**

```
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
```

**Amharic (አማርኛ):**

```
ግለጽ ፋክቶሪያል(n):
    ከሆነ n <= 1:
        መልስ 1
    ካልሆነ:
        መልስ n * ፋክቶሪያል(n - 1)
```

#### Output/Print Functions

Use `spit` (English) or `አውጣ` (Amharic) to display output:

**English:**

```
spit("Hello, World!")
spit("The result is:", result)
```

**Amharic (አማርኛ):**

```
አውጣ("ሰላም ልዩል!")
አውጣ("ውጤቱ:", ውጤት)
```

#### Comments

Use the `#` character for single-line comments:

**English:**

```
# This is a comment
x = 42  # This is also a comment
```

**Amharic (አማርኛ):**

```
# ይህ አስተያየት ነው
x = 42  # ይህም አስተያየት ነው
```

## Complete Example Programs

### Min-Max Calculator

**English Version:**

```
# Find minimum and maximum of two numbers
first = 45
second = 32

spit("Numbers:", first, second)

if first > second:
    min_num = second;
    max_num = first
else:
    min_num = first;
    max_num = second

difference = max_num - min_num

spit("Minimum:", min_num)
spit("Maximum:", max_num)
spit("Difference:", difference)
```

**Amharic Version:**

```
# የሁለት ቁጥሮች ትንሽና ትልቅ ማግኛ ፕሮግራም
አንደኛ = 45
ሁለተኛ = 32

አውጣ("ቁጥሮች:", አንደኛ, ሁለተኛ)

ከሆነ አንደኛ > ሁለተኛ:
    ትንሽ_ቁጥር = ሁለተኛ;
    ትልቅ_ቁጥር = አንደኛ
ካልሆነ:
    ትንሽ_ቁጥር = አንደኛ;
    ትልቅ_ቁጥር = ሁለተኛ

ልዩነት = ትልቅ_ቁጥር - ትንሽ_ቁጥር

አውጣ("ትንሽ ቁጥር:", ትንሽ_ቁጥር)
አውጣ("ትልቅ ቁጥር:", ትልቅ_ቁጥር)
አውጣ("ልዩነት:", ልዩነት)
```

### Factorial Calculator

**English Version:**

```
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

num = 5
result = factorial(num)
spit("Factorial of", num, "is", result)
```

**Amharic Version:**

```
ግለጽ ፋክቶሪያል(n):
    ከሆነ n <= 1:
        መልስ 1
    ካልሆነ:
        መልስ n * ፋክቶሪያል(n - 1)

ቁጥር = 5
ውጤት = ፋክቶሪያል(ቁጥር)
አውጣ("ፋክቶሪያል የ", ቁጥር, "ነው", ውጤት)
```

## Language Features

### Supported Keywords

| English  | Amharic     | Description           |
| -------- | ----------- | --------------------- |
| `if`     | `ከሆነ`       | Conditional statement |
| `else`   | `ካልሆነ`      | Alternative condition |
| `while`  | `እስከሆነ_ድረስ` | Loop statement        |
| `def`    | `ግለጽ`       | Function definition   |
| `return` | `መልስ`       | Return value          |
| `spit`   | `አውጣ`       | Output/print          |
| `and`    | `እና`        | Logical AND           |
| `or`     | `ወይም`       | Logical OR            |
| `not`    | `ተቃራኒ`      | Logical NOT           |

### Operators

- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `==`, `!=`, `<`, `<=`, `>`, `>=`
- Assignment: `=`
- Logical: `and`/`እና`, `or`/`ወይም`, `not`/`ተቃራኒ`

## Running Programs

### Using the Interpreter

To run a program with the interpreter:

```bash
python -m language_project.run <your_file.lang>
```

Example:

```bash
python -m language_project.run examples/factorial.lang
python -m language_project.run examples/amharic_min_max.lang
```

### Using the Transpiler

To transpile a program to Python:

```bash
python -m language_project.transpile <your_file.lang> <output_file.py>
```

Example:

```bash
python -m language_project.transpile examples/factorial.lang factorial.py
python -m language_project.transpile examples/amharic_factorial.lang amharic_factorial.py
```

Then run the generated Python file:

```bash
python factorial.py
```

## Examples

The `examples/` directory contains several example programs in both English and Amharic:

### English Examples:

1. `factorial.lang` - Calculates the factorial of a number
2. `fibonacci.lang` - Generates Fibonacci numbers
3. `sum_calculator.lang` - Computes the sum of numbers from 1 to n
4. `prime_checker.lang` - Checks if a number is prime
5. `gcd_calculator.lang` - Calculates the greatest common divisor of two numbers

### Amharic Examples:

1. `amharic_factorial.lang` - ፋክቶሪያል ማስላት
2. `amharic_fibonacci.lang` - ፊቦናቺ ቁጥሮች
3. `amharic_min_max.lang` - ትንሽና ትልቅ ቁጥር ማግኛ
4. `amharic_sum_calculator.lang` - ድምር ማስሊያ
5. `amharic_number_operations.lang` - የቁጥር አሰራሮች

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
4. **Mixed Keywords**: While you can mix English and Amharic keywords in the same program, it's recommended to use one language consistently for readability.

### Unicode Support

When writing Amharic programs, ensure your text editor supports UTF-8 encoding to properly display Amharic characters.

For more assistance, please open an issue on the project's GitHub repository.
