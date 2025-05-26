# Formal Grammar Specification

Below is the formal grammar specification for our programming language in BNF (Backus-Naur Form) notation.

```bnf
<program> ::= <statement>*

<statement> ::= <assignment>
              | <if_statement>
              | <while_statement>
              | <function_definition>
              | <return_statement>
              | <statement> ";" <statement>

<block> ::= <statement>

<assignment> ::= <identifier> "=" <expression>

<if_statement> ::= "if" <expression> ":" <block> ["else" ":" <block>]

<while_statement> ::= "while" <expression> ":" <block>

<function_definition> ::= "def" <identifier> "(" [<parameter_list>] ")" ":" <block>

<parameter_list> ::= <identifier> ("," <identifier>)*

<return_statement> ::= "return" <expression>

<expression> ::= <logical_expression>
               | <comparison>

<comparison> ::= <logical_expression> <comparison_operator> <logical_expression>

<comparison_operator> ::= "==" | "!=" | "<" | "<=" | ">" | ">="

<logical_expression> ::= <arithmetic_expression>
                       | <logical_expression> <logical_operator> <arithmetic_expression>

<logical_operator> ::= "and" | "or"

<arithmetic_expression> ::= <term>
                          | <arithmetic_expression> "+" <term>
                          | <arithmetic_expression> "-" <term>

<term> ::= <factor>
         | <term> "*" <factor>
         | <term> "/" <factor>
         | <term> "%" <factor>

<factor> ::= <number>
           | <identifier>
           | "(" <expression> ")"
           | <function_call>

<function_call> ::= <identifier> "(" [<argument_list>] ")"

<argument_list> ::= <expression> ("," <expression>)*

<number> ::= ["-"] <digit>+

<identifier> ::= <letter> (<letter> | <digit> | "_")*

<letter> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"

<digit> ::= "0" | "1" | ... | "9"
```

## Language Features

Our language supports:

1. **Variables and assignments**
2. **Arithmetic operations**: +, -, \*, /, %
3. **Comparison operators**: ==, !=, <, <=, >, >=
4. **Logical operators**: and, or
5. **Control structures**: if-else statements, while loops
6. **Functions**: function definition with parameters and return values
7. **Recursion**: functions can call themselves
8. **Semicolons**: statements can be separated by semicolons
9. **Comments**: lines starting with # are treated as comments

## Execution Model

The language follows these execution steps:

1. **Lexical Analysis**: Source code is tokenized into a stream of tokens
2. **Parsing**: Tokens are transformed into an Abstract Syntax Tree (AST)
3. **Interpretation**: The AST is evaluated to produce results
4. **Transpilation**: The AST can also be converted to equivalent Python code

This is a simple imperative language with elements of functional programming (through first-class functions).
