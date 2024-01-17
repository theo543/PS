import random
from argparse import ArgumentParser
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

def main():
    ap = ArgumentParser()
    ap.add_argument("--left", type=float, default=1)
    ap.add_argument("--right", type=float, default=1)
    ap.add_argument("--none", type=float, default=0)
    args = ap.parse_args()
    left = args.left
    right = left + args.right
    none = right + args.none
    plt.ion()
    fig, [ax_traj, ax_hist] = plt.subplots(2, 1)
    ax_traj.set_xlim([-10, 10])
    ax_traj.set_ylim([1, 10])
    ax_traj.set_xlabel("location")
    ax_traj.set_ylabel("time")
    ax_traj.set_xticks(range(-10, 10 + 1))
    ax_traj.set_yticks(range(1, 10 + 1))
    ax_traj.invert_yaxis()
    ax_hist.set_xlim([-10, 10])
    ax_hist.set_xticks(range(-10, 10 + 1))
    fig.tight_layout(pad=1.5)
    current_x = 0
    current_t = 1
    final_positions = []
    cmap = plt.get_cmap("hsv")
    seg = [[0, 1]]
    segs = []
    colors = []
    last_traj = None
    last_hist = None
    while plt.fignum_exists(fig.number) and len(final_positions) < 10_000:
        choice = random.random() * none
        if choice < left:
            current_x -= 1
        elif choice < right:
            current_x += 1
        else:
            pass
        current_t += 1
        seg += [[current_x, current_t]]
        if current_t == 10:
            final_positions.append(current_x)
            segs.append(seg)
            colors.append(cmap(random.random()))
            current_x = 0
            current_t = 1
            seg = [[0, 1]]
            if len(final_positions) % 500 == 0:
                if last_traj is not None:
                    last_traj.remove()
                if last_hist is not None:
                    for bin in last_hist:
                        bin.remove()
                ax_traj.title.set_text(f"trajectories: {len(final_positions)}")
                col = LineCollection(segs, colors=colors, alpha=0.01)
                last_traj = ax_traj.add_collection(col)
                bin_edges = [i - 0.5 for i in range(-10, 10 + 2)]
                _, _, last_hist = ax_hist.hist(final_positions, bin_edges, density=True, color="blue", width=1, edgecolor="black")
                plt.pause(0.01)
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()
