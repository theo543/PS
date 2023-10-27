import numpy as np
from mpmath import mp, nstr
from math import inf

def exact_formula(n, k):
    # (n! / (k!(n-k)!) / 2^n
    f = mp.factorial
    # arbitrary precision number
    return (f(n) / (f(k) * f(n - k))) / mp.power(2, n)

def sim(n, k):
    assert(k <= n)

    trues = 0
    times = 0
    def log(end):
        print(f"p = {trues}/{times} = {trues/times:.10f}", end=end)
    try:
        gen = np.random.default_rng()
        bin_gen_size = 20000000
        while True:
            counts = gen.binomial(n, 0.5, bin_gen_size)
            trues += np.count_nonzero(counts == k)
            times += bin_gen_size
            log('\r')
    except KeyboardInterrupt:
        log('\n')

if __name__ == "__main__":
    n = int(input("n = "))
    k = int(input("k = "))
    print(f"n = {n}, k = {k}")

    exact_result = exact_formula(n, k)
    print(f"exact formula => {nstr(exact_result, min_fixed=-50, max_fixed=inf)}")

    print("Simulation:")
    sim(n, k)
