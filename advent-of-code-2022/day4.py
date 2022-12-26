from common import parse_args_and_get_input

args, lines = parse_args_and_get_input()

pairs = [line.split(",") for line in lines]
paired_ranges = [list(int(num) for elf in pair for num in elf.split("-")) for pair in pairs]


overlap_count = 0
for vals in paired_ranges:
    fully_overlap = (vals[0] <= vals[2] and vals[1] >= vals[3]) or (vals[2] <= vals[0] and vals[3] >= vals[1])
    partly_overlap = (vals[0] <= vals[2] <= vals[1]) or (vals[0] <= vals[3] <= vals[1])

    if args.part_one and fully_overlap:
        overlap_count += 1
    elif args.part_two and (fully_overlap or partly_overlap):
        overlap_count += 1

print(overlap_count)