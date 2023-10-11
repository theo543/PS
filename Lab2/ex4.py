from combinatorics import comb

new = 13
old = 7
buy = 6

combs = [comb(old, o) * comb(new, buy - o) for o in range(1, min(old, buy) + 1)]
sum_combs = sum(combs)
prob = [combs[i] / sum_combs for i in range(len(combs))]

print(f"p(3 old out of 6) = {prob[3 - 1]:.2}")

index_max_prob = max(range(len(prob)), key=prob.__getitem__)
print(f"Most likely is {index_max_prob + 1} old computers with p = {prob[index_max_prob]:.2}")
