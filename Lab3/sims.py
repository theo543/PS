import numpy as np
import matplotlib.pyplot as plt

def once_sim(probs, times=10_000):
    opts = list(range(1, len(probs) + 1))

    gen = np.random.default_rng()
    flips = gen.choice(opts, size=times, p=probs)
    count = np.bincount(flips)
    return count

def live_sim(probs, batch=1):
    opts = list(range(1, len(probs) + 1))
    labels = [str(x) for x in opts]

    fig, ax = plt.subplots()
    fig.show()
    gen = np.random.default_rng()

    total = None

    while plt.get_fignums():
        flips = gen.choice(opts, size=batch, p=probs)
        count = np.bincount(flips, minlength=len(probs) + 1)
        if total is None:
            total = list(count)[1:]
        else:
            total = [x + y for x, y in zip(total, list(count)[1:])]
        
        total_throws = sum(total)
        t = [x for x, y in zip(total, labels) if x != 0]
        l = [y for x, y in zip(total, labels) if x != 0]
        ax.clear()
        ax.pie(t, labels=l, autopct=lambda val: f"{round(val, 1)}% : ~{int(val * total_throws / 100)}")
        plt.pause(0.05)

fair_coin = [0.5, 0.5]
bad_coin  = [0.25, 0.75]

fair_dice = [1 / 6] * 6
bad_dice  = [3/9, 2/9, 0, 0, 2/9, 2/9]
