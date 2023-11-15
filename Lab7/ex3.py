import numpy as np
from matplotlib import pyplot as plt
import argparse

def gen_distribution(values, probabilities, size):
    vector = np.random.random((1, size))
    # partial sums
    bins = np.cumsum(probabilities)
    assert(abs(bins[-1] - 1) <= 0.0001)
    indexes = np.digitize(vector, bins)
    return values[indexes[0]]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", default=10_000, type=int)
    ap.add_argument("-v", "--values", nargs="+", type=float, required=True)
    ap.add_argument("-p", "--probabilities", nargs="+", type=float, required=True)
    args = ap.parse_args()
    vals = np.array(args.values)
    prob = np.array(args.probabilities)
    assert(len(vals) == len(prob))
    X = gen_distribution(vals, prob, args.size)

    plt.hist(X, ec='black')
    plt.show(block=True)

if __name__ == "__main__":
    main()
