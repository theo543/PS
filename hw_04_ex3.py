import numpy as np
from scipy.special import factorial, gammaln
from matplotlib import pyplot as plt
from argparse import ArgumentParser

def poisson_values(λ: float, batches: int):
    gen = np.random.default_rng()

    # Poisson <=> generate add exponentials until > λ
    # log everything
    limit = np.exp(-λ)
    counts = np.zeros(batches)
    products = gen.random(batches)
    final_counts = np.empty(batches)
    left = batches
    buf_multiply = np.empty(batches)
    buf_done = np.empty(batches, dtype=bool)
    while left:
        tmp = buf_multiply[:left]
        gen.random(left, out=tmp)
        products *= tmp
        done = buf_done.view()[:left]
        np.less_equal(products, limit, out=done)
        nr_done = np.count_nonzero(done)
        final_counts[batches - left:batches - left + nr_done] = counts[done]
        np.bitwise_not(done, out=done)
        remaining = done # reuse buffer
        left -= nr_done
        counts[:left] = counts[remaining]
        counts = counts.view()[:left]
        counts += 1
        products[:left] = products[remaining]
        products = products.view()[:left]
    assert(np.size(final_counts) == batches)
    return final_counts

def poisson_mass(λ: float, start: int, stop: int):
    X = np.arange(start, stop + 1, 1)
    Y = X * np.log(λ)
    Y -= λ
    Y -= gammaln(X + 1)
    np.exp(Y, out=Y)
    return (X, Y)

def main():
    ap = ArgumentParser()
    ap.add_argument("--lambda", type=float, required=True, dest='λ')
    ap.add_argument("--batches", type=int, default=1_000_000)
    args = ap.parse_args()

    vals = poisson_values(args.λ, args.batches)
    min_val = int(np.min(vals))
    max_val = int(np.max(vals))                  
    plt.hist(vals, bins=range(min_val, max_val), density=True)

    (X, Y) = poisson_mass(args.λ, min_val, max_val)
    plt.step(X, Y)

    plt.show()

if __name__ == "__main__":
    main()
