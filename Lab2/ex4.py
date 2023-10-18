from combinatorics import comb


def chances_of_special_amounts(normal, special, choice):
    assert((normal + special) >= choice)
    combs = [comb(special, i) * comb(normal, choice - i) for i in range(0, min(special, choice) + 1)]
    if special < choice: combs += [0 for _ in range(choice - special)]
    sum_combs = sum(combs)
    prob = [combs[i] / sum_combs for i in range(len(combs))]
    return (combs, prob)

if __name__ == "__main__":

    new = 13
    old = 7
    buy = 6

    (_combs, prob) = chances_of_special_amounts(new, old, buy)

    print(f"p(3 old out of 6) = {prob[3 - 1]:.2}")

    index_max_prob = max(range(len(prob)), key=prob.__getitem__)
    print(f"Most likely is {index_max_prob} old computers with p = {prob[index_max_prob]:.2}")
