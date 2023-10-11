from typing import Tuple


lowercase = 26
uppercase = 26
digits = 10
length = 8

def human_readable(seconds):
    conversions = [(60, 'minutes'), (60, 'hours'), (24, 'days'), (7, 'weeks'), (4, 'months'), (12, 'years'), (100, 'centuries'), (10, 'millenia')]
    name = 'seconds'
    total = seconds
    for (factor, new_name) in conversions:
        if total > factor:
            total /= factor
            name = new_name
        else: break
    return (total, name)

def stats(letter_kinds):
    total = sum(letter_kinds) ** length
    per_sec = 1_000_000
    to_crack = total / per_sec
    (time, name) = human_readable(to_crack)
    print(f"{to_crack:.2f} seconds = {time:.1f} {name}")
    secs_in_week = 60 * 60 * 24 * 7
    percent = min(1, secs_in_week / to_crack)
    print(f"{percent * 100:.2f}% chance in a week")

print("With uppercase:")
stats([lowercase, uppercase, digits])
print("Without uppercase:")
stats([lowercase, digits])
