from sudoku import Sudoku
from generate_input import Gen_Input_Random
import argparse
from ac3 import AC3


def number_of_avai(sudoku, cell):
    cnt = 0
    for related_c in sudoku.related_cells[cell]:
        if len(sudoku.possibilities[related_c]) == 1:
            cnt += 1

    return cnt


def order_unassigned_variable(sudoku):

    unassigned = []

    for cell in sudoku.cells:

        if len(sudoku.possibilities[cell]) > 1:

            unassigned.append(cell)
    
    f = lambda cell: number_of_avai(sudoku, cell)

    return sorted(unassigned, key = f, reverse=True)



# def generate_possibilities(sudoku):

#     possibilities = dict()

#     for cell in order_unassigned_variable(sudoku):
#         possibilities[cell] = []

#         for value in range(1, sudoku.n + 1):
#             consistence = True

#             for related_c in sudoku.related_cells[cell]:

#                 if len(sudoku.possibilities[related_c]) == 1 and sudoku.possibilities[related_c][0] == value:
#                     consistence = False
#                     break
            
#             if consistence == True:
#                 possibilities[cell].append(value)

#     for cell in sudoku.cells:
#         if len(sudoku.possibilities[cell]) == 1:
#             possibilities[cell] = sudoku.possibilities[cell]

#     return possibilities

def generate_possibilities(sudoku):
    possibilities = dict()

    for cell in sudoku.cells:
        if len(sudoku.possibilities[cell]) == 1:
            possibilities[cell] = sudoku.possibilities[cell]
            continue

        possibilities[cell] = []
        for value in range(1, sudoku.n+1):
            consistence = True
            for related_c in sudoku.related_cells[cell]:
                if len(sudoku.possibilities[related_c]) == 1 and sudoku.possibilities[related_c][0] == value:
                    consistence = False
                    break
            
            if consistence == True:
                possibilities[cell].append(value)

    return possibilities

        



if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Solve a Sudoku with CSP')
    # parser.add_argument('--edge', type=int, default=3,
    #                     help='Edge of a square, if edge = 3 then Sudoku have size 9*9')
    # parser.add_argument('--sample', type=int, default=10,
    #                     help='Number of sample')
    # parser.add_argument('--level', type=float, default=0.2,
    #                     help='ratio of position have value (default: %(default)s)')
    # args = parser.parse_args()

    # sample = Gen_Input_Random(args.edge**2, 1, args.level)

    # Input = Sudoku(sample[0], args.edge**2)

    # Output = Sudoku(sample[0], args.edge**2)

    sample = Gen_Input_Random(9, 1, 0.2)

    Input = Sudoku(sample[0], 9)

    Output = Sudoku(sample[0], 9)

    Output.possibilities = generate_possibilities(Output)

    AC3(Input)

    for cell in Input.cells:
        if len(Input.possibilities[cell]) != len(Output.possibilities[cell]):
            print('Wrong!')
            exit(0)

        for value in Input.possibilities[cell]:
            if value not in Output.possibilities[cell]:
                print('Wrong!')
                exit(0)

    print('AC-3 is right!')
    