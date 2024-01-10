import numpy as np
from argparse import ArgumentParser
from matplotlib import pyplot as plt

def gen_values(λ: float, N: int, batches: int):
    gen = np.random.default_rng()

    probs = gen.random(size=(batches, N))
    probs -= 1
    probs *= -1
    np.log(probs, out=probs)
    probs /= -λ

    sums = np.add.reduce(probs, axis=1)
    sums /= N

    return sums

def normal_density(mean: float, standard_dev: float, points: int, start: int, stop: int):
    X = np.linspace(start, stop, num=points)
    Y = X.copy()

    Y -= mean
    Y /= standard_dev
    np.square(Y, out=Y)
    Y /= -2
    np.exp(Y, out=Y)
    Y /= standard_dev * np.sqrt(2 * np.pi)

    return (X, Y)

def main():
    ap = ArgumentParser()
    ap.add_argument("-N", type=int, default=10)
    ap.add_argument("--lambda", type=float, default=1, dest='λ')
    ap.add_argument("--batches", type=int, default=1_000_000)
    ap.add_argument("--hist-bins", type=int, default=1_000)
    ap.add_argument("--density-points", type=int, default=1_000)
    args = ap.parse_args()

    values = gen_values(args.λ, args.N, args.batches)
    mean = np.average(values)
    variance = np.var(values)

    plt.title(f"Mean: {mean}\nVariance: {variance}")
    plt.hist(values, args.hist_bins, density=True, label="Histogram")

    (density_x, density_y) = normal_density(mean, np.sqrt(variance), args.density_points, np.min(values), np.max(values))
    #assert abs(np.trapz(density_y, x=density_x) - 1) <= 0.0001
    plt.plot(density_x, density_y, label="PDF")
    plt.legend()

    plt.show()

if __name__ == "__main__":
    main()
