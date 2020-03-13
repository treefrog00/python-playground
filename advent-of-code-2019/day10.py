from common import parse_args_and_get_input
from collections import Counter
from dataclasses import dataclass
from typing import List

test1 = """
.#..#
.....
#####
....#
...##
"""


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int


def get_line_params(point1: Point, point2: Point):
    dy = point2.y - point1.y
    dx = point2.x - point1.x
    m = dy / dx
    c = point1.y - m * point1.x

    return m, c


def asteroid_blocks_view(viewer: Point, target: Point, asteroid: Point):
    if asteroid.x > viewer.x and asteroid.x > target.x:
        return False

    if asteroid.y > viewer.y and asteroid.y > target.y:
        return False

    if asteroid.x < viewer.x and asteroid.x < target.x:
        return False

    if asteroid.y < viewer.y and asteroid.y < target.y:
        return False

    if viewer.x == target.x:
        return asteroid.x == viewer.x

    m, c = get_line_params(viewer, target)
    expected_y = m * asteroid.x + c
    return expected_y == asteroid.y


def parse_map(data: List[str]):
    asteroids = []

    for y, line in enumerate(data):
        for x, symbol in enumerate(line):
            if symbol == '#':
                asteroids.append(Point(x, y))

    return asteroids


def parse_test(data: str):
    return parse_map(data.strip().splitlines())


def check_for_block(asteroids, viewer, target):
    for potential_block in asteroids:
        if potential_block == target or potential_block == viewer:
            continue

        if asteroid_blocks_view(viewer, target, potential_block):
            return True

    return False


def test():
    part_one(parse_test(test1))


def part_one(asteroids):
    count_by_viewer = Counter()

    for viewer in asteroids:
        viewable = set(asteroids)
        viewable.remove(viewer)

        for target in asteroids:
            if target not in viewable:
                continue

            blocked = check_for_block(asteroids, viewer, target)
            if blocked:
                viewable.remove(target)

        #print(f"Viewable for viewer {viewer}: {len(viewable)}, {viewable}")
        count_by_viewer[viewer] = len(viewable)

    print(count_by_viewer.most_common(1)[0])


def part_two(asteroids, station):
    remaining = set(asteroids)

    while remaining:
        pass


args, lines = parse_args_and_get_input()

if args.part_one:
    part_one(parse_map(lines))
else:
    part_two(parse_map(lines), Point(x=19, y=5))
