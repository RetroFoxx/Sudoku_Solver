#!/usr/bin/env python
# coding:utf-8

import timeit
import math
import sys

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"


def get_columns():
    column_list = []
    for c in range(9):
        column = []
        for r in range(9):
            column.append(ROW[r] + COL[c])
        column_list.append(column)

    return column_list


def get_rows():
    row_list = []
    for r in range(9):
        row = []
        for c in range(9):
            row.append(ROW[r] + COL[c])
        row_list.append(row)

    return row_list


def get_grids():
    grid_list = []
    a_to_c = list(ROW[0:3])
    d_to_f = list(ROW[3:6])
    g_to_i = list(ROW[6:9])
    one_to_three = list(COL[0:3])
    four_to_six = list(COL[3:6])
    six_to_nine = list(COL[6:9])

    grid_list.append([row + col for row in a_to_c for col in one_to_three])
    grid_list.append([row + col for row in a_to_c for col in four_to_six])
    grid_list.append([row + col for row in a_to_c for col in six_to_nine])

    grid_list.append([row + col for row in d_to_f for col in one_to_three])
    grid_list.append([row + col for row in d_to_f for col in four_to_six])
    grid_list.append([row + col for row in d_to_f for col in six_to_nine])

    grid_list.append([row + col for row in g_to_i for col in one_to_three])
    grid_list.append([row + col for row in g_to_i for col in four_to_six])
    grid_list.append([row + col for row in g_to_i for col in six_to_nine])

    return grid_list


rows = get_rows()
columns = get_columns()
grids = get_grids()


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ""
        for j in COL:
            row += str(board[i + j]) + " "
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return "".join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    solved_assignment = backtrack({}, board)
    solved_board = board
    for var in solved_assignment:
        solved_board[var] = solved_assignment[var]

    return solved_board


def backtrack(assignment, board):
    if is_complete(board):
        return assignment

    domain_unassigned = initialize_domain(board)
    var = select_unassigned_variable(board)
    order_domain_values = domain_unassigned[var]

    for value in order_domain_values:
        if is_consistent(assignment, domain_unassigned, var, value):
            assignment[var] = value
            board[var] = value
            result = backtrack(assignment, board)
            if result is not None:
                return result
            board[var] = 0
            del assignment[var]

    return None


def is_consistent(assignment, domain_unassigned, var, value):
    same_row = get_row(var)
    same_col = get_row(var)
    same_grid = get_grid(var)

    if len(assignment) != 0:
        for variable in assignment:
            if variable in same_row and assignment[variable] == value:
                return False
            if variable in same_col and assignment[variable] == value:
                return False
            if variable in same_grid and assignment[variable] == value:
                return False
    # forward checking
    for variable in domain_unassigned:
        if variable != var:
            if variable in same_row:
                if len(domain_unassigned[variable] - {value}) == 0:
                    return False
            if variable in same_col:
                if len(domain_unassigned[variable] - {value}) == 0:
                    return False
            if variable in same_col:
                if len(domain_unassigned[variable] - {value}) == 0:
                    return False
    return True


def is_complete(board):
    empty_tiles = tiles_to_solve(board)
    if len(empty_tiles) == 0:
        return True
    return False


# select using minimum remaining value
def select_unassigned_variable(board):
    domain_unassigned = initialize_domain(board)
    min_remaining_val = 9
    min_list = []

    for variable in domain_unassigned.keys():
        if len(domain_unassigned[variable]) < min_remaining_val:
            min_remaining_val = len(domain_unassigned[variable])
            min_list = []
            min_list.append(variable)

        elif len(domain_unassigned[variable]) == min_remaining_val:
            min_list.append(variable)
        else:
            continue

    return min_list[0]


def initialize_domain(board):
    domain_unassigned = {}
    empty_tiles = tiles_to_solve(board)

    for variable in empty_tiles:
        domain_unassigned[variable] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    for variable in domain_unassigned.keys():
        var_row = get_row(variable)
        var_col = get_column(variable)
        var_grid = get_grid(variable)

        invalid_vals = []
        for value in var_row:
            if board[value] != 0:
                invalid_vals.append(board[value])
        for value in var_col:
            if board[value] != 0:
                invalid_vals.append(board[value])
        for value in var_grid:
            if board[value] != 0:
                invalid_vals.append(board[value])
        invalid_set = set(invalid_vals)

        old_domain = domain_unassigned[variable]
        new_domain = old_domain - invalid_set

        domain_unassigned[variable] = new_domain

    return domain_unassigned


def get_column(variable):
    column_list = []
    for column in columns:
        if variable in column:
            column_list = column
    return column_list


def get_row(variable):
    row_list = []
    for row in rows:
        if variable in row:
            row_list = row
    return row_list


def get_grid(variable):
    grid_list = []
    for grid in grids:
        if variable in grid:
            grid_list = grid
    return grid_list


def tiles_to_solve(board):
    empty_tiles = []

    for key in board.keys():
        if board[key] == 0:
            empty_tiles.append(key)

    return empty_tiles


def get_min(min_list):
    min_val = min_list[0]

    for val in min_list:
        if min_val > val:
            min_val = val

    return min_val


def get_max(max_list):
    max_val = max_list[0]

    for val in max_list:
        if max_val < val:
            max_val = val

    return max_val


def get_sum(sum_list):
    sum_val = 0

    for val in sum_list:
        sum_val = sum_val + val

    return sum_val


def get_std(std_list, mean_val):
    std_calc = 0

    for val in std_list:
        diff = val - mean_val
        std_calc = std_calc + math.pow(diff, 2)

    sq_diff = std_calc / len(std_list)
    st_dev = math.sqrt(sq_diff)

    return st_dev


def read_from_file():
    src_filename = "sudokus_start.txt"
    try:
        srcfile = open(src_filename, "r")
        sudoku_list = srcfile.read()
    except:
        print("Error reading the sudoku file %s" % src_filename)
        exit()

    # Setup output file
    out_filename = "output.txt"
    outfile = open(out_filename, "w")

    results = []

    # Solve each board using backtracking
    for line in sudoku_list.split("\n"):

        if len(line) < 9:
            continue

        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {
            ROW[r] + COL[c]: int(line[9 * r + c]) for r in range(9) for c in range(9)
        }

        # Print starting board. TODO: Comment this out when timing runs.
        print_board(board)

        # Solve with backtracking
        start = timeit.default_timer()
        solved_board = backtracking(board)
        stop = timeit.default_timer()

        results.append(stop - start)

        # Print solved board. TODO: Comment this out when timing runs.
        print_board(solved_board)

        # Write board to file
        outfile.write(board_to_string(solved_board))
        outfile.write("\n")

    min_time = get_min(results)
    max_time = get_max(results)
    sum_time = get_sum(results)
    mean_time = sum_time / len(results)
    std_time = get_std(results, mean_time)

    readme_filename = "README.txt"
    readme_file = open(readme_filename, "w")
    readme_file.write(
        "Puzzles solved from sudokus_start.txt: " + str(len(results)) + "\n"
    )
    readme_file.write("Mean of runtimes: " + str(mean_time) + "\n")
    readme_file.write("Standard deviation of runtimes: " + str(std_time) + "\n")
    readme_file.write("Min runtime: " + str(min_time) + "\n")
    readme_file.write("Max runtime: " + str(max_time) + "\n")

    print("Finishing all boards in file.")


if __name__ == "__main__":
    arg_list = sys.argv
    if len(arg_list) == 1:
        read_from_file()
    elif len(arg_list) == 2:
        out_filename = "output.txt"
        outfile = open(out_filename, "w")

        sudoku_string = arg_list[1]
        if len(sudoku_string) != 81:
            print(
                "Please execute python3 sudoku.py <input_string> with a valid sudoku puzzle input_string"
            )
        if len(sudoku_string) == 81:
            board = {
                ROW[r] + COL[c]: int(sudoku_string[9 * r + c])
                for r in range(9)
                for c in range(9)
            }

            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)

            # Solve with backtracking
            start = timeit.default_timer()
            solved_board = backtracking(board)
            stop = timeit.default_timer()

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)
            print("Runtime: " + str(stop - start))

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write("\n")
    else:
        print("too many arguments!")
