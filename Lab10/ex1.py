from fractions import Fraction
from argparse import ArgumentParser
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

def main():
    ap = ArgumentParser()
    ap.add_argument("-n", type=int, required=True)
    args = ap.parse_args()
    n = args.n
    if n < 3:
        print("Required: n >= 3")
        exit(1)
    print(f"Searching k using exact formula...")
    expected = n / e
    print(f"Expected exact k = [n/e] = round({expected:.2f}) = {round(expected)}")
    exact_k = exact_search(n)
    print(f"Got {exact_k}, diff from expected = {abs(exact_k - round(expected))}")

if __name__ == "__main__":
    main()
