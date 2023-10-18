from math import factorial, prod

def perm(n, k):
    assert(k <= n)
    return prod(range(n - k + 1, n + 1))

def comb(n, k):
    assert(k <= n)
    if k > (n // 2):
        k = n - k
    return prod(range(n - k + 1, n + 1)) // factorial(k)
