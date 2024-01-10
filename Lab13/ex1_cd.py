from matplotlib import pyplot as plt
from random import random
import math
import time

def main():
    height = 2
    width = 10
    length = 1
    half_length = 0.5
    total_samples = 0
    total_successes = 0
    ax = plt.gca()
    ax.set_xlim([-length, width + length])
    ax.set_ylim([-length, height + length])
    plt.plot([0, width], [0, 0])
    plt.plot([0, width], [height, height])
    plt.plot([0, 0], [0, height])
    plt.plot([width, width], [0, height])
    plt.show(block=False)
    while plt.get_fignums():
        cx = random() * width
        cy = random() * height
        angle = random() * math.pi
        dx = half_length * math.cos(angle)
        dy = half_length * math.sin(angle)
        ax = cx - dx
        ay = cy - dy
        bx = cx + dx
        by = cy + dy
        success = (ay < 0 and by > 0) or (ay < height and by > height)
        total_samples += 1
        total_successes += success
        color = 'red' if success else 'black'
        plt.plot([ax, bx], [ay, by], color=color)
        if total_successes > 0:
            title = f"pi ~= {total_samples / total_successes:.10f}"
            plt.title(title, fontname='monospace')
        plt.pause(0.01)

if __name__ == "__main__":
    main()
