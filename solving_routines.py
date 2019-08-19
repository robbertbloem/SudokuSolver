"""

"""

import warnings

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SudokuSolver.routines as SSR


def check_singles(sudoku, verbose = 0):
    """

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku

    Returns
    -------
    sudoku : sudoku
        Standard sudoku

    Notes
    -----

    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_singles()")
    
    change_counter = 0
    
    while change_counter_local > 0 or finished:
        change_counter_local = 0
        
        sudoku, cc, finished = check_last_digit(sudoku, change_counter, verbose)
        change_counter_local += cc
        change_counter += cc
        
        if finished:
            break
        
        sudoku, cc, finished = check_full_house(sudoku, change_counter, verbose)
        change_counter_local += cc
        change_counter += cc

    return sudoku, change_counter, finished


def check_last_digit(sudoku, change_counter = 0, verbose = 0):
    """
    One possible digit for a cell.

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku
    change_counter : int (opt, 0)
        Count the number of changes

    Returns
    -------
    sudoku : sudoku
        Standard sudoku
    change_counter : int
        Number of changes
    finished : bool
        True if the puzzle is finished

    Notes
    -----

    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_last_digit()")
        
    finished = False
    
    rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(sudoku, verbose)
    
    for r in rows:
        for c in cols:
            if sudoku[r,c,0] == 0:
                if numpy.count_nonzero(sudoku[r,c,1:10]) == 1:
                    n = numpy.where(sudoku[r,c,1:10] != 0)[0][0] + 1
                    sudoku, finished = SSR.fill_value(sudoku, r, c, n, verbose)
                    change_counter += 1
            if finished:
                break
        if finished:
            break
    return sudoku, change_counter, finished
    

def check_full_house(sudoku, change_counter = 0, verbose = 0):
    """
    One possible digit for a house.

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku
    change_counter : int (opt, 0)
        Count the number of changes

    Returns
    -------
    sudoku : sudoku
        Standard sudoku
    change_counter : int
        Number of changes
    finished : bool
        True if the puzzle is finished

    Notes
    -----

    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_full_house()")
    
    finished = False
    
    rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(sudoku, verbose)
    
    for n in nums:
        for r in rows:
            if numpy.count_nonzero(sudoku[r,:,n]) == 1:
                c = numpy.where(sudoku[r,:,n] != 0)[0][0]
                sudoku, finished = SSR.fill_value(sudoku, r, c, n, verbose)
                change_counter += 1
            if finished:
                break
        if finished:
            break
            
        for c in cols:
            if numpy.count_nonzero(sudoku[:,c,n]) == 1:
                r = numpy.where(sudoku[:,c,n] != 0)[0][0]
                sudoku, finished = SSR.fill_value(sudoku, r, c, n, verbose)
                change_counter += 1
            if finished:
                break
        if finished:
            break

        for br in range(3):
            for bc in range(3):
                rs, re, cs, ce = SSR.find_block_indices_br_bc(br, bc, verbose)
                if numpy.count_nonzero(sudoku[rs:re,cs:ce,n]) == 1:
                
                    r, c = numpy.where(sudoku[rs:re,cs:ce,n] != 0)
                    sudoku, finished = SSR.fill_value(sudoku, r[0], c[0], n, verbose)
                    change_counter += 1
                    
                if finished:
                    break
            if finished:
                break
        if finished:
            break
              
    return sudoku, change_counter, finished


def check_naked_subsets(sudoku, verbose = 0):
    """
    N cells containing exactly N digits in the same house. These digits can be removed from other cells in the house. 

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku
    change_counter : int (opt, 0)
        Count the number of changes

    Returns
    -------
    sudoku : sudoku
        Standard sudoku
    change_counter : int
        Number of changes
    finished : bool
        True if the puzzle is finished

    Notes
    -----

    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_naked_subsets()")
    
    sudoku = check_naked_pair(sudoku, verbose)
    sudoku, change_counter, finished = check_singles(sudoku = sudoku, verbose = verbose)
    if not finished:
        sudoku = check_naked_triple(sudoku, verbose)

        sudoku, change_counter, finished = check_singles(sudoku = sudoku, verbose = verbose)
        if not finished:
            sudoku = check_naked_quad(sudoku, verbose)
            sudoku, change_counter, finished = check_singles(sudoku = sudoku, verbose = verbose)


    return sudoku, change_counter, finished


def check_naked_pair(sudoku, verbose = 0):
    """
    

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku
    change_counter : int (opt, 0)
        Count the number of changes

    Returns
    -------
    sudoku : sudoku
        Standard sudoku
    change_counter : int
        Number of changes
    finished : bool
        True if the puzzle is finished

    Notes
    -----



    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_naked_pair()")
        
        
    rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(sudoku, verbose)

    if len(rows) > 1 and len(nums) > 1: 
        for c in cols:
            for _r1 in range(len(rows)-1):
                r1 = rows[_r1]
                if numpy.count_nonzero(sudoku[r1,c,1:10]) == 2 and sudoku[r1,c,0] == 0:
                    
                    for _r2 in range(_r1+1,len(rows)):
                        r2 = rows[_r2]
                        if numpy.count_nonzero(sudoku[r2,c,1:10]) == 2 and sudoku[r2,c,0] == 0:
                            
                            for _n1 in range(len(nums)-1):
                                for _n2 in range(_n1,len(nums)):
                                    n1 = nums[_n1]
                                    n2 = nums[_n2]

                        
                                    test = numpy.zeros(9)
                                    test[n1-1] = n1
                                    test[n2-1] = n2
                                    
                                    if numpy.all(sudoku[r1,c,1:10] == test):
                                        if numpy.all(sudoku[r2,c,1:10] == test):
                                            sudoku = SSR.erase_pencil_col(sudoku, except_r = [r1, r2], c = c, n = [n1, n2], verbose = verbose)

    if len(cols) > 1 and len(nums) > 1:
        for r in rows:
            for _c1 in range(len(cols)-1):
                c1 = cols[_c1]
                if numpy.count_nonzero(sudoku[r,c1,1:10]) == 2 and sudoku[r,c1,0] == 0:
                    
                    for _c2 in range(_c1+1,len(cols)):
                        c2 = cols[_c2]
                        if numpy.count_nonzero(sudoku[r,c2,1:10]) == 2 and sudoku[r,c2,0] == 0:
                            
                            for _n1 in range(len(nums)-1):
                                for _n2 in range(_n1,len(nums)):
                                    n1 = nums[_n1]
                                    n2 = nums[_n2]
                        
                                    test = numpy.zeros(9)
                                    test[n1-1] = n1
                                    test[n2-1] = n2
                                    
                                    if numpy.all(sudoku[r,c1,1:10] == test):
                                        if numpy.all(sudoku[r,c2,1:10] == test):
                                            s = SSR.erase_pencil_row(sudoku, r = r, except_c = [c1, c2], n = [n1, n2], verbose = verbose)

    if len(blocks) > 1 and len(nums) > 1:
        for b in blocks:
            
            rs, re, cs, ce = SSR.find_block_indices_br_bc(b[0], b[1], verbose)
            
            for x in range(8):
                r1 = rs + x % 3
                c1 = cs + int(numpy.floor(x / 3))
                if numpy.count_nonzero(sudoku[r1,c1,1:10]) == 2 and sudoku[r1,c1,0] == 0:  
                    for y in range(x+1,9):
                        r2 = rs + y % 3
                        c2 = cs + int(numpy.floor(y / 3)) 
                        if numpy.count_nonzero(sudoku[r2,c2,1:10]) == 2 and sudoku[r2,c2,0] == 0:                 
                            for _n1 in range(len(nums)-1):
                                for _n2 in range(_n1,len(nums)):
                                    n1 = nums[_n1]
                                    n2 = nums[_n2]
                                    test = numpy.zeros(9)
                                    test[n1-1] = n1
                                    test[n2-1] = n2
                                    if numpy.all(sudoku[r1,c1,1:10] == test):
                                        if numpy.all(sudoku[r2,c2,1:10] == test):
                                            except_rc = [[r1,c1],[r2,c2]]
                                            sudoku = SSR.erase_pencil_block(sudoku, br = b[0], bc = b[1], except_rc = except_rc, n = [n1, n2], verbose = verbose)

                                            
    return sudoku
    

def check_naked_triple(sudoku, verbose = 0):
    """
    

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku
    change_counter : int (opt, 0)
        Count the number of changes

    Returns
    -------
    sudoku : sudoku
        Standard sudoku
    change_counter : int
        Number of changes
    finished : bool
        True if the puzzle is finished

    Notes
    -----

    
    

    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_naked_triple()")
        
        
    rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(sudoku, verbose)

    if len(rows) > 2 and len(nums) > 2: 
        for c in cols:
            for _r1 in range(len(rows)-2):   
                r1 = rows[_r1]
                if numpy.count_nonzero(sudoku[r1,c,1:10]) < 4 and sudoku[r1,c,0] == 0:                
                    for _r2 in range(_r1+1,len(rows)-1):
                        r2 = rows[_r2]
                        if numpy.count_nonzero(sudoku[r2,c,1:10]) < 4 and sudoku[r2,c,0] == 0:    
                            for _r3 in range(_r2+1,len(rows)):  
                                r3 = rows[_r3]
                                if numpy.count_nonzero(sudoku[r3,c,1:10]) < 4 and sudoku[r3,c,0] == 0:                            
                                    for _n1 in range(len(nums)-2):
                                        for _n2 in range(_n1+1,len(nums)-1):
                                            for _n3 in range(_n2+1,len(nums)):
                                                n1 = nums[_n1]
                                                n2 = nums[_n2]
                                                n3 = nums[_n3]
                                                
                                                n_idx = numpy.arange(1,10)
                                                n_idx = numpy.delete(n_idx, [n1-1,n2-1,n3-1])
                                    
                                                test_A = numpy.all(sudoku[r1,c,n_idx] == 0)                        
                                                test_B = numpy.all(sudoku[r2,c,n_idx] == 0)
                                                test_C = numpy.all(sudoku[r3,c,n_idx] == 0)
                                                
                                                if test_A and test_B and test_C: 
                                                    sudoku = SSR.erase_pencil_col(sudoku, except_r = [r1, r2, r3], c = c, n = [n1, n2, n3], verbose = verbose)


    if len(cols) > 2 and len(nums) > 2: 
        for r in rows:
            for _c1 in range(len(cols)-2): 
                c1 = cols[_c1]  
                if numpy.count_nonzero(sudoku[r,c1,1:10]) < 4 and sudoku[r,c1,0] == 0:                
                    for _c2 in range(_c1+1,len(cols)-1):
                        c2 = cols[_c2]
                        if numpy.count_nonzero(sudoku[r,c2,1:10]) < 4 and sudoku[r,c2,0] == 0:    
                            for _c3 in range(_c2+1,len(cols)):  
                                c3 = cols[_c3]
                                if numpy.count_nonzero(sudoku[r,c3,1:10]) < 4 and sudoku[r,c3,0] == 0:                            
                                    for _n1 in range(len(nums)-2):
                                        for _n2 in range(_n1,len(nums)-1):
                                            for _n3 in range(_n2,len(nums)):
                                                n1 = nums[_n1]
                                                n2 = nums[_n2]
                                                n3 = nums[_n3]
                                                n_idx = numpy.arange(1,10)
                                                n_idx = numpy.delete(n_idx, [n1-1,n2-1,n3-1])
                                    
                                                test_A = numpy.all(sudoku[r,c1,n_idx] == 0)                        
                                                test_B = numpy.all(sudoku[r,c2,n_idx] == 0)
                                                test_C = numpy.all(sudoku[r,c3,n_idx] == 0)
                                                
                                                if test_A and test_B and test_C: 
                                                    sudoku = SSR.erase_pencil_row(sudoku, r = r, except_c = [c1, c2, c3], n = [n1, n2, n3], verbose = verbose)
                                                    
                                                    
    if len(blocks) > 2 and len(nums) > 2:
        for b in blocks:
            
            rs, re, cs, ce = SSR.find_block_indices_br_bc(b[0], b[1], verbose)
            
            for x in range(7):
                r1 = rs + x % 3
                c1 = cs + int(numpy.floor(x / 3))
#                 print("r1: {:d}, c1: {:d}".format(r1,c1))
                if numpy.count_nonzero(sudoku[r1,c1,1:10]) < 4 and sudoku[r1,c1,0] == 0:  
                    for y in range(x+1,8):
                        r2 = rs + y % 3
                        c2 = cs + int(numpy.floor(y / 3)) 
#                         print("..r2: {:d}, c2: {:d}".format(r2,c2))
                        if numpy.count_nonzero(sudoku[r2,c2,1:10]) < 4 and sudoku[r2,c2,0] == 0:    
                            for z in range(y+1,9):
                                r3 = rs + z % 3
                                c3 = cs + int(numpy.floor(z / 3)) 
#                                 print("....r3: {:d}, c3: {:d}".format(r3,c3))
                                if numpy.count_nonzero(sudoku[r3,c3,1:10]) < 4  and sudoku[r3,c3,0] == 0:          
                                    for _n1 in range(len(nums)-2):
                                        for _n2 in range(_n1,len(nums)-1):
                                            for _n3 in range(_n2,len(nums)):
                                                n1 = nums[_n1]
                                                n2 = nums[_n2]
                                                n3 = nums[_n3]                                              
                                                n_idx = numpy.arange(1,10)
                                                n_idx = numpy.delete(n_idx, [n1-1,n2-1,n3-1])
                                    
                                                test_A = numpy.all(sudoku[r1,c1,n_idx] == 0)                        
                                                test_B = numpy.all(sudoku[r2,c2,n_idx] == 0)
                                                test_C = numpy.all(sudoku[r3,c3,n_idx] == 0)
                                                if test_A and test_B and test_C:
                                                    except_rc = [[r1,c1],[r2,c2],[r3,c3]]
                                                    sudoku = SSR.erase_pencil_block(sudoku, br = b[0], bc = b[1], except_rc = except_rc, n = [n1, n2, n3], verbose = verbose)
                                
    return sudoku          

        
def __check_naked_quad_col(sudoku, r1, r2, r3, r4, c, nums, verbose = 0):
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_naked_quad_col()")
    for _n1 in range(len(nums)-3):
        for _n2 in range(_n1+1,len(nums)-2):
            for _n3 in range(_n2+1,len(nums)-1):
                for _n4 in range(_n3+1,len(nums)):
                    n1 = nums[_n1]
                    n2 = nums[_n2]
                    n3 = nums[_n3]
                    n4 = nums[_n4]
                
                    n_idx = numpy.arange(1,10)
                    n_idx = numpy.delete(n_idx, [n1-1,n2-1,n3-1,n4-1])

                    test_A = numpy.all(sudoku[r1,c,n_idx] == 0)                        
                    test_B = numpy.all(sudoku[r2,c,n_idx] == 0)
                    test_C = numpy.all(sudoku[r3,c,n_idx] == 0)
                    test_D = numpy.all(sudoku[r4,c,n_idx] == 0)
        
                    if test_A and test_B and test_C and test_D: 
                        sudoku = SSR.erase_pencil_col(sudoku, except_r = [r1, r2, r3, r4], c = c, n = [n1, n2, n3, n4], verbose = verbose)
    
    return sudoku


def __check_naked_quad_row(sudoku, r, c1, c2, c3, c4, nums, verbose = 0):
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_naked_quad_row()")
    for _n1 in range(len(nums)-3):
        for _n2 in range(_n1+1,len(nums)-2):
            for _n3 in range(_n2+1,len(nums)-1):
                for _n4 in range(_n3+1,len(nums)):
                    n1 = nums[_n1]
                    n2 = nums[_n2]
                    n3 = nums[_n3]
                    n4 = nums[_n4]
                
                    n_idx = numpy.arange(1,10)
                    n_idx = numpy.delete(n_idx, [n1-1,n2-1,n3-1,n4-1])

                    test_A = numpy.all(sudoku[r,c1,n_idx] == 0)                        
                    test_B = numpy.all(sudoku[r,c2,n_idx] == 0)
                    test_C = numpy.all(sudoku[r,c3,n_idx] == 0)
                    test_D = numpy.all(sudoku[r,c4,n_idx] == 0)
            
                    if test_A and test_B and test_C and test_D: 
                        sudoku = SSR.erase_pencil_row(sudoku, r = r, except_c = [c1, c2, c3,c4], n = [n1, n2, n3, n4], verbose = verbose)
                        
    return sudoku


def __check_naked_quad_block(sudoku, b, r1, r2, r3, r4, c1, c2, c3, c4, nums, verbose = 0):
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_naked_quad_block()")

    for _n1 in range(len(nums)-3):
        for _n2 in range(_n1+1,len(nums)-2):
            for _n3 in range(_n2+1,len(nums)-1):
                for _n4 in range(_n3+1,len(nums)):
                    n1 = nums[_n1]
                    n2 = nums[_n2]
                    n3 = nums[_n3]
                    n4 = nums[_n4]
                
                    n_idx = numpy.arange(1,10)
                    n_idx = numpy.delete(n_idx, [n1-1,n2-1,n3-1,n4-1])
    
                    test_A = numpy.all(sudoku[r1,c1,n_idx] == 0)                        
                    test_B = numpy.all(sudoku[r2,c2,n_idx] == 0)
                    test_C = numpy.all(sudoku[r3,c3,n_idx] == 0)
                    test_D = numpy.all(sudoku[r4,c4,n_idx] == 0)
                    if test_A and test_B and test_C and test_D:
                        except_rc = [[r1,c1],[r2,c2],[r3,c3],[r4,c4]]
                        sudoku = SSR.erase_pencil_block(sudoku, br = b[0], bc = b[1], except_rc = except_rc, n = [n1, n2, n3, n4], verbose = verbose)

    return sudoku

 
def check_naked_quad(sudoku, verbose = 0):
    """
    

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku
    change_counter : int (opt, 0)
        Count the number of changes

    Returns
    -------
    sudoku : sudoku
        Standard sudoku
    change_counter : int
        Number of changes
    finished : bool
        True if the puzzle is finished

    Notes
    -----

    
    

    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_naked_quad()")
        
        
    rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(sudoku, verbose)
    
    if len(rows) > 3 and len(nums) > 3: 
        for c in cols:
            for _r1 in range(len(rows)-3):   
                r1 = rows[_r1]
                if numpy.count_nonzero(sudoku[r1,c,1:10]) < 5:                
                    for _r2 in range(_r1+1,len(rows)-2):
                        r2 = rows[_r2]
                        if numpy.count_nonzero(sudoku[r2,c,1:10]) < 5:    
                            for _r3 in range(_r2+1,len(rows)-1):  
                                r3 = rows[_r3]
                                if numpy.count_nonzero(sudoku[r3,c,1:10]) < 5:  
                                    for _r4 in range(_r3+1,len(rows)):  
                                        r4 = rows[_r4]
                                        if numpy.count_nonzero(sudoku[r4,c,1:10]) < 5:   
                                        
                                            sudoku = __check_naked_quad_col(sudoku, r1, r2, r3, r4, c, nums, verbose)
                                                                 


    if len(cols) > 3 and len(nums) > 3: 
        for r in rows:
            for _c1 in range(len(cols)-3):
                c1 = cols[_c1]
                if numpy.count_nonzero(sudoku[r,c1,1:10]) < 5:                
                    for _c2 in range(_c1+1,len(cols)-2):
                        c2 = cols[_c2]
                        if numpy.count_nonzero(sudoku[r,c2,1:10]) < 5:    
                            for _c3 in range(_c2+1,len(cols)-1):  
                                c3 = cols[_c3]
                                if numpy.count_nonzero(sudoku[r,c3,1:10]) < 5: 
                                    for _c4 in range(_c3+1,len(cols)): 
                                        c4 = cols[_c4] 
                                        if numpy.count_nonzero(sudoku[r,c4,1:10]) < 5: 
                                            sudoku = __check_naked_quad_row(sudoku, r, c1, c2, c3, c4, nums, verbose)
                                
                                                    
    if len(blocks) > 3 and len(nums) > 3:
        for b in blocks:
            
            rs, re, cs, ce = SSR.find_block_indices_br_bc(b[0], b[1], verbose)
            
            for x in range(6):
                r1 = rs + x % 3
                c1 = cs + int(numpy.floor(x / 3))
                if numpy.count_nonzero(sudoku[r1,c1,1:10]) < 5:  
                    for y in range(x+1,7):
                        r2 = rs + y % 3
                        c2 = cs + int(numpy.floor(y / 3)) 
                        if numpy.count_nonzero(sudoku[r2,c2,1:10]) < 5:    
                            for z in range(y+1,8):
                                r3 = rs + z % 3
                                c3 = cs + int(numpy.floor(z / 3)) 
                                if numpy.count_nonzero(sudoku[r3,c3,1:10]) < 5:          
                                    for a in range(z+1,9):
                                        r4 = rs + a % 3
                                        c4 = cs + int(numpy.floor(a / 3)) 
                                        if numpy.count_nonzero(sudoku[r4,c4,1:10]) < 5: 
                                            sudoku = __check_naked_quad_block(sudoku, b, r1, r2, r3, r4, c1, c2, c3, c4, nums, verbose)


                                
    return sudoku      


def check_hidden_subsets(sudoku, verbose = 0):
    """
    

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku

    Returns
    -------
    sudoku : sudoku
        Standard sudoku
    change_counter : int
        Number of changes
    finished : bool
        True if the puzzle is finished

    Notes
    -----

    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_hidden_subsets()")
    
    sudoku = check_hidden_pair(sudoku, verbose)
    sudoku, change_counter, finished = check_singles(sudoku = sudoku, verbose = verbose)
    if not finished:
        sudoku = check_hidden_triple(sudoku, verbose)

        sudoku, change_counter, finished = check_singles(sudoku = sudoku, verbose = verbose)
        if not finished:
            sudoku = check_hidden_quad(sudoku, verbose)
            sudoku, change_counter, finished = check_singles(sudoku = sudoku, verbose = verbose)

    return sudoku, change_counter, finished


def check_hidden_pair(sudoku, verbose = 0):
    """
    

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku

    Returns
    -------
    sudoku : sudoku
        Standard sudoku


    Notes
    -----



    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_hidden_pair()")
        
        
    rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(sudoku, verbose)

    if len(rows) > 1 and len(nums) > 1: 
        for c in cols:
            for _n1 in range(len(nums)-1):
                n1 = nums[_n1]
                if numpy.count_nonzero(sudoku[:,c,n1]) == 2:
                    for _n2 in range(_n1+1,len(nums)):
                        n2 = nums[_n2]
                        if numpy.count_nonzero(sudoku[:,c,n2]) == 2:
                            for _r1 in range(len(rows)-1):                                
                                for _r2 in range(_r1+1,len(rows)):
                                    r1 = rows[_r1]
                                    r2 = rows[_r2]
                                    test1 = numpy.zeros(9)
                                    test2 = numpy.zeros(9)
                                    test1[r1] = n1
                                    test1[r2] = n1
                                    test2[r1] = n2
                                    test2[r2] = n2
                                    if numpy.all(sudoku[:,c,n1] == test1):
                                        if numpy.all(sudoku[:,c,n2] == test2):
                                            n = numpy.arange(1,10)
                                            n = numpy.delete(n, [n1-1,n2-1])

                                            sudoku = SSR.erase_pencil(sudoku, r = r1, c = c, n = n, verbose = verbose)
                                            sudoku = SSR.erase_pencil(sudoku, r = r2, c = c, n = n, verbose = verbose)
                                            
    if len(cols) > 1 and len(nums) > 1: 
        for r in rows:
            for _n1 in range(len(nums)-1):
                n1 = nums[_n1]
                if numpy.count_nonzero(sudoku[r,:,n1]) == 2:
                    for _n2 in range(_n1+1,len(nums)):
                        n2 = nums[_n2]
                        if numpy.count_nonzero(sudoku[r,:,n2]) == 2:
                            for _c1 in range(len(cols)-1):
                                for _c2 in range(_c1+1,len(cols)):
                                    c1 = cols[_c1]
                                    c2 = cols[_c2]
                                    test1 = numpy.zeros(9)
                                    test2 = numpy.zeros(9)
                                    test1[c1] = n1
                                    test1[c2] = n1
                                    test2[c1] = n2
                                    test2[c2] = n2
                                    if numpy.all(sudoku[r,:,n1] == test1):
                                        if numpy.all(sudoku[r,:,n2] == test2):
                                            n = numpy.arange(1,10)
                                            n = numpy.delete(n, [n1-1,n2-1])

                                            sudoku = SSR.erase_pencil(sudoku, r = r, c = c1, n = n, verbose = verbose)
                                            sudoku = SSR.erase_pencil(sudoku, r = r, c = c2, n = n, verbose = verbose)                                         
                                            



    if len(blocks) > 1 and len(nums) > 1: 
        for b in blocks:
            rs, re, cs, ce = SSR.find_block_indices_br_bc(b[0], b[1], verbose)
            for _n1 in range(len(nums)-1):
                n1 = nums[_n1]
                if numpy.count_nonzero(sudoku[rs:re,cs:ce,n1]) == 2:
                    for _n2 in range(_n1+1,len(nums)):
                        n2 = nums[_n2]
                        if numpy.count_nonzero(sudoku[rs:re,cs:ce,n2]) == 2:
                            for x in range(8):
                                _r1 = x % 3
                                r1 = rs + _r1
                                _c1 = int(numpy.floor(x / 3))    
                                c1 = cs + _c1                          
                                for y in range(x+1,9):
                                    _r2 = y % 3
                                    r2 = rs + _r2
                                    _c2 = int(numpy.floor(y / 3)) 
                                    c2 = cs + _c2
                                    
#                                     print("..r1: {:d}, c1: {:d}, r2: {:d}, c2: {:d}".format(r1, c1, r2, c2))

                                    test1 = numpy.zeros((3,3), dtype = int)
                                    test2 = numpy.zeros((3,3), dtype = int)
                                    test1[_r1,_c1] = n1
                                    test1[_r2,_c2] = n1
                                    test2[_r1,_c1] = n2
                                    test2[_r2,_c2] = n2
                                    
#                                     print(test1)
#                                     print(sudoku[rs:re,cs:ce,n1])
                                    if numpy.all(sudoku[rs:re,cs:ce,n1] == test1):
                                        if numpy.all(sudoku[rs:re,cs:ce,n2] == test2):
                                            n = numpy.arange(1,10)
                                            n = numpy.delete(n, [n1-1,n2-1])

                                            sudoku = SSR.erase_pencil(sudoku, r = r1, c = c1, n = n, verbose = verbose)
                                            sudoku = SSR.erase_pencil(sudoku, r = r2, c = c2, n = n, verbose = verbose)     


                                            
    return sudoku
    

def check_hidden_triple(sudoku, verbose = 0):
    """
    

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku

    Returns
    -------
    sudoku : sudoku
        Standard sudoku


    Notes
    -----



    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_hidden_triple()")
        
        
    rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(sudoku, verbose)

    if len(rows) > 2 and len(nums) > 2: 
        for c in cols:
            for _n1 in range(len(nums)-2):
                n1 = nums[_n1]
                if numpy.count_nonzero(sudoku[:,c,n1]) < 4:
                    for _n2 in range(_n1+1,len(nums)-1):
                        n2 = nums[_n2]
                        if numpy.count_nonzero(sudoku[:,c,n2]) < 4:
                            for _n3 in range(_n2+1,len(nums)):
                                n3 = nums[_n3]
                                if numpy.count_nonzero(sudoku[:,c,n3]) < 4:
                                    for _r1 in range(len(rows)-2):
                                        for _r2 in range(_r1+1,len(rows)-1):
                                            for _r3 in range(_r2+1,len(rows)):
                                                r1 = rows[_r1]
                                                r2 = rows[_r2]                                            
                                                r3 = rows[_r3]
                                            
                                                r_idx = numpy.arange(9)
                                                r_idx = numpy.delete(r_idx, [r1,r2,r3])
                                    
                                                test_A = numpy.all(sudoku[r_idx,c,n1] == 0)
                                                test_B = numpy.all(sudoku[r_idx,c,n2] == 0)
                                                test_C = numpy.all(sudoku[r_idx,c,n3] == 0)  
                                            
                                                if test_A and test_B and test_C:
                                                    n = numpy.arange(1,10)
                                                    n = numpy.delete(n, [n1-1,n2-1,n3-1])

                                                    sudoku = SSR.erase_pencil(sudoku, r = r1, c = c, n = n, verbose = verbose)
                                                    sudoku = SSR.erase_pencil(sudoku, r = r2, c = c, n = n, verbose = verbose)
                                                    sudoku = SSR.erase_pencil(sudoku, r = r3, c = c, n = n, verbose = verbose)
                                            
    if len(cols) > 2 and len(nums) > 2: 
        for r in rows:
            for _n1 in range(len(nums)-2):
                n1 = nums[_n1]
                if numpy.count_nonzero(sudoku[r,:,n1]) < 4:
                    for _n2 in range(_n1+1,len(nums)-1):
                        n2 = nums[_n2]
                        if numpy.count_nonzero(sudoku[r,:,n2]) < 4:
                            for _n3 in range(_n2+1,len(nums)):
                                n3 = nums[_n3]
                                if numpy.count_nonzero(sudoku[r,:,n3]) < 4:
                                    for _c1 in range(len(cols)-2):
                                        for _c2 in range(_c1+1,len(cols)-1):
                                            for _c3 in range(_c2+1,len(cols)):
                                                c1 = cols[_c1]
                                                c2 = cols[_c2]
                                                c3 = cols[_c3]
                                                c_idx = numpy.arange(9)
                                                c_idx = numpy.delete(c_idx, [c1,c2,c3])
                                    
                                                test_A = numpy.all(sudoku[r,c_idx,n1] == 0)
                                                test_B = numpy.all(sudoku[r,c_idx,n2] == 0)
                                                test_C = numpy.all(sudoku[r,c_idx,n3] == 0)  
                                                if test_A and test_B and test_C:
                                                    n = numpy.arange(1,10)
                                                    n = numpy.delete(n, [n1-1,n2-1,n3-1])

                                                    sudoku = SSR.erase_pencil(sudoku, r = r, c = c1, n = n, verbose = verbose)
                                                    sudoku = SSR.erase_pencil(sudoku, r = r, c = c2, n = n, verbose = verbose)
                                                    sudoku = SSR.erase_pencil(sudoku, r = r, c = c3, n = n, verbose = verbose)                                   
                                            
    if len(blocks) > 2 and len(nums) > 2: 
        for b in blocks:
            rs, re, cs, ce = SSR.find_block_indices_br_bc(b[0], b[1], verbose)
            for _n1 in range(len(nums)-2):
                n1 = nums[_n1]
                if numpy.count_nonzero(sudoku[rs:re,cs:ce,n1]) < 4:
                    for _n2 in range(_n1+1,len(nums)-1):
                        n2 = nums[_n2]
                        if numpy.count_nonzero(sudoku[rs:re,cs:ce,n2]) < 4:
                            for _n3 in range(_n2+1,len(nums)):
                                n3 = nums[_n3]
                                if numpy.count_nonzero(sudoku[rs:re,cs:ce,n3]) < 4:    
                                    for x in range(7):
                                        _r1 = x % 3
                                        r1 = rs + _r1
                                        _c1 = int(numpy.floor(x / 3))    
                                        c1 = cs + _c1                          
                                        for y in range(x+1,8):
                                            _r2 = y % 3
                                            r2 = rs + _r2
                                            _c2 = int(numpy.floor(y / 3)) 
                                            c2 = cs + _c2                                    
                                            for z in range(y+1,9):
                                                _r3 = z % 3
                                                r3 = rs + _r3
                                                _c3 = int(numpy.floor(z / 3)) 
                                                c3 = cs + _c3
                                                
                                                test = numpy.zeros((3,3))
                                                test[_r1,_c1] = 1
                                                test[_r2,_c2] = 1
                                                test[_r3,_c3] = 1
                                                
                                                _r, _c = numpy.where(test == 0)
                                                _r += rs
                                                _c += cs
                                                
                                                test_A = numpy.all(sudoku[_r,_c,n1] == 0)
                                                test_B = numpy.all(sudoku[_r,_c,n2] == 0)
                                                test_C = numpy.all(sudoku[_r,_c,n3] == 0)

                                                if test_A and test_B and test_C:
                                                    n = numpy.arange(1,10)
                                                    n = numpy.delete(n, [n1-1,n2-1,n3-1])

                                                    sudoku = SSR.erase_pencil(sudoku, r = r1, c = c1, n = n, verbose = verbose)
                                                    sudoku = SSR.erase_pencil(sudoku, r = r2, c = c2, n = n, verbose = verbose)
                                                    sudoku = SSR.erase_pencil(sudoku, r = r3, c = c3, n = n, verbose = verbose)    

    return sudoku


def __check_hidden_quad_col(sudoku, rows, c, n1, n2, n3, n4, verbose = 0):
    if verbose > 1:
        print("SudokuSolver.solving_routines.__check_hidden_quad_col()")

    for _r1 in range(len(rows)-3):
        for _r2 in range(_r1+1,len(rows)-2):
            for _r3 in range(_r2+1,len(rows)-1):
                for _r4 in range(_r3+1,len(rows)):
                    r1 = rows[_r1]
                    r2 = rows[_r2]
                    r3 = rows[_r3]
                    r4 = rows[_r4]
            
                    r_idx = numpy.arange(9)
                    r_idx = numpy.delete(r_idx, [r1,r2,r3,r4])
    
                    test_A = numpy.all(sudoku[r_idx,c,n1] == 0)
                    test_B = numpy.all(sudoku[r_idx,c,n2] == 0)
                    test_C = numpy.all(sudoku[r_idx,c,n3] == 0)  
                    test_D = numpy.all(sudoku[r_idx,c,n4] == 0)  
            
                    if test_A and test_B and test_C and test_D:
                        n = numpy.arange(1,10)
                        n = numpy.delete(n, [n1-1,n2-1,n3-1,n4-1])

                        sudoku = SSR.erase_pencil(sudoku, r = r1, c = c, n = n, verbose = verbose)
                        sudoku = SSR.erase_pencil(sudoku, r = r2, c = c, n = n, verbose = verbose)
                        sudoku = SSR.erase_pencil(sudoku, r = r3, c = c, n = n, verbose = verbose)
                        sudoku = SSR.erase_pencil(sudoku, r = r4, c = c, n = n, verbose = verbose)
                    
    return sudoku


def __check_hidden_quad_row(sudoku, r, cols, n1, n2, n3, n4, verbose = 0):
    if verbose > 1:
        print("SudokuSolver.solving_routines.__check_hidden_quad_row()")
        
    for _c1 in range(len(cols)-3):
        for _c2 in range(_c1+1,len(cols)-2):
            for _c3 in range(_c2+1,len(cols)-1):
                for _c4 in range(_c3+1,len(cols)):
                    c1 = cols[_c1]
                    c2 = cols[_c2]
                    c3 = cols[_c3]
                    c4 = cols[_c4]
                
                    c_idx = numpy.arange(9)
                    c_idx = numpy.delete(c_idx, [c1,c2,c3,c4])
    
                    test_A = numpy.all(sudoku[r,c_idx,n1] == 0)
                    test_B = numpy.all(sudoku[r,c_idx,n2] == 0)
                    test_C = numpy.all(sudoku[r,c_idx,n3] == 0)  
                    test_D = numpy.all(sudoku[r,c_idx,n4] == 0)  
                    
                    if test_A and test_B and test_C and test_D:
                        n = numpy.arange(1,10)
                        n = numpy.delete(n, [n1-1,n2-1,n3-1,n4-1])

                        sudoku = SSR.erase_pencil(sudoku, r = r, c = c1, n = n, verbose = verbose)
                        sudoku = SSR.erase_pencil(sudoku, r = r, c = c2, n = n, verbose = verbose)
                        sudoku = SSR.erase_pencil(sudoku, r = r, c = c3, n = n, verbose = verbose)
                        sudoku = SSR.erase_pencil(sudoku, r = r, c = c4, n = n, verbose = verbose)  
                    
    return sudoku


def __check_hidden_quad_block(sudoku, rs, re, cs, ce, n1, n2, n3, n4, verbose = 0):
    if verbose > 1:
        print("SudokuSolver.solving_routines.__check_hidden_quad_block()")

    for x in range(6):
        _r1 = x % 3
        r1 = rs + _r1
        _c1 = int(numpy.floor(x / 3))    
        c1 = cs + _c1                          
        for y in range(x+1,7):
            _r2 = y % 3
            r2 = rs + _r2
            _c2 = int(numpy.floor(y / 3)) 
            c2 = cs + _c2                                    
            for z in range(y+1,8):
                _r3 = z % 3
                r3 = rs + _r3
                _c3 = int(numpy.floor(z / 3)) 
                c3 = cs + _c3
                
                for a in range(z+1,9):
                    _r4 = a % 3
                    r4 = rs + _r4
                    _c4 = int(numpy.floor(a / 3)) 
                    c4 = cs + _c4           
                
                    test = numpy.zeros((3,3))
                    test[_r1,_c1] = 1
                    test[_r2,_c2] = 1
                    test[_r3,_c3] = 1
                    test[_r4,_c4] = 1
                
                    _r, _c = numpy.where(test == 0)
                    _r += rs
                    _c += cs
                
                    test_A = numpy.all(sudoku[_r,_c,n1] == 0)
                    test_B = numpy.all(sudoku[_r,_c,n2] == 0)
                    test_C = numpy.all(sudoku[_r,_c,n3] == 0)
                    test_D = numpy.all(sudoku[_r,_c,n4] == 0)

                    if test_A and test_B and test_C and test_D:
                        n = numpy.arange(1,10)
                        n = numpy.delete(n, [n1-1,n2-1,n3-1,n4-1])

                        sudoku = SSR.erase_pencil(sudoku, r = r1, c = c1, n = n, verbose = verbose)
                        sudoku = SSR.erase_pencil(sudoku, r = r2, c = c2, n = n, verbose = verbose)
                        sudoku = SSR.erase_pencil(sudoku, r = r3, c = c3, n = n, verbose = verbose)  
                        sudoku = SSR.erase_pencil(sudoku, r = r4, c = c4, n = n, verbose = verbose)  

    return sudoku


def check_hidden_quad(sudoku, verbose = 0):
    """
    

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku

    Returns
    -------
    sudoku : sudoku
        Standard sudoku


    Notes
    -----



    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_hidden_quad()")
        
        
    rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(sudoku, verbose)

    if len(rows) > 3 and len(nums) > 3: 
        for c in cols:
            for _n1 in range(len(nums)-3):
                n1 = nums[_n1]
                if numpy.count_nonzero(sudoku[:,c,n1]) < 5:
                    for _n2 in range(_n1+1,len(nums)-2):
                        n2 = nums[_n2]
                        if numpy.count_nonzero(sudoku[:,c,n2]) < 5:
                            for _n3 in range(_n2+1,len(nums)-1):
                                n3 = nums[_n3]
                                if numpy.count_nonzero(sudoku[:,c,n3]) < 5:
                                    for _n4 in range(_n3+1,len(nums)):
                                        n4 = nums[_n4]
                                        if numpy.count_nonzero(sudoku[:,c,n4]) < 5:
                                            sudoku = __check_hidden_quad_col(sudoku, rows, c, n1, n2, n3, n4, verbose)
                                    
                                            
    if len(cols) > 3 and len(nums) > 3: 
        for r in rows:
            for _n1 in range(len(nums)-3):
                n1 = nums[_n1]
                if numpy.count_nonzero(sudoku[r,:,n1]) < 5:
                    for _n2 in range(_n1+1,len(nums)-2):
                        n2 = nums[_n2]
                        if numpy.count_nonzero(sudoku[r,:,n2]) < 5:
                            for _n3 in range(_n2+1,len(nums)-1):
                                n3 = nums[_n3]
                                if numpy.count_nonzero(sudoku[r,:,n3]) < 5:
                                    for _n4 in range(_n3+1,len(nums)):
                                        n4 = nums[_n4]
                                        if numpy.count_nonzero(sudoku[r,:,n4]) < 5:
                                            sudoku = __check_hidden_quad_row(sudoku, r, cols, n1, n2, n3, n4, verbose)
                                        
                                                                             
    if len(blocks) > 3 and len(nums) > 3: 
        for b in blocks:
            rs, re, cs, ce = SSR.find_block_indices_br_bc(b[0], b[1], verbose)
            for _n1 in range(len(nums)-3):
                n1 = nums[_n1]
                if numpy.count_nonzero(sudoku[rs:re,cs:ce,n1]) < 5:
                    for _n2 in range(_n1+1,len(nums)-2):
                        n2 = nums[_n2]
                        if numpy.count_nonzero(sudoku[rs:re,cs:ce,n2]) < 5:
                            for _n3 in range(_n2+1,len(nums)-1):
                                n3 = nums[_n3]
                                if numpy.count_nonzero(sudoku[rs:re,cs:ce,n3]) < 5: 
                                    for _n4 in range(_n3+1,len(nums)):
                                        n4 = nums[_n4]
                                        if numpy.count_nonzero(sudoku[rs:re,cs:ce,n4]) < 5:  
                                            sudoku = __check_hidden_quad_block(sudoku, rs, re, cs, ce, n1, n2, n3, n4, verbose)  
  

    return sudoku


def check_wing_double(sudoku, verbose = 0):
    """
    

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku

    Returns
    -------
    sudoku : sudoku
        Standard sudoku


    Notes
    -----



    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_wing_double()")    

    rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(sudoku, verbose)


    return sudoku



def check_wing_triple(sudoku, verbose = 0):
    """
    

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku

    Returns
    -------
    sudoku : sudoku
        Standard sudoku


    Notes
    -----



    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_wing_triple()")    

    rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(sudoku, verbose)













    return sudoku






def __check_locked_set_helper(xs,xe,y,ys,ye, verbose = 0):

    if verbose > 1:
        print("SudokuSolver.solving_routines.__check_locked_set_helper()")

    if xs == 0:
        xs1 = 3
        xe1 = 6
        xs2 = 6
        xe2 = 9
    elif xs == 3:
        xs1 = 0
        xe1 = 3
        xs2 = 6
        xe2 = 9
    else:
        xs1 = 0
        xe1 = 3
        xs2 = 3
        xe2 = 6  
       
    if y % 3 == 0:
        y1 = ys + 1
        y2 = ys + 2
    elif y % 3 == 1:
        y1 = ys
        y2 = ys + 2
    else:
        y1 = ys
        y2 = ys + 1

    return xs1, xe1, xs2, xe2, y1, y2



def check_locked_sets(sudoku, verbose = 0):
    """
    A number can only occur in the intersection of two houses. The pencil marks can be removed from the other house.
    
    X : cell which may contain a candidate for digit X
    - : cell which does not contain a candidate for digit X
    * : cell from which we may eliminate the candidates for digit X
    
    Type 1 (Pointing): 
    .-------.-------.-------.
    | * * * | * * * | X X X |
    |       |       | - - - |
    |       |       | - - - |
    '-------'-------'-------'

    Type 2 (Claiming or Box-Line Reduction):
    .-------.-------.-------.
    | - - - | - - - | X X X |
    |       |       | * * * |
    |       |       | * * * |
    '-------'-------'-------'


    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku

    Returns
    -------
    sudoku : sudoku
        Standard sudoku


    Notes
    -----



    """ 
    if verbose > 1:
        print("SudokuSolver.solving_routines.check_locked_set_double()")
        
        
    rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(sudoku, verbose)
    
    
    for br in range(3):
        for bc in range(3):
            rs, re, cs, ce = SSR.find_block_indices_br_bc(br, bc, verbose)
            for _n in range(len(nums)):
                n = nums[_n]
                for r in range(rs,re):
                    if r in rows:
                        cs1, ce1, cs2, ce2, r1, r2 = __check_locked_set_helper(cs, ce, r, rs, re, verbose)               
                        if numpy.all(sudoku[r,cs1:ce1,n] == 0):
                            if numpy.all(sudoku[r,cs2:ce2,n] == 0):
                                if numpy.any(sudoku[r,cs:ce,n] == n):
                                    sudoku[r1,cs:ce,n] = 0
                                    sudoku[r2,cs:ce,n] = 0
                            
                        if numpy.all(sudoku[r1,cs:ce,n] == 0):
                            if numpy.all(sudoku[r2,cs:ce,n] == 0):
                                if numpy.any(sudoku[r,cs:ce,n] == n):
                                    sudoku[r,cs1:ce1,n] = 0
                                    sudoku[r,cs2:ce2,n] = 0                                    
                                                        
                for c in range(cs,ce):
                    if c in cols:
                        rs1, re1, rs2, re2, c1, c2 = __check_locked_set_helper(rs, re, c, cs, ce, verbose)                        
                        if numpy.all(sudoku[rs1:re1,c,n] == 0):
                            if numpy.all(sudoku[rs2:re2,c,n] == 0):
                                if numpy.any(sudoku[rs:re,c,n] == n):
                                    sudoku[rs:re,c1,n] = 0
                                    sudoku[rs:re,c2,n] = 0
                            
                        if numpy.all(sudoku[rs:re,c1,n] == 0):
                            if numpy.all(sudoku[rs:re,c2,n] == 0):
                                if numpy.any(sudoku[rs:re,c,n] == n):
                                    sudoku[rs1:re1,c,n] = 0
                                    sudoku[rs2:re2,c,n] = 0                 
    
    
    
    return sudoku    
    
    
    
    
    
    
        











if __name__ == "__main__": 
    pass