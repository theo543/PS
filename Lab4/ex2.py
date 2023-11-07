from matplotlib import pyplot as plt
import numpy as np
import argparse

def sim(n, a, b):
    rand = np.random.uniform(0, 1, size=n)
    in_range = np.count_nonzero(((rand > a) & (rand < b)))
    ratio = in_range / n
    print(f"result = {in_range} / {n} = {ratio}")
    print(f"expected = {b} - {a} = {b - a}")
    fig, ax = plt.subplots()
    range = f"[{a}, {b}]"
    ax.pie([1 - ratio, ratio], labels=[f"x ~E {range}", f"x E {range}"], autopct=lambda val: f"{val/100:.5f}")
    plt.show(block=True,)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("a", type=float)
    ap.add_argument("b", type=float)
    args = ap.parse_args()
    assert(0 <= args.a < args.b <= 1)
    sim(args.n, args.a, args.b)
