from fractions import Fraction

sensitivity = Fraction(98, 100)
specificity = Fraction(95, 100)
initial_prior_probability = Fraction(1, 1000)

# P(A|B) = P(A) * P(B|A) / P(B)
def bayes(A: Fraction, B_given_A: Fraction, B: Fraction) -> Fraction:
    return A * B_given_A / B

def update_after_positive(D_plus: Fraction) -> Fraction:
    A = D_plus
    # B|A = T+|D+ = sensitivity
    B_given_A = sensitivity
    # B = T+
    # P(T+) = P(D+) * P(T+|D+) + P(D-) * P(T+|D-)
    B = D_plus * sensitivity + (1 - D_plus) * (1 - specificity)
    return bayes(A, B_given_A, B)

def update_after_negative(D_plus: Fraction) -> Fraction:
    A = D_plus
    # B|A = T-|D+ = (1 - specificity)
    B_given_A = 1 - specificity
    # B = T-
    # P(T-) = P(D+) * P(T-|D+) + P(D-) * P(T-|D-)
    B = D_plus * (1 - sensitivity) + (1 - D_plus) * specificity
    return bayes(A, B_given_A, B)

def main():
    def print_frac(name: str, frac: Fraction):
        print(f"{name}: {frac} ~= {float(frac) * 10:.10f}")

    p_plus_minus = update_after_negative(update_after_positive(initial_prior_probability))
    print_frac("Positive test then negative test", p_plus_minus) # 490/474721 ~= 0.0103218522
    p_minus_minus = update_after_negative(update_after_negative(initial_prior_probability))
    print_frac("Two negative tests", p_minus_minus) # 1/360628 ~= 0.0000277294

if __name__ == "__main__":
    main()
