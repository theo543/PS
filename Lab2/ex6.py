from ex4 import chances_of_special_amounts
from combinatorics import comb

def verify_diff(normal, special, choice):
    (combs, probs) = chances_of_special_amounts(normal, special, choice)
    return sum(combs) - comb(normal + special, choice)

for total in range(1, 10):
    for normal in range(0, total + 1):
        special = total - normal
        for choice in range(1, total):
            assert((normal + special) >= choice)
            print(f"Diff between sum and formula w. normal = {normal}, special = {special}, choice = {choice} is diff = {verify_diff(normal, special, choice)}")

# ???
