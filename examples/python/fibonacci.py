# This file was automatically generated from fibonacci.lang
# by the language transpiler

def fibonacci(n):
    if (n <= 1):
        return n
    else:
        return (fibonacci((n - 1)) + fibonacci((n - 2)))
result = fibonacci(10)