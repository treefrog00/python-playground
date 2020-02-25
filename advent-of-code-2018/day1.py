from common import parse_args_and_get_input, assert_equal
from collections import Counter


def part_two(lines):
    c = Counter()
    inputs = [int(x) for x in lines]
    i = 0
    freq = 0

    while True:
        freq = freq + inputs[i]
        c[freq] += 1

        if c[freq] == 2:
            return freq
        i = (i + 1) % len(inputs)


args, lines = parse_args_and_get_input()

if args.part_one:
    answer = sum([int(x) for x in lines])
else:
    assert_equal(14, part_two("+7, +7, -2, -7, -4".split(",")))
    answer = part_two(lines)

print(answer)

