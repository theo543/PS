import numpy as np
from fractions import Fraction
import argparse as argp
from itertools import product

def bruteforce(n: int, repeat_len: int) -> Fraction:
    def list_has_repeat(l) -> bool:
        for i in range(0, len(l) - repeat_len + 1):
            if all(l[i:(i+repeat_len)]):
                return True
        return False
    combinations = product([0, 1], repeat=n)
    comb_has_triple_ones = map(list_has_repeat, combinations)
    return Fraction(sum(comb_has_triple_ones), 2**n)

def formula(n: int, repeat_len: int) -> Fraction:
    if n < repeat_len: return Fraction(0)
    probs = [Fraction(0)] * repeat_len + [Fraction(1, 2) ** repeat_len]
    for _ in range(repeat_len + 1, n + 1):
        # P(n) = P(n - 1) + (1 - P(n - NUM_BITS_IN_REPEAT - 1)) * (1 / 2 ^ (NUM_BITS_IN_REPEAT + 1))
        # either there was already a repeat
        # or there wasn't, but the last digits were 01111...1, and then a 1 was added to the end
        # that requires (NUM_BITS_IN_REPEAT + 1) digits to have the exact right values
        already_was_true = probs[-1]
        could_become_true_now = (1 - probs[0]) / (2 ** repeat_len)
        became_true = could_become_true_now / 2
        probs = probs[1:] + [already_was_true + became_true]
    return probs[-1]

def simulate(n: int, batches: int, repeat_len: int) -> Fraction:

    gen = np.random.default_rng()

    rows = n + repeat_len - 1
    bits_padded = gen.integers(0, high=1, size=[rows, batches], dtype=bool, endpoint=True)
    bits_padded[n:rows, 0:batches] = False
    bits = bits_padded[0:n, 0:batches]
    repeat_at_position = bits.copy()
    for i in range(1, repeat_len):
        next_bit = bits_padded[i:(n + i), 0:batches]
        repeat_at_position &= next_bit
    any_in_batch = np.bitwise_or.reduce(repeat_at_position, axis=0)

    return Fraction(np.count_nonzero(any_in_batch), batches)

def print_frac(name: str, frac: Fraction):
    print(f"{name}: {frac} ~= {float(frac) * 100}%")

if __name__ == "__main__":
    ap = argp.ArgumentParser()
    ap.add_argument("-n", default=0, type=int)
    ap.add_argument("-rb", "--repeat-bits", default=4, type=int)
    ap.add_argument("-b", "--sim-batches", default=10_000, type=int)
    ap.add_argument("--always-bf", action='store_true')
    args = ap.parse_args()
    if args.n == 0: args.n = args.repeat_bits

    BRUTEFORCE_LIMIT = 20
    use_bruteforce = (args.n <= BRUTEFORCE_LIMIT) or (args.always_bf)

    print(f"Chance of {args.n} random bits containing {'1' * args.repeat_bits}:")

    if use_bruteforce:
        print_frac("Bruteforce", bruteforce(args.n, args.repeat_bits))
    else:
        print(f"Bruteforce: (not using bruteforce, would be too slow for {args.n})")
    print_frac("Formula", formula(args.n, args.repeat_bits))
    print_frac("Simulation", simulate(args.n, args.sim_batches, args.repeat_bits))
