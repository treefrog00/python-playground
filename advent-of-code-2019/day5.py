from common import parse_args_and_get_input, assert_equal


class Op:
    add = 1
    mult = 2
    inp = 3
    outp = 4
    jit = 5
    jif = 6
    lt = 7
    equals = 8
    halt = 99


def get_modes(strop, value_count):
    return list(reversed([int(x) for x in strop[:-2].zfill(value_count)]))


def run_code(code, on_input, on_output):
    ins_pointer = 0

    def read_values(ins_pointer, count):
        vals = [code[index] for index in range(ins_pointer + 1, ins_pointer + count + 1)]
        new_pointer = ins_pointer + count + 1

        return vals, new_pointer

    def get_params(vals, count):
        modes = get_modes(strop, count)

        def get_param(index):
            if modes[index] == 0:
                return code[vals[index]]
            if modes[index] == 1:
                return vals[index]

        return [get_param(i)for i in range(count)]

    while True:
        op_value = code[ins_pointer]
        strop = str(op_value)

        if op_value <= 99:
            op = op_value
        else:
            op = int("".join(strop[-2:]))

        if op == Op.add:
            vals, ins_pointer = read_values(ins_pointer, 3)
            params = get_params(vals, 2)
            code[vals[2]] = params[0] + params[1]

        elif op == Op.mult:
            vals, ins_pointer = read_values(ins_pointer, 3)
            params = get_params(vals, 2)
            code[vals[2]] = params[0] * params[1]

        elif op == Op.inp:
            vals, ins_pointer = read_values(ins_pointer, 1)
            code[vals[0]] = on_input()

        elif op == Op.outp:
            vals, ins_pointer = read_values(ins_pointer, 1)
            params = get_params(vals, 1)
            on_output(params[0])

        elif op == Op.jit:
            vals, ins_pointer = read_values(ins_pointer, 2)
            params = get_params(vals, 2)

            if params[0] != 0:
                ins_pointer = params[1]

        elif op == Op.jif:
            vals, ins_pointer = read_values(ins_pointer, 2)
            params = get_params(vals, 2)

            if params[0] == 0:
                ins_pointer = params[1]

        elif op == Op.lt:
            vals, ins_pointer = read_values(ins_pointer, 3)
            params = get_params(vals, 2)

            code[vals[2]] = 1 if params[0] < params[1] else 0

        elif op == Op.equals:
            vals, ins_pointer = read_values(ins_pointer, 3)
            params = get_params(vals, 2)

            code[vals[2]] = 1 if params[0] == params[1] else 0

        elif op == Op.halt:
            return code[0]


args, lines = parse_args_and_get_input()

code_immutable = tuple(int(x) for x in lines[0].split(","))

if args.part_one:
    code = list(code_immutable)
    answer = run_code(code, lambda: 1, lambda x: print("PRINT {}".format(x)))
else:
    code = list(code_immutable)
    answer = run_code(code, lambda: 5, lambda x: print("PRINT {}".format(x)))

print(answer)

