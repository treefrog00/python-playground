import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--part-one', action='store_true')
    parser.add_argument('--part-two', action='store_true')
    return parser.parse_args()


def parse_args_and_get_input():
    args = parse_args()

    with open(args.input) as f:
        lines = f.read().splitlines()

    return args, lines


def assert_equal(expected, actual):
    assert expected == actual, "expected_answer {}, actual answer {}".format(
        expected, actual)
