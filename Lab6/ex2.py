from fractions import Fraction

# P(A|B) = P(A) * P(B|A) / P(B)
def bayes(A: Fraction, B_given_A: Fraction, B: Fraction) -> Fraction:
    return A * B_given_A / B

def main():
    sensitivity = Fraction(95, 100)
    specificity = Fraction(98, 100)
    prevalence = Fraction(5, 100)
    # A = D+
    A = prevalence
    # B|A = T-|D+ = (1 - sensitivity)
    B_A = (1 - sensitivity)
    # B = T- = P(D+) * P(T-|D+) + P(D-) * P(T-|D-)
    B = prevalence * (1 - sensitivity) + (1 - prevalence) * specificity
    updated_probability = bayes(A, B_A, B)
    print(updated_probability)

if __name__ == "__main__":
    main()
