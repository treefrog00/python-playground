from common import parse_args_and_get_input

from intcode import parse_program, IntComputer


def output(val):
    print("PRINT {}".format(val))


args, lines = parse_args_and_get_input()
code_immutable = parse_program(lines[0])

# takes no input and produces a copy of itself as output.
test1 = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"

test2 = "1102,34915192,34915192,7,4,7,99,0"  # should output a 16-digit number.

test3 = "104,1125899906842624,99"  # should output the large number in the middle.

#IntComputer(parse_program(test1), lambda: 1, output).run()
#IntComputer(parse_program(test2), lambda: 1, output).run()
#IntComputer(parse_program(test3), lambda: 1, output).run()

if args.part_one:
    IntComputer(code_immutable, lambda: 1, output).run()
else:
    IntComputer(code_immutable, lambda: 2, output).run()
