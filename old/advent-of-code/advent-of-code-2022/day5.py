from common import parse_args_and_get_input

args, lines = parse_args_and_get_input()


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


line_break = lines.index("")
initial = lines[:line_break - 1]
move_lines = lines[line_break + 1:]

stacks = [[]]  # empty 0-indexed stack to be ignored

for offset in range(0, len(initial[0]), 4):
    stack = []
    for row in reversed(initial):
        val = row[offset+1:offset+2]
        if val != " ":
            stack.append(val)
    stacks.append(stack)

print(stacks)

moves = []
for line in move_lines:
    items = line.split()
    count = int(items[1])
    source = int(items[3])
    target = int(items[5])
    moves.append((count, source, target))

print(moves)

for count, source, target in moves:
    if args.part_one:
        for _ in range(count):
            item = stacks[source].pop()
            stacks[target].append(item)
    else:
        moved_crates = []
        for _ in range(count):
            moved_crates.insert(0, stacks[source].pop())
        stacks[target].extend(moved_crates)

print(stacks)
print("".join(s[-1] for s in stacks if s))