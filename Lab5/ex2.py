import numpy as np
from fractions import Fraction
import argparse as argp
from itertools import product

def bruteforce(n: int) -> Fraction:
    def list_has_triple_ones(l) -> bool:
        for i in range(0, len(l) - 2):
            if l[i] and l[i + 1] and l[i + 2]:
                return True
        return False
    combinations = product([0, 1], repeat=n)
    comb_has_triple_ones = map(list_has_triple_ones, combinations)
    return Fraction(sum(comb_has_triple_ones), 2**n)

def formula(n: int) -> Fraction:
    if n < 3: return Fraction(0)
    probs = [Fraction(0), Fraction(0), Fraction(0), Fraction(1, 8)]
    for _ in range(4, n + 1):
        # P(n) = P(n - 1) + (1 - P(n - 4)) / 16
        # either there were already three ones, or there weren't, but it ended with 011, and the last digit was one
        already_was_true = probs[3]
        could_become_true_now = (1 - probs[0]) / 8
        became_true = could_become_true_now / 2
        probs = [probs[1], probs[2], probs[3], already_was_true + became_true]
    return probs[3]

def simulate(n: int, batches: int) -> Fraction:

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

    return Fraction(np.count_nonzero(any_in_batch), batches)

def print_frac(name: str, frac: Fraction):
    print(f"{name}: {frac} ~= {float(frac) * 100}%")

if __name__ == "__main__":
    ap = argp.ArgumentParser()
    ap.add_argument("-n", default=3, type=int)
    ap.add_argument("-b", "--batches", default=10_000, type=int)
    ap.add_argument("--always-bf", action='store_true')
    args = ap.parse_args()

    BRUTEFORCE_LIMIT = 20
    use_bruteforce = (args.n <= BRUTEFORCE_LIMIT) or (args.always_bf)

    print(f"Chance of {args.n} random bits containing 111:")

    if use_bruteforce:
        print_frac("Bruteforce", bruteforce(args.n))
    else:
        print(f"Bruteforce: (not using bruteforce, would be too slow for {args.n})")
    print_frac("Formula", formula(args.n))
    print_frac("Simulation", simulate(args.n, args.batches))
