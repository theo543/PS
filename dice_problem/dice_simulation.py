import numpy as np

def main():
    gen = np.random.default_rng()
    np_batch_size = 10_000_000

    sum = 0
    count = 0

    dice = np.array([4, 6])

    def roll(max_val):
        return gen.integers(low=np.repeat([1], np_batch_size), high=max_val+1, size=np_batch_size)

    def display_results():
        if count == 0:
            msg = "No data yet..."
        else:
            msg = f"{sum}/{count} = {sum/count}"
        print(msg)

    while True:
        display_results()

        choice = dice[gen.integers(0, len(dice), size=np_batch_size)]

        r1 = roll(choice)
        r2 = roll(choice)

        has_r1_equal_2 = r1 == 2
        valid_rolls = r2[has_r1_equal_2]
        
        sum += valid_rolls.sum()
        count += has_r1_equal_2.sum()

if __name__ == "__main__":
    main()
