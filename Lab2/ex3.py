from math import factorial

folders = 10
found = 3

combinations = factorial(folders) // (factorial(folders - found) * factorial(found))
print(f"{combinations} combinations")
