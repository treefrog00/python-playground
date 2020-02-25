from common import parse_args_and_get_input, assert_equal
import itertools

from intcode import IntComputer, parse_program


def find_max_output_no_feedback(code_immutable):
    phase_setting = 0
    input_signal = 0
    input_count = 0
    max_output = 0
    amplifier_index = 0

    def input_func():
        nonlocal input_count
        input = phase_setting if input_count == 0 else input_signal
        input_count += 1
        return input

    def output_func(val):
        nonlocal input_signal
        nonlocal max_output
        input_signal = val
        if amplifier_index == 4:
            max_output = max(max_output, val)

    for perm in itertools.permutations(list(range(5))):
        input_signal = 0
        for amplifier_index in range(5):
            input_count = 0
            phase_setting = perm[amplifier_index]
            IntComputer(list(code_immutable), input_func, output_func).run()

    return max_output


def find_max_output_with_feedback(code_immutable):
    amp_count = 5
    max_output = 0

    def input_func():
        input = phase_setting if not phase_setting_was_read[amplifier_index] else input_signal
        phase_setting_was_read[amplifier_index] = True
        return input

    def output_func(val):
        nonlocal input_signal, max_output
        input_signal = val
        if amplifier_index == 4:
            max_output = max(max_output, val)
        return True

    for perm in itertools.permutations(list(range(5, 10))):
        input_signal = 0
        amplifier_index = 0
        phase_setting_was_read = [False for _ in range(amp_count)]

        computers = [IntComputer(list(code_immutable), input_func, output_func) for _ in range(amp_count)]

        its = 0

        while True:
            phase_setting = perm[amplifier_index]
            exit_code = computers[amplifier_index].run()

            if exit_code != "interrupt" and amplifier_index == 4:
                break

            amplifier_index = (amplifier_index + 1) % amp_count

            its += 1

    return max_output


args, lines = parse_args_and_get_input()


if args.part_one:
    test_code_immutable = parse_program(["3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"])
    assert_equal(43210, find_max_output_no_feedback(test_code_immutable))
    test_code_immutable2 = parse_program(["3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"])
    assert_equal(54321, find_max_output_no_feedback(test_code_immutable2))
    print(find_max_output_no_feedback(parse_program(lines)))
else:
    test_code_immutable = parse_program(["3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"])
    assert_equal(139629729, find_max_output_with_feedback(test_code_immutable))
    print(find_max_output_with_feedback(parse_program(lines)))

