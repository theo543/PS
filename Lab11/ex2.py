import numpy as np
from argparse import ArgumentParser
from matplotlib import pyplot as plt

def gen_cauchy(x_0: float, gamma: float, batches: int):
    gen = np.random.default_rng()
    probs = gen.random(size=batches)

    # invert function
    probs -= 1/2
    probs *= np.pi
    np.tan(probs, out=probs)
    probs *= gamma
    probs += x_0

    return probs

def cauchy_density(x0: float, gamma: float, points: int, start: int, stop: int):
    X = np.linspace(start, stop, num=points)
    Y = X.copy()

    Y -= x0
    Y /= gamma
    np.square(Y, out=Y)
    Y += 1
    Y *= np.pi * gamma
    np.reciprocal(Y, out=Y)

    return (X, Y)

def main():
    ap = ArgumentParser()
    ap.add_argument("--gamma", type=float, required=True)
    ap.add_argument("--x0", type=float, required=True)
    ap.add_argument("--batches", type=int, default=1_000_000)
    ap.add_argument("--hist-bins", type=int, default=1_000)
    ap.add_argument("--density-points", type=int, default=1_000)
    ap.add_argument("--percentile-range", type=float, default=99)
    args = ap.parse_args()

    values = gen_cauchy(args.x0, args.gamma, args.batches)
    # filter outliers
    hist_right = np.percentile(values, args.percentile_range)
    hist_left = np.percentile(values, 100 - args.percentile_range)
    values = values[(values >= hist_left) & (values <= hist_right)]

    plt.hist(values, args.hist_bins, density=True)

    (density_x, density_y) = cauchy_density(args.x0, args.gamma, args.density_points, np.min(values), np.max(values))
    plt.plot(density_x, density_y)

    plt.show()

if __name__ == "__main__":
    main()
