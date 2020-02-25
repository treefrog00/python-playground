from common import parse_args_and_get_input, assert_equal
from collections import Counter


def parse_lines(lines):
    no_ids = [line.split("@")[1] for line in lines]
    b = [((colon_split[0], colon_split[1]) for colon_split in line.split(":")) for line in no_ids]
    c = [(pos.split(","), size.split("x")) for pos, size in b]
    d = [((int(x) for x in pos), (int(y) for y in size)) for pos, size in c]
    #print(d)
    return d

def part_one(lines):
    pass


def part_two(lines):
    pass


args, lines = parse_args_and_get_input()

parse_lines(lines)

if args.part_one:
    answer = part_one(lines)
else:
    answer = part_two(lines)

print(answer)

