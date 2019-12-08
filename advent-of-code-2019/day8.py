from common import parse_args_and_get_input, assert_equal


args, lines = parse_args_and_get_input()


def part_one(data):
    width = 25
    height = 6
    layers = []

    for i in range(0, len(lines[0]), width * height):
        layers.append(data[i:i + width * height])

    min_zeros = min(layers, key=lambda x: x.count("0"))

    return min_zeros.count("1") * min_zeros.count("2")


data = lines[0]
if args.part_one:
    ans = part_one(data)
else:
    ans = 0

print(ans)

