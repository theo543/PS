import numpy as np
from fractions import Fraction

import argparse as argp

def formula(n: int) -> Fraction:
    return Fraction(-1)

def simulate(n: int, batches: int) -> int:
    if n < 3: return 0

    gen = np.random.default_rng()

    count = 0
    bits = gen.integers(0, high=1, size=n * batches + 2, dtype=bool, endpoint=True)
    bits[-1] = 0
    bits[-2] = 0
    next_bit = bits[1:-1]
    next_next_bit = bits[2:]
    three_repeats = np.copy(bits[:-2])
    three_repeats &= next_bit
    three_repeats &= next_next_bit

    is_not_last_two = np.repeat(True, n)
    is_not_last_two[-1] = 0
    is_not_last_two[-2] = 0
    is_not_last_two = is_not_last_two.repeat(batches)

    three_repeats &= is_not_last_two

    three_repeats_2d = three_repeats.reshape([batches, n], order='C')
    any_three_repeats = np.bitwise_or.reduce(three_repeats_2d, axis=1)
    count_any_three_repeats = np.count_nonzero(any_three_repeats)

    return count_any_three_repeats

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
