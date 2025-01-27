import json
from collections.abc import Collection

all_the_numbers = {*range(1, 10)}

def solve(
    sudoku: Collection[Collection[int]],
    row: int,
    col: int) -> bool:

    if row == 9:
        return True

    next_row = row if col != 8 else row + 1
    next_col = col + 1 if col != 8 else 0

    if sudoku[row][col] != 0:
        return solve(sudoku, next_row, next_col)

    row_nums = sudoku[row]
    col_nums = [row[col] for row in sudoku]

    square_row = row // 3
    square_col = col // 3
    square_nums = [num
                for row_list in sudoku[square_row*3:square_row*3+3]
                for num in row_list[square_col*3:square_col*3+3]]

    used_nums = [*row_nums, *col_nums, *square_nums]

    for choice in all_the_numbers.difference(used_nums):
        sudoku[row][col] = choice
        if solve(sudoku, next_row, next_col):
            return True
    sudoku[row][col] = 0
    return False

def print_sudoku(sudoku):
    for row in sudoku:
        print ("----" * 9)
        print("| " + " | ".join(str(x) for x in (row)) + " |")
    print ("----" * 9)
    print("")

with open("inputs.json") as f:
    inputs = json.load(f)

unsolved, presolved = inputs["unsolved"], inputs["solved"]
sudoku = unsolved[0]
original = list(x[:] for x in sudoku)
solve(sudoku, 0, 0)
print_sudoku(original)
print_sudoku(sudoku)
print_sudoku(presolved[0])