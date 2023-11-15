import numpy as np
from matplotlib import pyplot as plt
import argparse

def bernoulli(p: float, size: int) -> int:
    return binomial(1, p, size)

def binomial(n: int, p: float, size: int) -> int:
    matrix = np.random.random((n, size)) < p
    return np.sum(matrix, axis=0)

def geometric(p: float, size: int) -> int:
    batch_size = 100
    batch_max = 10000
    remaining = size
    found = np.array([])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--distribution", type=str, required=True)
    ap.add_argument("-p", default=0.5, type=float)
    ap.add_argument("-n", default=10, type=int)
    ap.add_argument("--size", default = 10_000, type=int)
    args = ap.parse_args()
    if args.distribution == "bernoulli":
        bins = [-0.5, 0.5, 1.5]
        ticks = [0, 1]
        X = bernoulli(args.p, args.size)
    elif args.distribution == "binomial":
        bins = [-0.5] + [p - 0.5 for p in range(1, args.n + 2)]
        ticks = range(args.n + 1)
        X = binomial(args.n, args.p, args.size)
    elif args.distribution == "geometric":
        pass
    else:
        print(f"Unknown distribution ${args.distribution}")
        exit(1)
    plt.hist(X, bins=bins, ec='black', density=True)
    plt.xticks(ticks)
    plt.show(block=True)

if __name__ == "__main__":
    main()
