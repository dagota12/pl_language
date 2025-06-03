# This file was automatically generated from factorial.lang
# by the language transpiler

def factorial(n):
    if (n <= 1):
            return 1
    else:
            return (n * factorial((n - 1)))
result = factorial(5)