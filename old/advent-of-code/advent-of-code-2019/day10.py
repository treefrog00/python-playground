from common import parse_args_and_get_input
from collections import Counter
from dataclasses import dataclass
from typing import List
import sys


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class AsteroidTarget:
    asteroid: Point
    gradient: float
    distance_sq: float
    is_rightwards_or_straight_up: bool

    # less than means "lower priority for destruction"
    def __lt__(self, other: 'AsteroidTarget'):
        if self.is_rightwards_or_straight_up and not other.is_rightwards_or_straight_up:
            return False
        if other.is_rightwards_or_straight_up and not self.is_rightwards_or_straight_up:
            return True

        if self.gradient == other.gradient:
            return self.distance_sq > other.distance_sq

        return self.gradient < other.gradient


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

    # is area of triangle equal to 0? (skipping multiplication by 0.5)
    return viewer.x * (target.y - asteroid.y) + target.x * (asteroid.y - viewer.y) + asteroid.x * (viewer.y - target.y) == 0


def parse_map(data: List[str]):
    asteroids = []
    station = None

    for y, line in enumerate(data):
        for x, symbol in enumerate(line):
            if symbol == '#':
                asteroids.append(Point(x, y))
            elif symbol == 'X':
                station = Point(x, y)
                asteroids.append(Point(x, y))  # to be consistent with maps where station is not included as an X

    return asteroids, station


def parse_test(data: str):
    return parse_map(data.strip().splitlines())


def check_for_block(asteroids, viewer, target):
    for potential_block in asteroids:
        if potential_block == target or potential_block == viewer:
            continue

        if asteroid_blocks_view(viewer, target, potential_block):
            return True

    return False


def test_part_one():
    part_one(parse_test(test1)[0])


def part_one(asteroids: List[Point]):
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

        count_by_viewer[viewer] = len(viewable)

    print(count_by_viewer.most_common(20))


def get_order_of_destruction(asteroids: List[Point], station: Point) -> List[AsteroidTarget]:
    gradients = []

    for asteroid in set(asteroids) - {station}:
        dx = asteroid.x - station.x
        if not dx:
            gradient = sys.maxsize
        else:
            gradient = (station.y - asteroid.y) / dx

        distance_sq = (station.x - asteroid.x)**2 + (station.y - asteroid.y)**2

        is_rightwards = asteroid.x > station.x
        is_straight_up = asteroid.x == station.x and asteroid.y < station.y

        gradients.append(
            AsteroidTarget(
                asteroid, gradient, distance_sq, is_rightwards or is_straight_up))

    remaining = sorted(gradients)

    last_grad = None
    index = -1

    destroy_order = []

    while remaining:
        possible = remaining[index]
        if possible.gradient != last_grad:
            destroy_order.append(remaining.pop(index))
        else:
            index -= 1

        last_grad = possible.gradient

        if abs(index) > len(remaining):
            index = -1
            last_grad = None

    return destroy_order


test1 = """
.#..#
.....
#####
....#
...##
"""

test_part_two_small_input = """
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##
"""

test_part_two_large_input = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.####X#####...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

test_part_two_small_expected_asteroid_order = {
    0: Point(8, 1),  # 1 in the explanatory map
    1: Point(9, 0),  # 2
    2: Point(9, 1),  # 3
    3: Point(10, 0),  # 4
    4: Point(9, 2),  # 5
    5: Point(11, 1),  # 6
    8: Point(15, 1),  # 9
    9: Point(12, 2),  # at this point in explanatory map, new map starting at 1
    10: Point(13, 2),  # 2
    11: Point(14, 2),  # 3
    12: Point(15, 2),  # 4
    13: Point(12, 3),  # 5
    14: Point(16, 4),  # 6
    15: Point(15, 4),  # 7
    16: Point(10, 4),  # 8
    17: Point(4, 4),  # 9
    18: Point(2, 4),  # at this point in explanatory map, new map starting at 1
    19: Point(2, 3),  # 2
    20: Point(0, 2),  # 3
    21: Point(1, 2),  # 4
    22: Point(0, 1),  # 5
    23: Point(1, 1),  # 6
    24: Point(5, 2),  # 7
    27: Point(6, 1),  # at this point in explanatory map, new map starting at 1
    28: Point(6, 0),  # 2
    29: Point(7, 0),  # 3
    30: Point(8, 0),  # 4
    31: Point(10, 1),  # 5
    32: Point(14, 0),  # 6
    33: Point(16, 1),  # 7
    34: Point(13, 3),  # 8
    35: Point(14, 3),  # 9
}

test_part_two_large_expected_asteroid_order = {
    0: Point(11, 12),
    1: Point(12, 1),
    2: Point(12, 2),
    9: Point(12, 8),
    19: Point(16, 0),
    49: Point(16, 9),
    99: Point(10, 16),
    198: Point(9, 6),
    199: Point(8, 2),
    298: Point(11, 1),
}


def test_part_two(go_large):
    if go_large:
        data, expected_order = test_part_two_large_input, test_part_two_large_expected_asteroid_order
    else:
        data, expected_order = test_part_two_small_input, test_part_two_small_expected_asteroid_order

    asteroids, station = parse_test(data)
    destroy_order = get_order_of_destruction(asteroids, station)

    for i, actual in enumerate(destroy_order):
        expected = expected_order.get(i)
        if not expected:
            continue
        if expected != actual.asteroid:
            print(f"{i} expected: {expected} actual {actual}")
            return


def part_two():
    asteroids, _ = parse_map(lines)
    destroy_order = get_order_of_destruction(asteroids, Point(x=30, y=34))
    two_hundrendth = destroy_order[199]
    answer = two_hundrendth.asteroid.x * 100 + two_hundrendth.asteroid.y
    print(answer)


if __name__ == "__main__":
    args, lines = parse_args_and_get_input()

    if args.part_one:
        asteroids, _ = parse_map(lines)
        part_one(asteroids)
    else:
        test_part_two(go_large=False)
        test_part_two(go_large=True)
        part_two()
