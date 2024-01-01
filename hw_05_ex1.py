import numpy as np
from argparse import ArgumentParser
from matplotlib import pyplot as plt

def standard_normal_values(batches: int):
    gen = np.random.default_rng()


    U2_a = gen.random(size=batches)
    U2_a *= 2 * np.pi
    U2_b = U2_a.copy()
    np.cos(U2_a, out=U2_a)
    np.sin(U2_b, out=U2_b)

    U1 = gen.random(size=batches)
    np.log(U1, out=U1)
    U1 *= -2
    np.sqrt(U1, out=U1)
    U1 = np.tile(U1, 2)
    U1[:batches] *= U2_a
    U1[batches:] *= U2_b

    return U1

def standard_normal_density(points: int, start: int, stop: int):
    X = np.linspace(start, stop, num=points)
    Y = X.copy()

    np.square(Y, out=Y)
    Y /= -2
    np.exp(Y, out=Y)
    Y /= np.sqrt(2 * np.pi)

    return (X, Y)

def main():
    ap = ArgumentParser()
    ap.add_argument("--batches", type=int, default=30_000_000)
    ap.add_argument("--hist-bins", type=int, default=1_000)
    ap.add_argument("--density-points", type=int, default=1_000)
    args = ap.parse_args()

    values = standard_normal_values(args.batches)

    plt.hist(values, args.hist_bins, density=True)

    (density_x, density_y) = standard_normal_density(args.density_points, np.min(values), np.max(values))
    assert abs(np.trapz(density_y, x=density_x) - 1) <= 0.0001
    plt.plot(density_x, density_y)

    plt.show()

if __name__ == "__main__":
    main()
