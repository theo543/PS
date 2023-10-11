from math import factorial, prod

def perm(n, k):
    return prod(range(n - k + 1, n + 1))

def comb(n, k):
    if k > (n // 2):
        k = n - k
    return prod(range(n - k + 1, n + 1)) // factorial(k)
