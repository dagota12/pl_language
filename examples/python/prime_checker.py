# This file was automatically generated from prime_checker.lang
# by the language transpiler

def is_prime(n):
    if (n <= 1):
        return 0
i = 2
while (i < n):
    if ((n % i) == 0):
        return 0
i = (i + 1)
return 1
result = is_prime(17)
result = is_prime(15)