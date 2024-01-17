from argparse import ArgumentParser
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

def main():
    gen = np.random.default_rng()
    ap = ArgumentParser()
    ap.add_argument("--log", action="store_true", default=False)
    log = ap.parse_args().log
    chances = np.array([0.1, 0.1 + 0.4, 0.1 + 0.4 + 0.5])
    percents = np.array([1, 1 - 0.4, 1 + 0.5])
    batches = 10_000
    months = 12
    changes = gen.random((batches, months))
    changes = np.digitize(changes, chances)
    changes = percents[changes]
    changes = np.cumprod(changes, axis=1)
    if log:
        changes = np.log(changes)
    segs = []
    cmap = plt.get_cmap("hsv")
    colors = [cmap(rand) for rand in gen.random(batches)]
    for batch in changes:
        seg = [(1, 1)]
        for month, value in enumerate(batch):
            seg.append((month + 1, value))
        segs.append(seg)
    lc = LineCollection(segs, colors=colors, alpha=1/510)
    fig, [ax, ax_hist] = plt.subplots(2, 1)
    ax.set_xlabel("month")
    ax.set_ylabel("value")
    ax.set_xticks(range(0, months + 1))
    ax.set_ylim((round(np.min(changes)) - 1, round(np.max(changes)) + 1))
    ax.add_collection(lc)
    ax.plot([0, months], [1, 1], color="red", linestyle="dashed", zorder=100)
    ax_hist.hist(changes[:, -1], density=True)
    plt.show()
if __name__ == "__main__":
    main()
