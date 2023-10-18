import numpy as np

# needs proof
def sim(n, k):
    assert(k <= n)

    gen = np.random.default_rng()
    trues = 0
    times = 0
    while True:
        times += 1
        flips = gen.random(n) > 0.5
        counts = np.bincount(flips, minlength=2)
        if counts[1] == k:
            trues += 1
        print(f"p = {trues}/{times} = {trues/times * 100:.2f}%")
