from common import parse_args_and_get_input

from intcode import parse_program, IntComputer

args, lines = parse_args_and_get_input()

code_immutable = parse_program(lines[0])


def output(val):
    print("PRINT {}".format(val))


if args.part_one:
    IntComputer(code_immutable, lambda: 1, output).run()
else:
    IntComputer(code_immutable, lambda: 5, output).run()

