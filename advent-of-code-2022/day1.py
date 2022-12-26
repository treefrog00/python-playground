from common import parse_args_and_get_input

args, lines = parse_args_and_get_input()


if args.part_one:
    cals_by_elf = []
    cals_for_elf = 0
    for line in lines:
        if not line:
            cals_by_elf.append(cals_for_elf)
            cals_for_elf = 0
        else:
            cals_for_elf += int(line)

    if args.part_one:
        print(max(cals_by_elf))
    else:
        print(sum(sorted(cals_by_elf, reverse=True)[:3]))
