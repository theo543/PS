import random

def choice():
    return random.getrandbits(1)

def gen_case():
    return (choice(), choice())

def log(times_true, times_false):
        print(f"Times both female: {times_true}, not: {times_false} => {times_true / (times_true + times_false) * 100:.2f}")
# Cases:
# M M - rejected
# M F - no
# F M - rejected
# F F - yes
# p = 1 / 2
def sim_a():
    times_true = 0
    times_false = 0

    while True:
        case = gen_case()
        if not case[1]:
            # reject cases where older isn't female
            continue
        if case[0] == True:
            times_true += 1
        else:
            times_false += 1
        log(times_true, times_false)

# Cases:
# M M - rejected
# M F - no
# F M - no
# F F - yes
# p = 1 / 3
def sim_b():
    times_true = 0
    times_false = 0

    while True:
        case = gen_case()
        if not (case[0] or case[1]):
            # reject cases where neither is female
            continue
        if (case[0] and case[1]):
            times_true += 1
        else:
            times_false += 1
        log(times_true, times_false)

            
