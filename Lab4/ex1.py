import numpy as np
import random
import timeit

DICE = np.array([[2, 2, 2, 5, 5, 5], [3, 3, 3, 3, 3, 6], [1, 4, 4, 4, 4, 4]])
DICE_NAMES = ["red", "green", "black"]
STRAGEGIES = [(0, 1), (0, 2), (1, 2), (1, 0), (2, 0), (2, 1)]
NR_SAMPLES_PER_STRATEGY = 1_000_000

vectorize = True

def try_strategy_nonvectorized(P1 : int, P2 : int) -> float:
    # without numpy
    P1_dice = DICE[P1]
    P2_dice = DICE[P2]
    P1_rolls = [random.choice(P1_dice) for _ in range(NR_SAMPLES_PER_STRATEGY)]
    P2_rolls = [random.choice(P2_dice) for _ in range(NR_SAMPLES_PER_STRATEGY)]
    times_P1_wins = 0
    for i in range(NR_SAMPLES_PER_STRATEGY):
        times_P1_wins += (P1_rolls[i] > P2_rolls[i])
    return times_P1_wins / NR_SAMPLES_PER_STRATEGY

def try_strategy(P1 : int, P2 : int) -> float:
    rng = np.random.default_rng()
    P1_rolls = rng.choice(DICE[P1], size=NR_SAMPLES_PER_STRATEGY)
    P2_rolls = rng.choice(DICE[P2], size=NR_SAMPLES_PER_STRATEGY)
    times_P1_wins = np.count_nonzero(P1_rolls > P2_rolls)

    return times_P1_wins / NR_SAMPLES_PER_STRATEGY

def print_result(P1_prob : float, P1 : int, P2 : int):
    print(f"P1 chooses dice '{DICE_NAMES[P1]}'={DICE[P1]}. P2 chooses '{DICE_NAMES[P2]}'={DICE[P2]}.")
    print(f"P1's chances of winning are {P1_prob} assuming both players play optimally.")


def run_simulations(try_strategy_func):
    res_for : list[float] = [999999] * 3
    P2_choice : list[int] = [-1] * 3
    for strategy in STRAGEGIES:
        (P1, P2) = strategy
        res = try_strategy_func(P1, P2)
        print_result(res, P1, P2)
        P1_prob = res
        current = res_for[P1]
        # P2 will choose the second dice to minimize P for P1's choice
        if current > P1_prob:
            res_for[P1] = res
            P2_choice[P1] = P2
    (best_P, (best_P1, best_P2)) = max(zip(res_for, zip(range(3), P2_choice)), key=lambda r: r[0])
    print("Best strategy:")
    print_result(best_P, best_P1, best_P2)

if __name__ == "__main__":
    start = timeit.default_timer()
    run_simulations(try_strategy)
    print(f"Vectorized runtime = {timeit.default_timer() - start} seconds\n")

    start = timeit.default_timer()
    run_simulations(try_strategy_nonvectorized)
    print(f"Non-vectorized runtime = {timeit.default_timer() - start} seconds\n")
