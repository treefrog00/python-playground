from itertools import chain
from typing import List

from common import parse_args_and_get_input

args, lines = parse_args_and_get_input()

example_input = """30373
25512
65332
33549
35390"""

example_lines = example_input.splitlines()


def have_a_look(arr: List[int], reverse: bool):
    if reverse:
        start_idx = len(arr) - 1
        step = -1
        end = -1
    else:
        start_idx = 0
        step = 1
        end = len(arr)

    current_height = arr[start_idx]
    seen = {start_idx}

    print(f"reverse {reverse}")
    for idx in range(start_idx + step, end, step):
        height = arr[idx]
        if height > current_height:
            print(f"idx {idx}, {height} < {current_height}")
            seen.add(idx)
        current_height = max(height, current_height)

    return seen


def print_visible_trees(lines, seen):
    for r in range(len(lines)):
        out_chars = []
        for c in range(len(lines[0])):
            if (r, c) in seen:
                out_chars.append("*")
            else:
                out_chars.append("x")
        print(" ".join(out_chars))
        print("\n")

def run(lines):
    matrix = []
    for line in lines:
        curr_row = []
        for num in line:
            curr_row.append(int(num))
        matrix.append(curr_row)

    for row in matrix:
        print(row)

    seen = set()

    for col_idx in range(len(lines[0])):
        column = [row[col_idx] for row in matrix]
        print("column", col_idx)
        for seen_idx in chain(have_a_look(column, reverse=False), have_a_look(column, reverse=True)):
            print((seen_idx, col_idx))
            seen.add((seen_idx, col_idx))
    for row_idx, row in enumerate(matrix):
        print("row", row_idx)
        for seen_idx in chain(have_a_look(row, reverse=False), have_a_look(row, reverse=True)):
            print((row_idx, seen_idx))
            seen.add((row_idx, seen_idx))

    #print_visible_trees(lines, seen)

    if args.part_one:
        print(len(seen))
    else:
        print("hello")


#run(example_lines)
run(lines)
