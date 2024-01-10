import numpy as np
from argparse import ArgumentParser

def main():
    ap = ArgumentParser()
    ap.add_argument("--length", type=float, default=1)
    ap.add_argument("--height", type=float, default=2)
    args = ap.parse_args()
    batches = 100_000_000
    height = args.height
    length = args.length
    total_samples = 0
    total_successes = 0
    def update_status(end='\r'):
        P = total_successes / total_samples
        print(f"{total_samples} samples, pi ~= {(2 * length) / (height * P)}", end=end)
    gen = np.random.default_rng()
    try:
        while True:
            stick_y = gen.random(size=batches)
            stick_y *= height / 2
            dy = gen.random(size=batches)
            dy *= np.pi
            np.sin(dy, out=dy)
            dy *= length * 1/2
            stick_y -= dy
            is_success = stick_y <= 0
            total_samples += batches
            total_successes += np.count_nonzero(is_success)
            update_status()
    except KeyboardInterrupt:
        update_status('\n')

if __name__ == "__main__":
    main()
