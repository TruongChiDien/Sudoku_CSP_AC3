import argparse
import sys
from sudoku import Sudoku
from ac3 import AC3
from backtrack import recursive_backtrack_algorithm
from utils import print_grid
from generate_input import Sudoku_Gen_Input


"""
solve
solves a sudoku based on its String grid
"""
def solve(grid, index, total, n):
    
    print("\nSudoku {}/{} : \n{}".format(index, total, print_grid(grid, n)))


    print("{}/{} : AC3 starting".format(index, total))


    # instanciate Sudoku
    sudoku = Sudoku(grid, n)

    # launch AC-3 algorithm of it
    AC3_result = AC3(sudoku)

    # Sudoku has no solution
    if not AC3_result:
        print("{}/{} : this sudoku has no solution".format(index, total))

    else:
        
        # check if AC-3 algorithm has solve the Sudoku
        if sudoku.isFinished():

            print("{}/{} : AC3 was enough to solve this sudoku !".format(index,total))
            print("{}/{} : Result: \n{}".format(index, total, sudoku))

        # continue the resolution
        else:

            print("{}/{} : AC3 finished, Backtracking starting...".format(index,total))

            assignment = {}

            # for the already known values
            for cell in sudoku.cells:

                if len(sudoku.possibilities[cell]) == 1:
                    assignment[cell] = sudoku.possibilities[cell][0]
            
            # start backtracking
            assignment = recursive_backtrack_algorithm(assignment, sudoku)

            if not assignment:
                print("{}/{} : No solution exists".format(index, total))
                return
            
            # merge the computed values for the cells at one place
            for cell in sudoku.possibilities:
                sudoku.possibilities[cell] = assignment[cell] if len(cell) > 1 else sudoku.possibilities[cell]
            
            print("{}/{} : Result: \n{}".format(index, total, sudoku))




if __name__ == "__main__":

    # samples = Sudoku_Gen_Input(16, 3, 0.2)


    # for i in range(3):
    # # fetch sudokus from user input
    #     sudoku_grid_as_string = samples.grid[i]
    #     #sudoku_grid= fetch_sudokus(sudoku_grid_as_string)
        
    #     # for each sudoku, solve it !
    #     #for index, sudoku_grid in enumerate(sudoku_queue):
    #     solve(sudoku_grid_as_string, i+1, 3, 16)


    # argument parsing using argparse module
    # doc @ https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='Solve a Sudoku with CSP')
    parser.add_argument('--edge', type=int, default=3, help='Edge of a sqare, if edge = 3 then Sudoku have size 9*9')
    parser.add_argument('--sample', type=int, default=10, help='Number of sample')
    parser.add_argument('--level', type=float, default=0.2, help='ratio of position have value (default: %(default)s)')
    args = parser.parse_args()
    
    if args.edge > 10:
        print('Edge is too large, must be between 2 and 10')

    if args.level > 0.4:
        print('Ratio is too large, must be between 0.1 and 0.4')

    samples = Sudoku_Gen_Input(args.edge**2, args.sample, args.level)


    for i in range(args.sample):
        solve(samples.grid[i], i+1, args.sample, args.edge**2)