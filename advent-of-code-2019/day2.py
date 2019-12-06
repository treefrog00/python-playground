from common import parse_args_and_get_input, assert_equal


def read_values(code, ins_pointer, count):
    vals = [code[index] for index in range(ins_pointer + 1, ins_pointer + count + 1)]
    new_pointer = ins_pointer + count + 1

    return vals, new_pointer


def run_code(code):
    ins_pointer = 0

    while True:
        op = code[ins_pointer]

        if op == 1:
            vals, ins_pointer = read_values(code, ins_pointer, 3)
            code[vals[2]] = code[vals[0]] + code[vals[1]]
        elif op == 2:
            vals, ins_pointer = read_values(code, ins_pointer, 3)
            code[vals[2]] = code[vals[0]] * code[vals[1]]
        elif op == 99:
            return code[0]


def match_then_map_output(desired_result):
    for noun in range(0, 99 + 1):
        for verb in range(0, 99 + 1):
            code = list(code_immutable)
            code[1] = noun
            code[2] = verb
            if run_code(code) == desired_result:
                return 100 * noun + verb

    return None


def map_state(code):
    run_code(code)
    return code


args, lines = parse_args_and_get_input()

code_immutable = tuple(int(x) for x in lines[0].split(","))

if args.part_one:
    assert_equal([30, 1, 1, 4, 2, 5, 6, 0, 99], map_state([1, 1, 1, 4, 99, 5, 6, 0, 99]))
    code = list(code_immutable)
    code[1] = 12
    code[2] = 2
    answer = run_code(code)
else:
    answer = match_then_map_output(19690720)

print(answer)
