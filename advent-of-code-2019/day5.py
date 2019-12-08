from common import parse_args_and_get_input, assert_equal

from intcode import parse_program, IntComputer

args, lines = parse_args_and_get_input()

code_immutable = parse_program(lines)


def output(val):
    print("PRINT {}".format(val))


if args.part_one:
    code = list(code_immutable)
    _ = IntComputer(code, lambda: 1, output).run()
else:
    code = list(code_immutable)
    _ = IntComputer(code, lambda: 5, output).run()

