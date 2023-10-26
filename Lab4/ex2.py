from matplotlib import pyplot as plt
import numpy as np

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
    n = int(input("n = "))
    a = float(input("a = "))
    b = float(input("b = "))
    sim(n, a, b)
