import numpy as np

def main():
    gen = np.random.default_rng()
    np_batch_size = 10_000_000

    sum = 0
    count = 0

    def display_results():
        if count == 0:
            msg = "No data yet..."
        else:
            msg = f"{sum}/{count} = {sum/count}"
        print(msg)

    def rand_bools():
        bools = np.empty((2, np_batch_size), dtype=np.int64)
        bools[0, :] = gen.integers(0, 1 + 1, size=np_batch_size)
        bools[1, :] = 1 - bools[0, :]
        return bools

    def roll_4():
        return gen.integers(1, 4 + 1, size=np_batch_size, dtype=np.int64)

    def roll_6():
        return gen.integers(1, 6 + 1, size=np_batch_size, dtype=np.int64)

    def roll_interleaved(bools):
        r4 = roll_4()
        r6 = roll_6()
        r4 *= bools[0, :]
        r6 *= bools[1, :]
        r4 += r6
        return r4

    while True:
        display_results()

        bools = rand_bools()
        r1 = roll_interleaved(bools)
        r2 = roll_interleaved(bools)

        has_r1_equal_2 = r1 == 2
        valid_rolls = r2[has_r1_equal_2]

        sum += valid_rolls.sum()
        count += has_r1_equal_2.sum()

if __name__ == "__main__":
    main()
