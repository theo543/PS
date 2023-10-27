import numpy as np

# Cases:
# M M - 0
# M F - 1
# F M - 2
# F F - 3

# 0, 2 rejected
# 1 no
# 3 yes
# p = 1/2 = 0.5
def cases_with_second_is_f(counts):
    no = counts[0]
    yes = counts[2]
    return yes / (no + yes)

# 0 rejected
# 1, 2 no
# 3 yes
# p = 1 / 3 = 0.(3)
def cases_with_at_least_one_f(counts):
    no = counts[0] + counts[1]
    yes = counts[2]
    return yes / (no + yes)

def sim(n):
    cases = np.random.randint(0, 3 + 1, size=n)
    counts = np.bincount(cases, minlength=4)
    prob_1 = cases_with_second_is_f(counts)
    prob_2 = cases_with_at_least_one_f(counts)
    print(f"Result for case 1: {prob_1}")
    print(f"Result for case 2: {prob_2}")

if __name__ == "__main__":
    n = int(input("n = "))
    sim(n)
