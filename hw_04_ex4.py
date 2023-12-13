import numpy as np
from argparse import ArgumentParser
from matplotlib import pyplot as plt

def hypergeom_values(N: int, K: int, n: int, batches: int):
    gen = np.random.default_rng()

    deck = np.zeros((1, N), dtype=np.bool_)
    deck[0, :K] = True
    deck = np.repeat(deck, batches, axis=0)
    gen.permuted(deck, axis=1, out=deck)
    drawn = deck[:, :n]
    values = np.count_nonzero(drawn, axis=1)

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
    plt.hist(vals, bins=bins, density=True)

    (X, Y) = hypergeom_mass(args.N, args.K, args.n, np.min(vals), np.max(vals))
    plt.step(X, Y, where='post')

    plt.show()

if __name__ == "__main__":
    main()
