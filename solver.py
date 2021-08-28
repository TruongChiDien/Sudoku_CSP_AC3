import argparse
from sudoku import Sudoku
from ac3 import AC3
from backtrack import recursive_backtrack_algorithm
from utils import print_grid
from generate_input import Sudoku_Gen_Input
import time
import copy




def solve(grid, index, total, n):
    """
    Hàm giải Sudoku bằng AC-3 và backtracking
    """

    print("\nSudoku {}/{} : \n{}".format(index, total, print_grid(grid, n)))

    print("{}/{} : AC3 starting".format(index, total))

    # Tạo một Sudoku
    sudoku = Sudoku(grid, n)
    sudoku2 = copy.deepcopy(sudoku)

    # Chạy AC-3    
    print('\n-----Before AC-3')
    num_arc = len(sudoku.binary_constraints)
    tolal_val = 0
    largest_domain = 0
    for cell in sudoku.possibilities:
        tolal_val += len(sudoku.possibilities[cell])
        largest_domain = max(len(sudoku.possibilities[cell]), largest_domain)
    print(f'Number of arcs: {num_arc}\nTotal values: {tolal_val}\nSize of largest domain: {largest_domain}')

    start = time.time()
    AC3_result = AC3(sudoku)
    time_ac3 = time.time() - start
    print('\n-----AC-3 take {} s'.format(time_ac3))
    
    print('\n-----After AC-3')
    num_arc = len(sudoku.binary_constraints)
    tolal_val = 0
    largest_domain = 0
    for cell in sudoku.possibilities:
        tolal_val += len(sudoku.possibilities[cell])
        largest_domain = max(len(sudoku.possibilities[cell]), largest_domain)
    print(f'Number of arcs: {num_arc}\nnTotal values: {tolal_val}\nSize of largest domain: {largest_domain}')

    # Sudoku không có lời giải
    if not AC3_result:
        print("{}/{} : this sudoku has no solution".format(index, total))
        print("Total time: {}s".format(time_ac3))

    else:

        # Kiểm tra xem Sudoku đã được giải chưa
        if sudoku.isFinished():

            print("{}/{} : AC3 was enough to solve this sudoku!".format(index, total))
            print("{}/{} : Result: \n{}".format(index, total, sudoku))


        # Nếu chưa thì tiếp tục dùng backtracking
        else:

            print('Backtracking starting...')
            assignment = {}

            # Gán các giá trị đã biết
            for cell in sudoku.cells:

                if len(sudoku.possibilities[cell]) == 1:
                    assignment[cell] = sudoku.possibilities[cell][0]

            # Backtracking
            start = time.time()
            assignment = recursive_backtrack_algorithm(assignment, sudoku)
            time_back = time.time() - start
            print('Backtracking take {} s'.format(time_back))

            if not assignment:
                print("{}/{} : No solution exists".format(index, total))
                print('Total time: {}s'.format(time_ac3 + time_back))
                
            else:
                # Gán giá trị cell lại cho miền giá trị của nó
                for cell in sudoku.possibilities:
                    sudoku.possibilities[cell] = assignment[cell]

                print("{}/{} : Result: \n{}".format(index, total, sudoku))

    choice = input('Do you wanna compare to Backtracking-only?(n = No)')
    if choice == 'n':
        return

    print('------Backtracking-only starting...')
    
    assignment = {}

    # Gán các giá trị đã biết
    for cell in sudoku2.cells:

        if len(sudoku2.possibilities[cell]) == 1:
            assignment[cell] = sudoku2.possibilities[cell][0]

    # Backtracking
    start = time.time()
    assignment = recursive_backtrack_algorithm(assignment, sudoku2)
    time_back = time.time() - start
    print('Backtracking take {} s'.format(time_back))

    if not assignment:
        print("{}/{} : No solution exists".format(index, total))
        print('Total time: {}s'.format(time_back))
        return
        
    else:
        # Gán giá trị cell lại cho miền giá trị của nó
        for cell in sudoku2.possibilities:
            sudoku2.possibilities[cell] = assignment[cell]

        print("{}/{} : Result: \n{}".format(index, total, sudoku2))

    # compare = True
    # for cell in sudoku.cells:
    #     if sudoku.possibilities[cell] != sudoku2.possibilities[cell]:
    #         compare = False
    #         break
    # if compare:   
    #     print('Both have the same result!')
    # else:
    #     print('Both have the different solution!')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Solve a Sudoku with CSP')
    parser.add_argument('--edge', type=int, default=3,
                        help='Edge of a square, if edge = 3 then Sudoku have size 9*9')
    parser.add_argument('--sample', type=int, default=1,
                        help='Number of sample')
    parser.add_argument('--level', type=float, default=0.2,
                        help='ratio of position have value (default: %(default)s)')
    args = parser.parse_args()

    if args.edge > 6:
        print('Edge is too large, must be between 2 and 6')
        exit(0)

    if args.level > 0.3:
        print('Ratio is too large, must be between 0.1 and 0.3')
        exit(0)

    samples = Sudoku_Gen_Input(args.edge**2, args.sample, args.level)

    for i in range(args.sample):
        solve(samples.grid[i], i+1, args.sample, args.edge**2)
