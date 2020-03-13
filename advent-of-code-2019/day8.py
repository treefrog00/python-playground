from common import parse_args_and_get_input


width = 25
height = 6


def load_layers(data):
    layers = []

    for i in range(0, len(lines[0]), width * height):
        layers.append(data[i:i + width * height])

    return layers


def part_one(layers):
    min_zeros = min(layers, key=lambda x: x.count("0"))

    return min_zeros.count("1") * min_zeros.count("2")


def part_two(layers):
    layers.reverse()

    output = []
    for y in range(height):
        line = []
        for x in range(width):
            new_val = "X"

            for layer in layers:
                color = layer[y*width + x]
                if color == "1":
                    new_val = "X"
                elif color == "0":
                    new_val = " "

            line.append(new_val)

        output.append("".join(line))

    return "\n".join(output)


args, lines = parse_args_and_get_input()
data = lines[0]

if args.part_one:
    ans = part_one(load_layers(data))
else:
    ans = part_two(load_layers(data))

print(ans)

