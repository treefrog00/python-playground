from common import parse_args_and_get_input, assert_equal
from dataclasses import dataclass
from functools import reduce


"""
It would be more efficient to store segments as start + end points and calculate interception points using geometry,
but this dumb approach of storing all the points works
"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def map_wires(lines):
    return [l.split(",") for l in lines]


def get_points(wire):
    def map_segment(points, segment):
        dir = segment[0]
        count = int(segment[1:])

        funcs = {
            "U": lambda p: Point(p.x, p.y + 1),
            "D": lambda p: Point(p.x, p.y - 1),
            "L": lambda p: Point(p.x + 1, p.y),
            "R": lambda p: Point(p.x - 1, p.y)
        }
        for _ in range(count):
            prev = points[-1]
            points.append(funcs[dir](prev))

        return points

    return reduce(map_segment, wire, [Point(0, 0)])


def intersections(points):
    intersects = set(points[0]).intersection(points[1])
    intersects.remove(Point(0,0))
    return intersects


def closest_intersection(wires):
    points = [get_points(w) for w in wires]
    return min(abs(p.x) + abs(p.y) for p in intersections(points))


def min_total_steps(wires):
    points = [get_points(w) for w in wires]
    intersects = intersections(points)

    return min(points[0].index(intersect) + points[1].index(intersect) for intersect in intersects)


args, lines = parse_args_and_get_input()

if args.part_one:
    test_wires = map_wires(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"])
    assert_equal(159, closest_intersection(test_wires))
    answer = closest_intersection(map_wires(lines))
else:
    test_wires = map_wires(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"])
    assert_equal(610, min_total_steps(test_wires))
    answer = min_total_steps(map_wires(lines))


print(answer)

