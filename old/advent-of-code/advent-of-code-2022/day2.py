from common import parse_args_and_get_input

args, lines = parse_args_and_get_input()

shape_score = {
    "A": 1,
    "B": 2,
    "C": 3,
}

test_input = """A Y
B X
C Z
""".splitlines()

#print(test_input)
#lines = test_input

rounds = [l.split() for l in lines]

if args.part_one:
    shape_score = {**shape_score, **{
        "X": 1,
        "Y": 2,
        "Z": 3,
    }}

    shape_text = {
        "A": "rock",
        "B": "paper",
        "C": "scissors",
        "X": "rock",
        "Y": "paper",
        "Z": "scissors",
    }

    total_score = 0

    for elf_shape, our_shape in rounds:
        our_score = shape_score[our_shape]

        if shape_score[elf_shape] == shape_score[our_shape]:
            our_score += 3
        elif (elf_shape == "A" and our_shape == "Y") or (elf_shape == "B" and our_shape == "Z") or (elf_shape == "C" and our_shape == "X"):
            our_score += 6

        print(shape_text[elf_shape], shape_text[our_shape], our_score)
        total_score += our_score

    print(total_score)
else:
    total_score = 0

    winning_shape_response = {
        "A": "B",
        "B": "C",
        "C": "A",
    }

    losing_shape_response = {v:k for k, v in winning_shape_response.items()}

    for elf_shape, desired_outcome in rounds:
        elf_score = shape_score[elf_shape]
        our_score = 0

        if desired_outcome == "Y":
            elf_score += 3
            our_score += elf_score
        elif desired_outcome == "X":
            our_score = shape_score[losing_shape_response[elf_shape]]
            elf_score += 6
        else:
            our_score = shape_score[winning_shape_response[elf_shape]]
            our_score += 6

        print(our_score)

        total_score += our_score

    print(total_score)

