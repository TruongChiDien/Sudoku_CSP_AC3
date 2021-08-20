import itertools
import os
import math

class Sudoku:
    def  __init__(self, grid, order=9) -> None:
        game = list(map(int, grid.split()))
        self.n = order # sudoku n*n

        # generate coordinate
        self.cells = list()
        self.cells = self.generate_coords()

        # generation of all the possibilities for each one of these coords
        self.possibilities = dict()
        self.possibilities = self.generate_possibilities(game)
   
        # generation of the line / row / square constraints
        rule_constraints = self.generate_rules_constraints()

        # convertion of these constraints to binary constraints
        self.binary_constraints = list()
        self.binary_constraints = self.generate_binary_constraints(rule_constraints)

        # generating all constraint-related cells for each of them
        self.related_cells = dict()
        self.related_cells = self.generate_related_cells()

        #prune
        self.pruned = dict()
        self.pruned = {v: list() if game[i] == 0 else [(v, game[i])] for i, v in enumerate(self.cells)}


    """
    generates all the coordinates of the cells
    """
    def generate_coords(self):

        all_cells_coords = []

        # for 1, 2, 3, ..., n
        for col in range(1, self.n+1):

            #for 1,2,3 ,... ,n
            for row in range(1, self.n+1):
                
                # (1,1), (1,2), (1,2), ...,  (n,n)
                new_coords = (col, row)
                all_cells_coords.append(new_coords)

        return all_cells_coords

    """
    generates all possible value remaining for each cell
    """
    def generate_possibilities(self, grid_as_list):

        possibilities = dict()

        for index, coords in enumerate(self.cells):
            # if value is 0, then the cell can have any value in [1, n]
            if grid_as_list[index] == 0:
                possibilities[coords] = list(range(1, self.n+1))
            # else value is already defined, possibilities is this value
            else:
                possibilities[coords] = [grid_as_list[index]]

        return possibilities

    """
    generates the constraints based on the rules of the game:
    value different from any in row, column or square
    """
    def generate_rules_constraints(self):
        
        row_constraints = []
        column_constraints = []
        square_constraints = []

        rows = cols = list(range(1, self.n+1)) #[1, 2, 3, ..., n]

        # get rows constraints
        for row in rows:
            row_constraints.append([(col, row) for col in cols]) # [[(1, 2), (1, 3), ..., (n, n)]]

        # get columns constraints
        for col in cols:
            column_constraints.append([(col, row) for row in rows])

        # get square constraints
        # how to split coords (non static): 
        # https://stackoverflow.com/questions/9475241/split-string-every-nth-character

        edge_square  = int(math.sqrt(self.n)) 

        rows_square_coords = (cols[i:i+edge_square] for i in range(0, len(rows), edge_square))
        rows_square_coords = list(rows_square_coords)

        cols_square_coords = (rows[i:i+edge_square] for i in range(0, len(cols), edge_square))
        cols_square_coords = list(cols_square_coords)

        # for each square
        for row in rows_square_coords:
            for col in cols_square_coords:

                current_square_constraints = []
                
                # and for each value in this square
                for x in row:
                    for y in col:
                        current_square_constraints.append((x, y))

                square_constraints.append(current_square_constraints)

        # all constraints is the sum of these 3 rules
        return row_constraints + column_constraints + square_constraints # [[r1], [r2], ..., [square(sqrt(n))]]

    """
    generates the binary constraints based on the rule constraints
    """
    def generate_binary_constraints(self, rule_constraints):
        generated_binary_constraints = list()

        # for each set of constraints
        for constraint_set in rule_constraints:

            binary_constraints = list()

            # 2 because we want binary constraints
            # solution taken from :
            # https://stackoverflow.com/questions/464864/how-to-get-all-possible-combinations-of-a-list-s-elements
            
            #for tuple_of_constraint in itertools.combinations(constraint_set, 2):
            for tuple_of_constraint in itertools.permutations(constraint_set, 2):
                binary_constraints.append(tuple_of_constraint)

            # for each of these binary constraints
            for constraint in binary_constraints:

                # check if we already have this constraint saved
                # = check if already exists
                # solution from https://stackoverflow.com/questions/7571635/fastest-way-to-check-if-a-value-exist-in-a-list
                constraint_as_list = list(constraint)
                if(constraint_as_list not in generated_binary_constraints):
                    generated_binary_constraints.append(constraint_as_list)

        return generated_binary_constraints

    """
    generates the the constraint-related cell for each one of them
    """
    def generate_related_cells(self):
        related_cells = dict()

        #for each one of the 81 cells
        for cell in self.cells:

            related_cells[cell] = list()

            # related cells are the ones that current cell has constraints with
            for constraint in self.binary_constraints:
                if cell == constraint[0]:
                    related_cells[cell].append(constraint[1])

        return related_cells

    """
    checks if the Sudoku's solution is finished
    we loop through the possibilities for each cell
    if all of them has only one, then the Sudoku is solved
    """
    def isFinished(self):
        for coords, possibilities in self.possibilities.items():
            if len(possibilities) > 1:
                return False
        
        return True
    
    """
    returns a human-readable string
    """
    def __str__(self):

        output = ""
        count = 1
        
        # for each cell, print its value
        for cell in self.cells:

            # trick to get the right print in case of an AC3-finished sudoku
            value = self.possibilities[cell]
            if type(self.possibilities[cell]) == list:
                value = str(self.possibilities[cell][0])

            if self.n < 10:
                output += "[{}]".format(value)
            elif self.n <100:
                output += "[{0:02d}]".format(value)

            # if we reach the end of the line,
            # make a new line on display
            if count >= self.n:
                count = 0
                output += "\n"
            
            count += 1
        
        return output