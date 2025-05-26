# This file was automatically generated from gcd_calculator.lang
# by the language transpiler

def gcd(a, b):
    if (b == 0):
        return a
return gcd(b, (a % b))
result = gcd(48, 18)
result = gcd(17, 13)