from math import factorial


students = 10
computers = 10
assert(computers >= students)
permutations = factorial(students) // factorial(students - computers)

print(f"{permutations} permutations")
