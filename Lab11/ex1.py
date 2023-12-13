import numpy as np
from argparse import ArgumentParser
from matplotlib import pyplot as plt

def gen_continuous_exp(λ: float, batches: int):
    gen = np.random.default_rng()
    probs = gen.random(size=batches)

    # invert function
    probs -= 1
    probs *= -1
    np.log(probs, out=probs)
    probs /= -λ

    return probs

def continous_exp_density(λ: float, points: int, start: int, stop: int):
    X = np.linspace(start, stop, num=points)
    Y = X.copy()
    Y *= -λ
    np.exp(Y, out=Y)
    Y *= λ
    return (X, Y)

def main():
    ap = ArgumentParser()
    ap.add_argument("--lambda", type=float, required=True, dest="lambda_parameter")
    ap.add_argument("--batches", type=int, default=1_000_000)
    ap.add_argument("--hist-bins", type=int, default=1_000)
    ap.add_argument("--density-points", type=int, default=1_000)
    args = ap.parse_args()

    values = gen_continuous_exp(args.lambda_parameter, args.batches)
    plt.hist(values, args.hist_bins, density=True)

    (density_x, density_y) = continous_exp_density(args.lambda_parameter, args.density_points, np.min(values), np.max(values))
    plt.plot(density_x, density_y)

    plt.show()

if __name__ == "__main__":
    main()
