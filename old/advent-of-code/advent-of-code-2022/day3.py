from functools import reduce
from string import ascii_lowercase, ascii_uppercase

from common import parse_args_and_get_input

args, lines = parse_args_and_get_input()

priority_lookup = {
    c: i + 1 for i, c in enumerate(ascii_lowercase + ascii_uppercase)
}


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if args.part_one:
    score = 0

    for line in lines:
        section_size = int(len(line) / 2)
        section_one = set(line[:section_size])
        section_two = set(line[section_size:])
        common = next(iter(section_one & section_two))
        score += priority_lookup[common]

    print(score)
else:
    score = 0

    for elf_team in chunks(lines, 3):
        sets = [set(elf) for elf in elf_team]
        common = next(iter(reduce(lambda x, y: x & y, sets)))
        score += priority_lookup[common]

    print(score)