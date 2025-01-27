from collections import deque

from common import parse_args_and_get_input

args, lines = parse_args_and_get_input()

small_example = """noop
addx 3
addx -5""".splitlines()

large_example = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop""".splitlines()


def parse_instruction(line):
    parts = line.split()
    if parts[0] == "addx":
        parts[1] = int(parts[1])

    return parts


def part_one(lines):
    ins_queue = deque(map(parse_instruction, lines))
    register_queue = deque()
    cycle = 1
    X = 1
    saves = []
    stack_value = 0

    while ins_queue:
        print(f"start of cycle {cycle} value {X}")
        if (cycle - 20) % 40 == 0:
            print(f"cycle {cycle} value {X}")
            saves.append(X * cycle)

        if not register_queue:
            ins = ins_queue.popleft()
            if ins[0] == "addx":
                register_queue.append(ins[0])
                stack_value = ins[1]
        else:
            ins = register_queue.popleft()
            if ins == "addx":
                X += stack_value

        cycle += 1

    print(saves)
    print(sum(saves))


def part_two(lines):
    ins_queue = deque(map(parse_instruction, lines))
    register_queue = deque()
    cycle = 1
    X = 1
    stack_value = 0
    crt = [[]]

    while ins_queue:
        crt_col = (cycle - 1) % 40
        print(f"start of cycle {cycle} value {X} crt col {crt_col}")

        if crt_col - 1 <= X <= crt_col + 1:
            crt[-1].append("#")
        else:
            crt[-1].append(".")

        if cycle % 40 == 0:
            crt.append([])

        if not register_queue:
            ins = ins_queue.popleft()
            if ins[0] == "addx":
                register_queue.append(ins[0])
                stack_value = ins[1]
        else:
            ins = register_queue.popleft()
            if ins == "addx":
                X += stack_value

        cycle += 1

    for row in crt:
        print("".join(row))


if args.part_one:
    part_one(large_example)
else:
    part_two(lines)

