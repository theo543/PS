import numpy as np
from scipy.special import comb
from argparse import ArgumentParser
from matplotlib import pyplot as plt
from os.path import basename
from sys import argv

def hypergeom_values(N: int, K: int, n: int, batches: int):
    gen = np.random.default_rng()

    k = np.arange(0, N+1, 1)
    pmf = comb(K, k) * comb(N - K, n - k) / comb(N, n)
    assert(1.001 > pmf.sum() > 0.999)
    cdf = np.cumsum(pmf)
    probs = gen.random(batches)
    values = np.digitize(probs, cdf)

    return values

def hypergeom_mass(N: int, K: int, n: int, start: int, stop: int):
    X = list(range(start, stop + 1))
    Y = [np.math.comb(K, k) * np.math.comb(N - K, n - k) / np.math.comb(N, n) for k in X]
    return (X, Y)

def main():
    ap = ArgumentParser()
    ap.add_argument("-N", type=int, required=True)
    ap.add_argument("-K", type=int, required=True)
    ap.add_argument("-n", type=int, required=True)
    ap.add_argument("--batches", type=int, default=1_000_000)
    args = ap.parse_args()

    vals = hypergeom_values(args.N, args.K, args.n, args.batches)
    bins = list(range(0, args.n))
    plt.hist(vals, bins=bins, density=True, label='Hypergeometric Histogram')

    (X, Y) = hypergeom_mass(args.N, args.K, args.n, np.min(vals), np.max(vals))
    plt.step(X, Y, where='post', label='Hypergeometric PMF')

    plt.title(' '.join([basename(argv[0])] + argv[1:]))
    plt.legend(loc='upper left')
    plt.show()

if __name__ == "__main__":
    main()
