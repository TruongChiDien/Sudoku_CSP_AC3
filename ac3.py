from utils import is_different

"""
Lan truyền ràng buộc với AC-3
Mã giả tại @ https://en.wikipedia.org/wiki/AC-3_algorithm
"""
def AC3(csp, queue=None):

    if queue == None:
        queue = list(csp.binary_constraints)

    while queue:

        (xi, xj) = queue.pop(0)

        if remove_inconsistent_values(csp, xi, xj): 

            # Nếu có cell nào không còn giá trị thì bài toán không có lời giải
            if len(csp.possibilities[xi]) == 0:
                return False
            
            for Xk in csp.related_cells[xi]:
                if Xk != xi:
                    queue.append((Xk, xi))
                    
    return True

"""
Loại bỏ các giá trị không nhất quán tại 1 cell liền kề của cell hiện tại
"""
def remove_inconsistent_values(csp, cell_i, cell_j):

    removed = False

    # for each possible value remaining for the cell_i cell
    for value in csp.possibilities[cell_i]:

        # if cell_i=value is in conflict with cell_j=poss for each possibility
        if not any([is_different(value, poss) for poss in csp.possibilities[cell_j]]):
            
            # then remove cell_i=value
            csp.possibilities[cell_i].remove(value)
            removed = True

    # returns true if a value has been removed
    return removed
