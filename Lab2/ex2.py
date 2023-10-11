from combinatorics import perm

students = 10
computers = 10
assert(computers >= students)
print(f"{perm(computers, students)} permutations")
