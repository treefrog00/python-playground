from common import parse_args_and_get_input, assert_equal
from collections import Counter
import re


def part_one(lines):
    def word_counts(w):
        c = Counter()
        for x in w:
            c[x] += 1
        return c

    counters = [word_counts(w) for w in lines]

    two_count = sum(1 for c in counters if any(x == 2 for x in c.values()))
    three_count = sum(1 for c in counters if any(x == 3 for x in c.values()))

    return two_count * three_count


def part_two(lines):
    for i in range(len(lines)):

        search_word = lines[i]
        needles = []
        for z in range(len(search_word)):
            needles.append("{}.{}".format(search_word[:z], search_word[z + 1:]))

        for j in range(i + 1, len(lines)):
            for n in needles:
                if re.match(n, lines[j]):
                    return n


args, lines = parse_args_and_get_input()

if args.part_one:
    answer = part_one(lines)
else:
    answer = part_two(lines)

print(answer)

