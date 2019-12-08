from common import parse_args_and_get_input, assert_equal
from collections import defaultdict

COM = "COM"
SAN = "SAN"
YOU = "YOU"

def parse_lines(lines):
    return [l.split(")") for l in lines]


test_data = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""


def build_tree(orbits):
    tree = defaultdict(list)
    for t1, t2 in orbits:
        tree[t1].append(t2)
    return tree


def count_orbits(lines):
    tree = build_tree(lines)
    current_level = [COM]
    depth = 0
    count = 0

    while True:
        count += len(current_level * depth)
        current_level = [child for parent in current_level for child in tree[parent] if parent in tree]
        depth += 1
        if not current_level:
            return count


def get_path(tree, start, target):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in tree[vertex]:
            if next == target:
                return path
            else:
                stack.append((next, path + [next]))


def min_transfers(lines):
    tree = build_tree(lines)
    path1 = get_path(tree, COM, SAN)
    path2 = get_path(tree, COM, YOU)

    s = set(path2)

    common_ancestor = None
    for orbit in reversed(path1):
        if orbit in s:
            common_ancestor = orbit
            break

    if not common_ancestor:
        raise Exception()

    path3 = get_path(tree, common_ancestor, SAN)
    path4 = get_path(tree, common_ancestor, YOU)

    return len(path3) + len(path4) - 2


args, lines = parse_args_and_get_input()


if args.part_one:
    test_orbits = parse_lines([x for x in test_data.split("\n") if x])
    assert_equal(42, count_orbits(test_orbits))
    answer = count_orbits(parse_lines(lines))
else:
    answer = min_transfers(parse_lines(lines))

print(answer)

