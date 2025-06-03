# Formal Grammar Specification for AmhPy

Below is the formal grammar specification for AmhPy programming language in BNF (Backus-Naur Form) notation. AmhPy supports both English and Amharic (አማርኛ) keywords and Unicode identifiers.

```bnf
<program> ::= <statement>*

<statement> ::= <assignment>
              | <if_statement>
              | <while_statement>
              | <function_definition>
              | <return_statement>
              | <print_statement>
              | <statement> ";" <statement>

<block> ::= <statement>

<assignment> ::= <identifier> "=" <expression>

<if_statement> ::= (<if_keyword>) <expression> ":" <block> [<else_keyword> ":" <block>]

<while_statement> ::= (<while_keyword>) <expression> ":" <block>

<function_definition> ::= (<def_keyword>) <identifier> "(" [<parameter_list>] ")" ":" <block>

<parameter_list> ::= <identifier> ("," <identifier>)*

<return_statement> ::= (<return_keyword>) <expression>

<print_statement> ::= (<print_keyword>) <expression> ("," <expression>)*

<expression> ::= <logical_expression>
               | <comparison>

<comparison> ::= <logical_expression> <comparison_operator> <logical_expression>

<comparison_operator> ::= "==" | "!=" | "<" | "<=" | ">" | ">="

<logical_expression> ::= <arithmetic_expression>
                       | <logical_expression> <logical_operator> <arithmetic_expression>

<logical_operator> ::= (<and_keyword>) | (<or_keyword>)

<arithmetic_expression> ::= <term>
                          | <arithmetic_expression> "+" <term>
                          | <arithmetic_expression> "-" <term>

<term> ::= <factor>
         | <term> "*" <factor>
         | <term> "/" <factor>
         | <term> "%" <factor>

<factor> ::= <number>
           | <string>
           | <identifier>
           | "(" <expression> ")"
           | <function_call>

<function_call> ::= <identifier> "(" [<argument_list>] ")"

<argument_list> ::= <expression> ("," <expression>)*

<number> ::= ["-"] <digit>+

<string> ::= '"' <unicode_char>* '"' | "'" <unicode_char>* "'"

<identifier> ::= <identifier_start> <identifier_char>*

<identifier_start> ::= <ascii_letter> | <amharic_char>

<identifier_char> ::= <ascii_letter> | <digit> | "_" | <amharic_char>

<ascii_letter> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"

<digit> ::= "0" | "1" | ... | "9"

<amharic_char> ::= /* Unicode characters in ranges U+1200–U+137F, U+1380–U+139F, U+2D80–U+2DDF */

<unicode_char> ::= /* Any valid Unicode character */

<!-- Bilingual Keywords -->
<if_keyword> ::= "if" | "ከሆነ"

<else_keyword> ::= "else" | "ካልሆነ"

<while_keyword> ::= "while" | "እስከሆነ_ድረስ"

<def_keyword> ::= "def" | "ግለጽ"

<return_keyword> ::= "return" | "መልስ"

<print_keyword> ::= "spit" | "አውጣ"

<and_keyword> ::= "and" | "እና"

<or_keyword> ::= "or" | "ወይም"
```

## Language Features

AmhPy supports:

1. **Bilingual Programming**: Write code using English or Amharic keywords
2. **Unicode Identifiers**: Variable names can use Amharic characters
3. **Variables and assignments**: Using the `=` operator
4. **Arithmetic operations**: +, -, \*, /, %
5. **Comparison operators**: ==, !=, <, <=, >, >=
6. **Logical operators**: and/እና, or/ወይም
7. **Control structures**: if-else statements, while loops
8. **Functions**: function definition with parameters and return values
9. **Recursion**: functions can call themselves
10. **Print functions**: spit (English) or አውጣ (Amharic)
11. **Semicolons**: statements can be separated by semicolons
12. **Comments**: lines starting with # are treated as comments
13. **String literals**: Support for both single and double quotes with Unicode content

## Bilingual Keyword Examples

### Control Flow

- **English**: `if`, `else`, `while`
- **Amharic**: `ከሆነ`, `ካልሆነ`, `እስከሆነ_ድረስ`

### Functions

- **English**: `def`, `return`
- **Amharic**: `ግለጽ`, `መልስ`

### Output

- **English**: `spit`
- **Amharic**: `አውጣ`

### Logical Operators

- **English**: `and`, `or`
- **Amharic**: `እና`, `ወይም`

## Unicode Support

The grammar supports:

1. **Amharic Identifiers**: Variables can be named using Amharic characters

   - Example: `ስም = "ዮሐንስ"`, `እድሜ = 25`

2. **Mixed Scripts**: Identifiers can combine ASCII and Amharic characters

   - Example: `user_ስም = "John"`

3. **String Literals**: Full Unicode support in string content
   - Example: `message = "ሰላም ዓለም!"` (Hello World in Amharic)

## Execution Model

AmhPy follows these execution steps:

1. **Lexical Analysis**: Source code is tokenized with Unicode support
2. **Parsing**: Tokens are transformed into an Abstract Syntax Tree (AST)
3. **Interpretation**: The AST is evaluated to produce results
4. **Transpilation**: The AST can be converted to equivalent Python code

This is a simple imperative language with elements of functional programming, designed specifically for educational purposes to make programming accessible to Ethiopian developers.
