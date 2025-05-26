# This file was automatically generated from sum_calculator.lang
# by the language transpiler

def sum_to_n(n):
    i = 1
    total = 0
    while (i <= n):
        total = (total + i)
        i = (i + 1)
return total
result = sum_to_n(100)