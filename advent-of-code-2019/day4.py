import argparse
from common import assert_equal

puzzle_input = ["245318", "765747"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--part-one', action='store_true')
    parser.add_argument('--part-two', action='store_true')
    return parser.parse_args()


def make_min_vals(min_str):
    min_vals = [int(x) for x in min_str]
    changed = False
    for x in range(1, len(min_vals)):
        if changed:
            min_vals[x] = min_vals[x - 1]
        else:
            changed = min_vals[x] < min_vals[x - 1]
            min_vals[x] = max(min_vals[x], min_vals[x - 1])
    return min_vals


def make_max_vals(max_str):
    max_vals = [int(x) for x in max_str]
    for index in range(len(max_vals) - 1):
        if max_vals[index] > max_vals[index + 1]:
            max_vals[index] = max_vals[index] - 1
            for index2 in range(index + 1, len(max_vals)):
                max_vals[index2] = 9

    return max_vals


def go(min_str, max_str, sequence_check):
    min_vals = make_min_vals(min_str)
    max_vals = make_max_vals(max_str)

    permutations = 0

    def digit_start(prev_digit, leftward_digit_increased, i):
        return prev_digit if leftward_digit_increased else min_vals[i]

    for digit1 in range(min_vals[0], 10):
        leftward_digit_increased = digit1 > min_vals[0]

        for digit2 in range(digit_start(digit1, leftward_digit_increased, 1), 10):
            leftward_digit_increased = leftward_digit_increased or digit2 > min_vals[1]

            for digit3 in range(digit_start(digit2, leftward_digit_increased, 2), 10):
                leftward_digit_increased = leftward_digit_increased or digit3 > min_vals[2]

                for digit4 in range(digit_start(digit3, leftward_digit_increased, 3), 10):
                    leftward_digit_increased = leftward_digit_increased or digit4 > min_vals[3]

                    for digit5 in range(digit_start(digit4, leftward_digit_increased, 4), 10):
                        leftward_digit_increased = leftward_digit_increased or digit5 > min_vals[4]

                        for digit6 in range(digit_start(digit5, leftward_digit_increased, 5), 10):
                            digits = [digit1, digit2, digit3, digit4, digit5, digit6]

                            if sequence_check(digits):
                                permutations += 1

                            if digits == max_vals:
                                return permutations


args = parse_args()

if args.part_one:
    def sequence_check(digits):
        return any(x == y for x, y in zip(digits, digits[1:]))

    assert_equal([3, 5, 5, 5, 5, 5], make_min_vals("352222"))
    assert_equal([2, 9, 9, 9, 9, 9], make_max_vals("322222"))
    assert_equal([2, 4, 5, 5, 5, 5], make_min_vals("245318"))
    assert_equal([6, 9, 9, 9, 9, 9], make_max_vals("765747"))
    assert_equal(1, go("299999", "299999", sequence_check))
    assert_equal(2, go("389999", "399999", sequence_check))
    assert_equal(3, go("388999", "399999", sequence_check))
    assert_equal(6, go("388888", "399999", sequence_check))
    assert_equal(11, go("378888", "399999", sequence_check))
    assert_equal(0, go("123456", "123457", sequence_check))
    assert_equal(1, go("123455", "123457", sequence_check))
    answer = go(puzzle_input[0], puzzle_input[1], sequence_check)
else:
    def sequence_check(digits):
        padded_digits = [0] + digits + [0]
        return (
                any(one == two and one != before and two != after for before, one, two, after in zip(padded_digits, padded_digits[1:], padded_digits[2:], padded_digits[3:]))
        )

    answer = go(puzzle_input[0], puzzle_input[1], sequence_check)

print(answer)
