from common import parse_args_and_get_input

args, lines = parse_args_and_get_input()

example_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".splitlines()

large_example = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""".splitlines()


def print_h_t(h, t):
    print(f"h {h}")
    print(f"t {t}")


def update_knot(front, back):
    if front[0] == back[0] and abs(front[1] - back[1]) > 1:
        col_change = 1 if front[1] > back[1] else -1
        return (back[0], back[1] + col_change)

    if front[1] == back[1] and abs(front[0] - back[0]) > 1:
        row_change = 1 if front[0] > back[0] else -1
        return (back[0] + row_change, back[1])

    if (abs(front[1] - back[1]) > 1 and front[0] != back[0]) or (abs(front[0] - back[0]) > 1 and front[1] != back[1]):
        row_change = 1 if front[0] > back[0] else -1
        col_change = 1 if front[1] > back[1] else -1
        return (back[0] + row_change, back[1] + col_change)

    return back
        
    
def part_one(motions):
    h = (0, 0)
    t = (0, 0)

    tail_seen = {(0,0)}

    for direction, distance in motions:
        print(f"direction {direction} distance {distance}")
        for _ in range(distance):
            print("move one")
            h = update_head(h, direction)
            t = update_knot(h, t)

            tail_seen.add(tuple(t))

        print(len(tail_seen))


def update_head(h, direction):
    if direction == "L":
        return (h[0], h[1] -1)

    elif direction == "R":
        return (h[0], h[1] +1)

    elif direction == "U":
        return (h[0] - 1, h[1])
    else:
        return (h[0] + 1, h[1])


def part_two(motions):
    knots = [(0,0)] * 10

    tail_seen = {(0, 0)}

    for direction, distance in motions:
        print(f"direction {direction} distance {distance}")
        for _ in range(distance):
            knots[0] = update_head(knots[0], direction)
            for i in range(1, len(knots)):
                knots[i] = update_knot(knots[i-1], knots[i])
            tail_seen.add(knots[-1])
        for i in range(len(knots)):
            print(f"new pos for knot {i}: {knots[i]}")
            print(f"seen {knots[-1]}")

    print(f"len: {len(tail_seen)}")


motions = [line.split(" ") for line in lines]
motions = [(m[0], int(m[1])) for m in motions]

if args.part_one:
    part_one(motions)
else:
    part_two(motions)
