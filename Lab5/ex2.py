import numpy as np
from fractions import Fraction

import argparse as argp

def formula(n: int) -> Fraction:
    return Fraction(-1)

def simulate(n: int, batches: int) -> int:
    if n < 3: return 0

    gen = np.random.default_rng()

    bits_padded = gen.integers(0, high=1, size=[n + 2, batches], dtype=bool, endpoint=True)
    rows = n + 2
    bits_padded[(rows-2):rows, 0:batches] = False
    bits = bits_padded[0:(rows - 2), 0:batches]
    next_bit = bits_padded[1:(rows - 1), 0:batches]
    next_next_bit = bits_padded[2:rows, 0:batches]
    all_three = bits.copy()
    all_three &= next_bit
    all_three &= next_next_bit
    any_in_batch = np.bitwise_or.reduce(all_three, axis=0)

    return np.count_nonzero(any_in_batch)

if __name__ == "__main__":
    ap = argp.ArgumentParser()
    ap.add_argument("-n", default=3, type=int)
    ap.add_argument("-b", "--batches", default=10_000, type=int)
    args = ap.parse_args()

    print(f"Chance of {args.n} random bits containing 111:")

    #exact_frac = formula(n)
    #print(f"Formula: {exact_frac} ~= {float(exact_frac) * 100}%")

    events = simulate(args.n, args.batches)
    print(f"Simulation: {events} / {args.batches} ~= {(events / args.batches) * 100}%")
