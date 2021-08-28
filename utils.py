import sys
import math


def is_different(cell_i, cell_j):
    """
    Hàm kiểm tra 2 giá trị
    """
    result = cell_i != cell_j
    return result


def number_of_conflicts(sudoku, cell, value):
    """
    Hàm đếm số lượng xung đột ràng buộc của 1 cell khi được gán 1 giá trị nhất định
    """
    count = 0

    # Duyệt qua các cell liên quan
    for related_c in sudoku.related_cells[cell]:

        if value in sudoku.possibilities[related_c]:
            count += 1

    return count


def is_consistent(sudoku, assignment, cell, value):
    """
    Hàm kiểm tra khi gán 1 giá trị cụ thể cho 1 cell thì có gây ra xung đột ràng buộc hay không
    """
    is_consistent = True

    # Duyệt qua tất cả các cell đã được gán giá trị
    for current_cell, current_value in assignment.items():

        # Nếu cell đó liên quan đến cell hiện tại và được gán cùng giá trị
        if current_value == value and current_cell in sudoku.related_cells[cell]:
            is_consistent = False
            break
    
    return is_consistent


def assign(sudoku, cell, value, assignment):
    """
    Hàm gán giá trị cụ thể cho 1 cell và cắt bỏ miền giá trị của các cell liên quan
    """
    assignment[cell] = value
    
    return forward_check(sudoku, cell, value, assignment)


def unassign(sudoku, cell, assignment):
    """
    Hàm tháo giá trị của 1 cell và trả về các miền giá trị đã bị cắt bỏ của các cell liên quan
    """
    if cell in assignment:

        # Duyệt qua tất cả các cell và giá trị đã bị cắt bỏ khi cell này được gán
        for (coord, value) in sudoku.pruned[cell]:

            # trả lại về miền giá trị của nó
            sudoku.possibilities[coord].append(value)

        sudoku.pruned[cell] = []

        # Xóa gán
        del assignment[cell]

def forward_check(sudoku, cell, value, assignment):
    """
    Hàm cắt bỏ miền giá trị của các cell liên quan và phát hiện phép gán không hợp lệ
    """

    # Duyệt qua tất cả cell liên quan
    for related_c in sudoku.related_cells[cell]:

        # Nếu cell đó chưa được gán
        if related_c not in assignment:

            # Nếu giá trị được gán có trong miền giá trị của cell liên quan
            if value in sudoku.possibilities[related_c]:

                # Cắt bỏ giá trị đó khỏi miền giá trị của cell liên quan
                sudoku.possibilities[related_c].remove(value)

                # Thêm vào dict cắt bỏ của cell
                sudoku.pruned[cell].append((related_c, value))

                # Phát hiện phép gán không hợp lệ
                if sudoku.possibilities[related_c] == []:
                    return False

    return True           

def fetch_sudokus(input):
    """
    Xây dựng sudoku từ một chuỗi
    """

    # Tìm bậc của sudoku (bậc bằng với độ dài 1 cạnh của các ô vuông)
    n = math.sqrt(math.sqrt(len(input.split()))) # Căn bậc 4

    # Nếu bậc không hợp lệ
    if (n != int(n)):
        print("Error : the element of string must be an integer power of 4")
        sys.exit()
    
    else:
        return input, n


def print_grid(grid, n):
    '''
    Hàm in ra Sudoku trước khi giải
    '''
    output = ""
    count = 1
    
    # for each cell, print its value
    for value in list(map(int, grid.split())):

        if n < 10:
            output += "[{}]".format(value)
        elif n <100:
            output += "[{0:02d}]".format(value)

        if count >= n:
            count = 0
            output += "\n"
        
        count += 1
    
    return output