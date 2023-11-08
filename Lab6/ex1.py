import argparse
from fractions import Fraction

# Return (chance you win if switch, chance you win if stay)
def monty_hall(n: int) -> tuple[Fraction, Fraction]:
    prob_switch = Fraction(0)
    prob_stay =   Fraction(0)
    for car in range(1, n + 1):
        for choice in range(1, n + 1):
            if choice != car:
                # Only one possibility: Monty keeps the car door closed, and opens all other unchosed doors.
                # We should switch to the car door.
                # Probability of this branch: 1/n * 1/n
                prob_switch += Fraction(1, n) * Fraction(1, n)
            else:
                # Monty has n - 1 doors he could leave closed.
                for other_choice in range(1, n + 1):
                    if other_choice == car:
                        continue
                    # In this branch, we should stay, since we already have the car.
                    # 1/n * 1/n * 1/(n-2) chance we got here.
                    prob_stay += Fraction(1, n) * Fraction(1, n) * Fraction(1, n - 1)
    return (prob_switch, prob_stay)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", default=3, type=int)
    args = ap.parse_args()
    assert(args.n >= 2)

    (switch, stay) = monty_hall(args.n)    
    print(f"P(win if switch) = {switch}, P(win if stay) = {stay}")

if __name__ == "__main__":
    main()
