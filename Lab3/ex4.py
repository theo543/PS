import numpy as np
from mpmath import mp, nstr
from math import inf
from sys import argv

def exact_formula(n, k):
    # (n! / (k!(n-k)!) / 2^n
    f = mp.factorial
    # arbitrary precision number
    return (f(n) / (f(k) * f(n - k))) / mp.power(2, n)

def sim(n: int, k: int, binomial: bool):
    trues = 0
    times = 0
    def log(end):
        print(f"p = {trues}/{times} = {trues/times:.10f}", end=end)
    try:
        gen = np.random.default_rng()
        bin_gen_size = 20_000_000
        while True:
            if binomial:
                counts = gen.binomial(n, 0.5, bin_gen_size)
                trues += np.count_nonzero(counts == k)
                times += bin_gen_size
            else:
                flips = gen.integers(0, high=1, size=n, dtype=bool, endpoint=True)
                if np.count_nonzero(flips) == k:
                    trues += 1
                times += 1
            log('\r')
    except KeyboardInterrupt:
        log('\n')

if __name__ == "__main__":
    n:int
    k:int
    binomial:bool

    try:
        parse_arg3 = {'-f': False, '-b': True}
        n = int(argv[1])
        k = int(argv[2])
        binomial = parse_arg3[argv[3]]
        print(f"n = {n}, k = {k}")
    except (IndexError, ValueError, KeyError):
        print("Usage: py ex4.py <n> <k> <-f (simulate flips with random bools)| -b (use np.random.binomial)>")
        exit(1)
    assert(n >= k)

    exact_result = exact_formula(n, k)
    print(f"exact formula => {nstr(exact_result, min_fixed=-50, max_fixed=inf)}")

    print("Simulation: " + ("(using np.random.binomial)" if binomial else "(using random bools)"))
    sim(n, k, binomial)
