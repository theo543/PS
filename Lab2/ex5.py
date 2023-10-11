from ex4 import chances_of_special_amounts

asi = 4
total = 52

(_combs, prob) = chances_of_special_amounts(total - asi, asi, 5)

print(f"p(3 asi) = {prob[3 - 1]:.2}")

index_max_prob = max(range(len(prob)), key=prob.__getitem__)
print(f"Most likely is {index_max_prob} asi with p = {prob[index_max_prob]:.2}")
