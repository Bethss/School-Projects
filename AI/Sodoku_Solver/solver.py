"""
Notes
- minimum remaining value and degree heuristics for unassigned variable selection
- that is, whichever var has the least # of domain vals and 
- has the most constraints on other unassigned vars
"""
from itertools import count
from threading import get_ident
import copy

var_grid = [[],[],[],[],[],[],[],[],[]]
    
def read_to_sgrid(filename,grid):
    """
    writes numbers from input file to a grid    
    """
    file = open(filename,"r")
    rowNo = 0
    for line in file:
        if rowNo<=8:
            try:
                row = list(map(int,line[:-1].split(' ')))
            except:
                row = list(map(int,line[:-2].split(' ')))
            if line[-1]!='\n':
                row = list(map(int,line.split(' ')))
            grid[rowNo]= row
        rowNo+=1
    file.close()

def print_sgrid(grid):
    """
    Prints grid in list form, row by row    
    """
    for row in grid:
        print(row)

def count_zeros(grid):
    count = 0
    for row in range(9):
        for col in range(9):
            if grid[row][col]==0:
                count+=1
    return count

def grid3x3_test(grid, num, row, col):
    """
    based on given row and column, find 3x3 grid num belongs to
    check that num is the only of its kind(int val) in the 3xt grid
    """
    grid_row_start = (row//3)*3 # First get which 3x3 row
    grid_col_start = (col//3)*3 # Then get which 3x3 col
    count = 0
    for i in range(3):
        for j in range(3):
            if grid[grid_row_start+i][grid_col_start+j]==num:
                count+=1
                if count>1:
                    return False
    return True

def constraint_test(grid, num, row, col):
    """
    Checks that num is the only # in its row, column,
    and finally i its 3x3 grid
    """
    row_count = 0
    for ints in grid[row]:
        if ints == num:
            row_count +=1
            if row_count>1:
                return False # row check failed, i.e. double found
    col_count = 0
    for i in range(9):
        if grid[i][col] == num:
            col_count+=1
            if col_count>1:
                return False # col check failed, i.e. double found
    if grid3x3_test(grid, num, row, col):
        return True
    return False

def degree_heuristic(grid,row,col):
    """
    Counts # of unassigned in rows+columns and 3x3 grid and returns the #
    """
    count = 0
    for ints in grid[row]: 
        if ints == 0:
            count +=1      # count 0s in row
    for i in range(9):
        if grid[i][col] == 0:
            count+=1       # count 0s in col
    grid_row_start = (row//3)*3      # First get which 3x3 row
    grid_col_start = (col//3)*3      # Then get which 3x3 col
    for i in range(3):
        for j in range(3):
            if grid[grid_row_start+i][grid_col_start+j]==0:
                if grid_row_start+i!= row and grid_col_start+j!= col: # already done row and col
                    count+=1    # count 0s in 3x3 grid
    return count - 2 # subtract itself (row and col, as grid skips row and col)

def count_legal_moves(grid, row, col):
    domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    Counts # of legal moves avail// removes neighboring vars from domain list above
    """
    for ints in grid[row]: 
        if ints != 0:
            if ints in domain:
                domain.remove(ints)
    for i in range(9):
        if grid[i][col] != 0:
            if grid[i][col] in domain:
                domain.remove(grid[i][col])
    grid_row_start = (row//3)*3      # First get which 3x3 row
    grid_col_start = (col//3)*3      # Then get which 3x3 col
    for i in range(3):
        for j in range(3):
            if grid[grid_row_start+i][grid_col_start+j]!=0:
                if grid[grid_row_start+i][grid_col_start+j] in domain:
                    domain.remove(grid[grid_row_start+i][grid_col_start+j])
    return len(domain), domain

def sel_unassigned_var(grid,visited):
    """
    Find grid pos based on # of legal moves and, # of constraints (neighbors)
    i.e total # of unassigned in rows+columns and 3x3 grid as these 
    variables share constraints of unique row,column and 3x3 grid numbers
    """
    min_rem_val = 8
    same_count_lst= []
    for row in range(9):
        for col in range(9): # loop through every var
            if grid[row][col]==0: # if 0, we found an unassigned var
                if [row,col] not in visited: # proceed if var has not been visited
                    rem_moves,domain = count_legal_moves(grid, row, col)
                    if rem_moves<min_rem_val:
                        constraint_count = degree_heuristic(grid,row,col)
                        same_count_lst.clear()
                        same_count_lst.append([[row,col],domain,constraint_count])
                    elif rem_moves== min_rem_val:
                        constraint_count = degree_heuristic(grid,row,col)
                        same_count_lst.append([[row,col],domain,constraint_count])                 
    """
    using degree heuristic as tie breaker, returns variable's pos and domain (ones needed)
    """
    max_constraints_count = 0
    max_constraints_var_info = []
    for item in same_count_lst:
        if item[2] > max_constraints_count:
            max_constraints_count= item[2]
            max_constraints_var_info = item
    return max_constraints_var_info

def solved_test(grid):
    """
    Loops through every element/var on 9x9 grid
         and checks that constraints are satisfied
    """
    check = True
    for i in range(9):
        for j in range(9):
            if check == True:
                check = constraint_test(grid,grid[i][j],i,j)
                check = grid[i][j]!=0
    return check

def backtracking(grid, visited):
    """
    Recursive alg to solve sodoku problem
    * It might not match backtracking at first glance as the functions created
        above already handle some operations
    """
    if count_zeros(grid)==0:
        return True, grid, visited
    var_info = sel_unassigned_var(grid, visited)
    if len(var_info)==0:
        return False, grid, visited
    for legal_move in var_info[1]:
        grid[var_info[0][0]][var_info[0][1]]= legal_move
        if constraint_test(grid, legal_move, var_info[0][0], var_info[0][1]):
            result, grid, unimportant = backtracking(grid, visited)
            if result:
                return result, grid, visited
        else:
            grid[var_info[0][0]][var_info[0][1]]= 0
    return False, grid, var_info[0]

def solve(grid):
    """
    The above backtracking relies on the first variable it selects.
    'Solve' goes to select a new first variable if the first doesnt
        work and etc..
    """
    total_unassigned= count_zeros(grid)
    visited = []
    while len(visited)!=total_unassigned:
        result_grid = copy.deepcopy(grid)
        res, result_grid, pos = backtracking(result_grid,visited)
        if res:
            return res, result_grid, visited
        visited.append(pos)
    return False, result_grid, visited

def main():
    """
    File inclusion: Please delete lines of files not in folder or include them :)
    """
    in_1 = "Input1.txt"
    in_2 = "Input2.txt"
    in_3 = "Input3.txt"
    in_4 = "Sample_input.txt"
    op_1 = "Input1_Sol.txt"
    op_2 = "Input2_Sol.txt"
    op_3 = "Input3_Sol.txt"
    op_4 = "Sample_Output.txt"

    """ *** GRID SETUP *** """
    read_to_sgrid(in_1,var_grid) # please change first argument to the file being solved
    print_sgrid(var_grid)
    print("Solving below..")

    """ *** SOLVER *** """
    res,res_grid, visited = solve(var_grid)
    #visited = []
    #res,res_grid, visited = backtracking(var_grid,visited)
    """ *** WRITING TO FILE *** """

    """ *** OPTIONAL PRINTING TO OUTPUT *** """
    print_sgrid(res_grid)
    print(res)
    #print(visited)

main()