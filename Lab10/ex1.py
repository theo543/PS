from fractions import Fraction
from argparse import ArgumentParser
import numpy as np
from math import e

def exact_prob_n_k(n: int, k: int):
    sum = Fraction(0)
    for j in range(k + 1, n + 1):
        sum += Fraction(k, j - 1) * Fraction(1, n)
    return sum

def exact_search(n: int):
    assert(n >= 3)
    l = 1
    r = n
    while l != r:
        m = round((l + r) / 2)
        val = exact_prob_n_k(n, m)
        val_pv = exact_prob_n_k(n, m - 1)
        val_af = exact_prob_n_k(n, m + 1)
        if val_pv < val > val_af:
            l = m
            r = m
            break
        elif val_pv > val > val_af:
            r = m - 1
        else:
            l = m + 1
    return l

def vectorized_sim(n: int, k: int, batches: int) -> Fraction:
    gen = np.random.default_rng()
    range_arr = np.arange(1, n + 1)
    perms = np.repeat(range_arr[np.newaxis, :], batches, axis=0)
    gen.permuted(perms, axis=1, out=perms)
    look = perms[:, :k]
    choose = perms[:, k:]
    look_maxvals = np.max(look, axis=1).reshape((batches, 1))
    choices = np.zeros_like(choose, dtype=bool)
    choices_rows = np.arange(0, batches)
    choices_cols = (choose > look_maxvals).argmax(axis=1)
    choices[choices_rows, choices_cols] = True
    good_choices = choose == n
    correct_choices = choices & good_choices
    return Fraction(np.count_nonzero(correct_choices), batches)

def main():
    ap = ArgumentParser()
    ap.add_argument("-n", type=int, required=True)
    ap.add_argument("-b", "--batches", type=int, default=100_000)
    args = ap.parse_args()
    n = args.n
    batches = args.batches
    if n < 3:
        print("Required: n >= 3")
        exit(1)
    print(f"Searching k using exact formula...")
    expected = n / e
    print(f"Expected exact k = [n/e] = round({expected:.2f}) = {round(expected)}")
    exact_k = exact_search(n)
    print(f"Got {exact_k}, diff from expected = {abs(exact_k - round(expected))}")
    exact_prob = exact_prob_n_k(n, exact_k)
    print(f"Running simulation with k = {exact_k}")
    print(f"Expected prob = exact formula P(A_{exact_k}_{n}) = {float(exact_prob):.5f}")
    vectorized_prob = vectorized_sim(n, exact_k, batches)
    print(f"Got P(A_{exact_k}_{n}) = {float(vectorized_prob):.5f}")

if __name__ == "__main__":
    main()
