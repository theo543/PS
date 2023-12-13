import numpy as np
from scipy.special import gammaln, comb
from matplotlib import pyplot as plt
from argparse import ArgumentParser
from time import time
from sys import argv
from os.path import basename

def poisson_values(λ: float, batches: int):
    gen = np.random.default_rng()

    # Generate values from uniform [0, 1] distribution until their product <= -λ
    # Do the multiplication in a logarithm to avoid underflow
    counts = np.zeros(batches)
    sums = np.log(gen.random(batches))
    final_counts = np.empty(batches)
    left = batches
    buf_multiply = np.empty(batches)
    buf_done = np.empty(batches, dtype=bool)
    while left:
        tmp = buf_multiply[:left]
        gen.random(left, out=tmp)
        np.log(tmp, out=tmp)
        sums += tmp
        done = buf_done.view()[:left]
        np.less_equal(sums, -λ, out=done)
        if np.any(done):
            nr_done = np.count_nonzero(done)
            final_counts[batches - left:batches - left + nr_done] = counts[done]
            np.bitwise_not(done, out=done)
            remaining = done # reuse buffer
            left -= nr_done
            counts[:left] = counts[remaining]
            counts = counts.view()[:left]
            sums[:left] = sums[remaining]
            sums = sums.view()[:left]
        counts += 1
    return final_counts

def poisson_mass(λ: float, start: int, stop: int):
    X = np.arange(start, stop + 1, 1)
    Y = X * np.log(λ)
    Y -= λ
    Y -= gammaln(X + 1)
    np.exp(Y, out=Y)
    return (X, Y)

def binomial_mass(n: int, p: float, min_val: int, max_val: int):
    X = np.arange(min_val, max_val + 1, 1)
    Y = comb(n, X)
    Y *= np.power(p, X)
    Y *= np.power(1 - p, n - X)
    return (X, Y)

def main():
    ap = ArgumentParser()
    ap.add_argument("--lambda", type=float, required=True, dest='λ')
    ap.add_argument("--batches", type=int, default=1_000_000)
    ap.add_argument("--binomial-n", type=int, default=None)
    args = ap.parse_args()

    start_time = time()
    vals = poisson_values(args.λ, args.batches)
    end_time = time()
    print(f'Time taken to run poisson_values: {end_time - start_time} seconds')

    min_val = int(np.min(vals))
    max_val = int(np.max(vals))                  
    plt.hist(vals, bins=range(min_val, max_val), density=True, label='Poisson Histogram')

    start_time = time()
    (X, Y) = poisson_mass(args.λ, min_val, max_val)
    end_time = time()
    print(f'Time taken to run poisson_mass: {end_time - start_time} seconds')
    plt.step(X, Y, label='Poisson PMF')

    if not (args.binomial_n is None):
        start_time = time()
        (X, Y) = binomial_mass(args.binomial_n, args.λ/args.binomial_n, min_val, max_val)
        end_time = time()
        print(f'Time taken to run binomial_mass: {end_time - start_time} seconds')
        plt.step(X, Y, label='Binomial PMF')

    plt.legend(loc='upper right')
    plt.title(' '.join([basename(argv[0])] + argv[1:]))
    plt.show()
if __name__ == "__main__":
    main()
