import numpy as np
from fractions import Fraction

from sys import argv

C1_1 = Fraction(6, 10)
C1_0 = Fraction(7, 10)
C2_1 = Fraction(8, 10)
C2_0 = Fraction(5, 10)
BIT_1= Fraction(7, 10)

def formula():

    # A = "received a 0 on both channels"
    # if the bit is 1 both must be wrong, else both must be right
    A = ((1 - C1_1) * (1 - C2_1)) * BIT_1 + (C1_0 * C2_0) * (1 - BIT_1)

    # A_and_B = "received a 0 on both channels and both channels correct"
    # the bit must be 0 and both channels must be right
    A_and_B = (1 - BIT_1) * C1_0 * C2_0

    # P(B | A) = P(A ∩ B) / P(A)
    B_given_A = (A_and_B) / A

    return B_given_A

def simulate(n: int) -> tuple[int, int]:
    gen = np.random.default_rng()

    def gen_bools(true_p):
        true_p = float(true_p)
        return gen.choice(a=[False, True], size=n, p=[1 - true_p, true_p])

    send_1_over_c1 = gen_bools(C1_1)
    send_0_over_c1 = gen_bools(C1_0)
    send_1_over_c2 = gen_bools(C2_1)
    send_0_over_c2 = gen_bools(C2_0)

    which_bit = gen_bools(BIT_1)

    # Bit is 1 but both channels failed.
    false_positive = np.count_nonzero(which_bit & ~send_1_over_c1 & ~send_1_over_c2)
    # Bit is 0 and both channels worked.
    true_positive = np.count_nonzero(~which_bit & send_0_over_c1 & send_0_over_c2)
    return (false_positive, true_positive)

if __name__ == "__main__":
    exact_frac = formula()
    print(f"Formula: {exact_frac} ~= {float(exact_frac) * 100}%")

    n = 10_000 if len(argv) == 1 else int(argv[1])
    (fp, tp) = simulate(n)
    print(f"Simulation: {tp} / ({fp} + {tp}) ~= {tp/(fp+tp) * 100}%")
