from typing import Callable


class Op:
    add = 1
    mult = 2
    inp = 3
    outp = 4
    jit = 5
    jif = 6
    lt = 7
    equals = 8
    adjust_relative_base = 9
    halt = 99


def get_modes(strop, value_count):
    return list(reversed([int(x) for x in strop[:-2].zfill(value_count)]))


class IntComputer:
    def __init__(self, code_immutable: tuple, on_input: Callable[[], int], on_output: Callable[[int], None]):
        self.code = list(code_immutable) + [0] * 1000
        self.ins_pointer = 0
        self.on_input = on_input
        self.on_output = on_output
        self.relative_base = 0

    def _read_values(self, count):
        vals = [self.code[index] for index in range(self.ins_pointer + 1, self.ins_pointer + count + 1)]
        self.ins_pointer = self.ins_pointer + count + 1

        return vals

    def _get_params(self, strop, literal_modes):
        vals = self._read_values(len(literal_modes))
        modes = get_modes(strop, len(vals))

        def get_param(index):
            if modes[index] == 0:
                return self.code[vals[index]]
            if modes[index] == 1:
                return vals[index]
            if modes[index] == 2:
                return self.code[vals[index] + self.relative_base]

        def get_param_literal(index):
            if modes[index] == 0:
                return vals[index]
            if modes[index] == 1:
                raise Exception("mode 1 in literal mode")
            if modes[index] == 2:
                return vals[index] + self.relative_base

        return [
            get_param_literal(i) if literal_modes[i] else get_param(i) for i in range(len(vals))
        ]

    def run(self):
        while True:
            op_value = self.code[self.ins_pointer]
            strop = str(op_value)

            if op_value <= 99:
                op = op_value
            else:
                op = int("".join(strop[-2:]))

            if op == Op.add:
                params = self._get_params(strop, [False, False, True])
                self.code[params[2]] = params[0] + params[1]

            elif op == Op.mult:
                params = self._get_params(strop, [False, False, True])
                self.code[params[2]] = params[0] * params[1]

            elif op == Op.inp:
                params = self._get_params(strop, [True])
                self.code[params[0]] = self.on_input()

            elif op == Op.outp:
                params = self._get_params(strop, [False])
                interrupt = self.on_output(params[0])
                if interrupt:
                    return "interrupt"

            elif op == Op.jit:
                params = self._get_params(strop, [False, False])

                if params[0] != 0:
                    self.ins_pointer = params[1]

            elif op == Op.jif:
                params = self._get_params(strop, [False, False])

                if params[0] == 0:
                    self.ins_pointer = params[1]

            elif op == Op.lt:
                params = self._get_params(strop, [False, False, True])

                self.code[params[2]] = 1 if params[0] < params[1] else 0

            elif op == Op.equals:
                params = self._get_params(strop, [False, False, True])

                self.code[params[2]] = 1 if params[0] == params[1] else 0

            elif op == Op.adjust_relative_base:
                params = self._get_params(strop, [False])
                self.relative_base += params[0]

            elif op == Op.halt:
                return self.code[0]


def parse_program(line):
    return tuple(int(x) for x in line.split(","))
