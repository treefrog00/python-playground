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


def part_one(matrix):
    def have_a_look(arr: List[int], reverse: bool):
        def real_index(idx):
            return len(arr) - idx - 1 if reverse else idx

        if reverse:
            arr = list(reversed(arr))

        current_height = arr[0]
        seen = {real_index(0)}

        for idx in range(len(arr)):
            height = arr[idx]
            if height > current_height:
                print(f"idx {idx}, {height} < {current_height}")
                seen.add(real_index(idx))
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

    print(f"visible tree count: {len(seen)}")


def part_two(matrix):
    def have_a_look(arr: List[int], house_height):
        count = 0
        for tree_height in arr:
            count += 1
            if tree_height >= house_height:
                return count
        return count

    max_scenic_score = 0

    for house_row, row in enumerate(matrix):
        for house_col in range(len(matrix[0])):
            leftwards = reversed(row[:house_col])
            rightwards = row[house_col + 1:]
            upwards = reversed([row[house_col] for row in matrix[:house_row]])
            downwards = [row[house_col] for row in matrix[house_row + 1:]]

            house_height = row[house_col]

            print(f"house col {house_col} house_row {house_row} l {leftwards} r {rightwards} up {upwards} down {downwards}")

            scenic_score = 1
            for arr in [leftwards, rightwards, upwards, downwards]:
                scenic_score *= have_a_look(arr, house_height)

            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score

    print(max_scenic_score)

def build_matrix(lines):
    matrix = []
    for line in lines:
        curr_row = []
        for num in line:
            curr_row.append(int(num))
        matrix.append(curr_row)

    for row in matrix:
        print(row)

    return matrix

matrix = build_matrix(lines)
part_one(matrix)
