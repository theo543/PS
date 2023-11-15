import numpy as np
from matplotlib import pyplot as plt
import argparse

def gen_distribution(distribution, size):
    vector = np.random.random((1, size))
    # partial sums
    bins = np.cumsum(distribution)
    assert(abs(bins[-1] - 1) <= 0.0001)
    indexes = np.digitize(vector, bins)
    return indexes[0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", default=10_000, type=int)
    ap.add_argument("-d", "--distribution", nargs="+", type=float, required=True)
    args = ap.parse_args()
    dist = args.distribution
    X = gen_distribution(dist, args.size)
    bins = [-0.5] + [p - 0.5 for p in range(1, len(dist) + 2)]
    ticks = range(len(dist))
    plt.hist(X, bins=bins, ec='black')
    plt.xticks(ticks)
    plt.show(block=True)

if __name__ == "__main__":
    main()
