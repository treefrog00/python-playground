
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


class IntComputer:
    def __init__(self, code, on_input, on_output):
        self.code = code
        self.ins_pointer = 0
        self.on_input = on_input
        self.on_output = on_output

    def read_values(self, count):
        vals = [self.code[index] for index in range(self.ins_pointer + 1, self.ins_pointer + count + 1)]
        self.ins_pointer = self.ins_pointer + count + 1

        return vals

    def run(self):

        def get_params(vals, count):
            modes = get_modes(strop, count)

            def get_param(index):
                if modes[index] == 0:
                    return self.code[vals[index]]
                if modes[index] == 1:
                    return vals[index]

            return [get_param(i)for i in range(count)]

        while True:
            op_value = self.code[self.ins_pointer]
            strop = str(op_value)

            if op_value <= 99:
                op = op_value
            else:
                op = int("".join(strop[-2:]))

            if op == Op.add:
                vals = self.read_values(3)
                params = get_params(vals, 2)
                self.code[vals[2]] = params[0] + params[1]

            elif op == Op.mult:
                vals = self.read_values(3)
                params = get_params(vals, 2)
                self.code[vals[2]] = params[0] * params[1]

            elif op == Op.inp:
                vals = self.read_values(1)
                self.code[vals[0]] = self.on_input()

            elif op == Op.outp:
                vals = self.read_values(1)
                params = get_params(vals, 1)
                interrupt = self.on_output(params[0])
                if interrupt:
                    return "interrupt"

            elif op == Op.jit:
                vals = self.read_values(2)
                params = get_params(vals, 2)

                if params[0] != 0:
                    self.ins_pointer = params[1]

            elif op == Op.jif:
                vals = self.read_values(2)
                params = get_params(vals, 2)

                if params[0] == 0:
                    self.ins_pointer = params[1]

            elif op == Op.lt:
                vals = self.read_values(3)
                params = get_params(vals, 2)

                self.code[vals[2]] = 1 if params[0] < params[1] else 0

            elif op == Op.equals:
                vals = self.read_values(3)
                params = get_params(vals, 2)

                self.code[vals[2]] = 1 if params[0] == params[1] else 0

            elif op == Op.halt:
                return self.code[0]


def parse_program(lines):
    return tuple(int(x) for x in lines[0].split(","))
