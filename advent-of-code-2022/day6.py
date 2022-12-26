from common import parse_args_and_get_input

args, lines = parse_args_and_get_input()


tests = {
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 7,
    "bvwbjplbgvbhsrlpgdmjqwftvncz": 5,
    "nppdvjthqldpwncqszvftbrmjlhg": 6,
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 10,
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 11,
}


def find_marker(text, num_unique):
    iterables = [text[i:] for i in range(num_unique)]
    for i, chars in enumerate(zip(*iterables)):
        is_unique = len(set(chars)) == num_unique

        if is_unique:
            return i + num_unique


for test_input, expected in tests.items():
    result = find_marker(test_input, 4)
    assert result == expected

if args.part_one:
    print(find_marker(lines[0], 4))
else:
    print(find_marker(lines[0], 14))
