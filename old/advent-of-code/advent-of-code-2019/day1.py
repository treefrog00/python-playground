from common import parse_args_and_get_input, assert_equal


def fuel_for_mass(mass):
    return int(mass / 3) - 2


def fuel_for_mass_with_additional_fuel(m, acc):
    f = fuel_for_mass(m)
    return fuel_for_mass_with_additional_fuel(f, f + acc) if f > 0 else acc


args, lines = parse_args_and_get_input()

modules = [int(x) for x in lines]

if args.part_one:
    assert_equal(33583, fuel_for_mass(100756))
    answer = sum(fuel_for_mass(m) for m in modules)
else:
    assert_equal(50346, fuel_for_mass_with_additional_fuel(100756, 0))
    answer = sum(fuel_for_mass_with_additional_fuel(m, 0) for m in modules)


print(answer)

