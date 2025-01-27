from collections import deque
from dataclasses import dataclass
from pprint import pprint
from typing import List

from common import parse_args_and_get_input

args, lines = parse_args_and_get_input()

example = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".splitlines()


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

@dataclass
class Monkey:
    monkey_id: int
    items: List[int]
    operation: List[str]
    test: str
    if_true: int
    if_false: int


def parse_target_monkey(line):
    return int(line.split(":")[1].strip().split()[-1])

def parse_monkey(line):
    monkey_id = int(line[0].split()[1][:-1])
    items = [int(x) for x in line[1].split(":")[1].split(",")]
    operation = [x.strip() for x in line[2].split("=")[1].split()]
    test = line[3].split(":")[1].strip()
    if_true = parse_target_monkey(line[4])
    if_false = parse_target_monkey(line[5])
    return Monkey(monkey_id, items, operation, test, if_true, if_false)


def parse_lines(lines):
    return [parse_monkey(m) for m in chunks(lines, 7)]


def part_one(monkeys):

    for round in range(20):
        for monkey in monkeys:
            for item in monkey.items:
                # modify worry level with operation
                # reduce worry
                # test worry level
                # throw item
        
        for monkey in monkeys:
            print(f"monkey {monkey.monkey_id} {monkey.items")



monkeys = parse_lines(example)

if args.part_one:
    part_one(monkeys)