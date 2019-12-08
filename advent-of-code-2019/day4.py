import argparse
from common import assert_equal

puzzle_input = ["245318", "765747"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--part-one', action='store_true')
    parser.add_argument('--part-two', action='store_true')
    return parser.parse_args()


def go(min_str, max_str, sequence_check):
    permutations = 0

    for i in range(int(min_str), int(max_str)):
        digits = [int(x) for x in str(i)]
        if digits == sorted(digits) and sequence_check(digits):
            permutations += 1

    return permutations


args = parse_args()

if args.part_one:
    def sequence_check(digits):
        return any(x == y for x, y in zip(digits, digits[1:]))
    answer = go(puzzle_input[0], puzzle_input[1], sequence_check)
else:
    def sequence_check(digits):
        padded_digits = [0] + digits + [0]
        return (
                any(one == two and one != before and two != after for before, one, two, after in zip(padded_digits, padded_digits[1:], padded_digits[2:], padded_digits[3:])))

    answer = go(puzzle_input[0], puzzle_input[1], sequence_check)

print(answer)
