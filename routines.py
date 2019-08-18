"""

"""

import warnings

import numpy
import matplotlib 
import matplotlib.pyplot as plt







def construct_sudoku(verbose = 0):
    """

    Arguments
    ---------
    sudoku: type
        Explanation

    Returns
    -------
    sudoku 

    Notes
    -----

    """   

    if verbose > 1:
        print("SudokuSolver.routines.construct_sudoku()")
        
    s = numpy.zeros((9,9,12), dtype = int)
    
    for n in range(1,10):
        s[:,:,n] = n
    
    for br in range(3): 
        for bc in range(3): 
            rs = br * 3
            re = rs + 3
            cs = bc * 3
            ce = cs + 3
            s[rs:re,cs:ce,10] = br
            s[rs:re,cs:ce,11] = bc
    
    return s
        

def fill_value(sudoku, r, c, n, verbose = 0):
    """

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku
    r : int
        Row
    c : int
        Column
    n : int
        Value

    Returns
    -------
    sudoku : sudoku
        The sudoku
    finished : bool
        True if finished. 

    Notes
    -----

    """ 

    if verbose > 1:
        print("SudokuSolver.routines.fill_value(r: {:d}, c: {:d}, n: {:d})".format(r,c,n))
        
    if sudoku[r,c,0] != 0:
        warnings.warn("r: {:d}, c: {:d}, n: {:d}: fill value in square that is already filled with {:d}".format(r,c,n, sudoku[r,c,0]))

    sudoku[r,c,0] = n
    
    sudoku[r,c,1:10] = 0
    sudoku[r,:,n] = 0
    sudoku[:,c,n] = 0

    br = sudoku[r,c,10]
    bc = sudoku[r,c,11]    

    _r, _c = numpy.where(numpy.logical_and(sudoku[:,:,10] == br, sudoku[:,:,11] == bc))  
    
    for i in range(9):
        sudoku[_r[i], _c[i], n] = 0    
        
    finished = check_finished(sudoku, verbose)
    
    return sudoku, finished




def erase_pencil(sudoku, r, c, n, verbose = 0):
    """

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku
    r : int
        Row
    c : int
        Column
    n : int or array
        Value or values to be erased

    Returns
    -------
    sudoku

    Notes
    -----

    """     

    if verbose > 1:
        print("SudokuSolver.routines.erase_pencil()")
    
    if type(n) == int:
        n = numpy.asarray([n], dtype = int)
    
    for _n in n:
        sudoku[r,c,_n] = 0
    
    return sudoku



def erase_pencil_rcn(sudoku, rcn, verbose = 0):
    """

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku
    rcn : list
        List with lists of coordinates at which pencilmarks are removed.

    Returns
    -------
    sudoku

    Notes
    -----

    """     

    if verbose > 1:
        print("SudokuSolver.routines.erase_pencil_rcn()")
    
    rcn = numpy.asarray(rcn, dtype = int)
    
    for _rcn in rcn:
        sudoku[_rcn[0],_rcn[1],_rcn[2]] = 0
    
    return sudoku



def erase_pencil_row(sudoku, r, except_c, n, verbose = 0):
    """

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku
    r : int
        Row from which pencilmarks have to be erased
    except_c : int
        Do not erase pencil marks in these columns
    n : int or array
        Value or values to be erased

    Returns
    -------
    sudoku

    Notes
    -----

    """     

    if verbose > 1:
        print("SudokuSolver.routines.erase_pencil_row()")

    if type(n) == int:
        n = numpy.asarray([n], dtype = int)
         
    for _n in n:
        temp = numpy.copy(sudoku[r,:,_n])
        sudoku[r,:,_n] = 0
        sudoku[r,except_c,_n] = temp[except_c]
    
    return sudoku



def erase_pencil_col(sudoku, except_r, c, n, verbose = 0):
    """

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku
    except_r : int
        Do not erase pencil marks in these rows
    c : int
        Column from which pencilmarks have to be erased
    n : int or array
        Value or values to be erased

    Returns
    -------
    sudoku

    Notes
    -----

    """     

    if verbose > 1:
        print("SudokuSolver.routines.erase_pencil_col()")
    
    if type(n) == int:
        n = numpy.asarray([n], dtype = int)
         
    for _n in n:    
        temp = numpy.copy(sudoku[:,c,_n])
        sudoku[:,c,_n] = 0
        sudoku[except_r,c,_n] = temp[except_r]
    
    return sudoku



def erase_pencil_block(sudoku, br, bc, except_rc, n, verbose = 0):
    """

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku
    br : int
        Block row index from which pencilmarks have to be erased.
    bc : int
        Block column index from which pencilmarks have to be erased.
    except_rc : list
        Do not erase pencil marks at these indices. Indices are 0-9. Format is [[r1,c1], [r2,c2]]
    n : int or array
        Value or values to be erased

    Returns
    -------
    sudoku

    Notes
    -----

    """     

    if verbose > 1:
        print("SudokuSolver.routines.erase_pencil_block()")
        
        
    rs, re, cs, ce = find_block_indices_br_bc(br, bc, verbose)
    
    if type(n) == int:
        n = numpy.asarray([n], dtype = int)  
    
    # coordinates within the block
    except_rc = numpy.asarray(except_rc, dtype = int) 
    r = except_rc[:,0] - rs
    c = except_rc[:,1] - cs

    for _n in n:
        temp = numpy.copy(sudoku[rs:re,cs:ce,_n])
        sudoku[rs:re,cs:ce,_n] = 0
        
        for i in range(len(r)):
            sudoku[except_rc[i,0],except_rc[i,1],_n] = temp[r[i],c[i]]
    
    return sudoku




def check_finished(sudoku, verbose = 0):
    """

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku

    Returns
    -------
    object

    Notes
    -----

    """ 
    
    if verbose > 1:
        print("SudokuSolver.routines.check_finished()")
        
    if numpy.count_nonzero(sudoku[:,:,0]) == 81:
        return True
    else:
        return False




def check_sanity(sudoku, verbose = 0):
    """

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku

    Returns
    -------
    n_warnings : int
        Number of warnings

    Notes
    -----
    The following things are checked:
    
    - if the value exists, there should be no pencilmarks
    - if the value does not exist, there should be at least one pencilmark

    """ 
    
    if verbose > 1:
        print("SudokuSolver.routines.check_sanity()") 
    
    n_warnings = 0
    for r in range(9):
        for c in range(9):
            
            if sudoku[r,c,0] == 0:
                if numpy.count_nonzero(sudoku[r,c,1:10]) == 0:
                    warnings.warn("r: {:d}, c: {:d}: square: no value and no pencilmarks".format(r,c))
                    n_warnings += 1
                    
            else: 
                if numpy.count_nonzero(sudoku[r,c,1:10]) != 0:
                    warnings.warn("r: {:d}, c: {:d}: square: value exists, not all pencilmarks are zero".format(r,c))
                    n_warnings += 1
                    
        if n_warnings > 9:
            warnings.warn("Stopped checking... too many warnings.")
            break
    
    if n_warnings > 9:
        return n_warnings
    
    for n in range(1,10):               
        for r in range(9):   
            if n not in sudoku[r,:,0]:
                if numpy.count_nonzero(sudoku[r,:,n]) == 0:
                    warnings.warn("r: {:d}, n: {:d}: row: no value and no pencilmarks".format(r,n))
                    n_warnings += 1
            else:
                if numpy.count_nonzero(sudoku[r,:,n]) != 0:
                    warnings.warn("r: {:d}, n: {:d}: row: value exists, not all pencilmarks are zero".format(r,n))
                    n_warnings += 1

        if n_warnings > 9:
            warnings.warn("Stopped checking... too many warnings.")
            break

      
        for c in range(9):   
            if n not in sudoku[:,c,0]:
                if numpy.count_nonzero(sudoku[:,c,n]) == 0:
                    warnings.warn("c: {:d}, n: {:d}: column: no value and no pencilmarks".format(c,n))
                    n_warnings += 1
            else:
                if numpy.count_nonzero(sudoku[:,c,n]) != 0:
                    warnings.warn("c: {:d}, n: {:d}: column: value exists, not all pencilmarks are zero".format(c,n)) 
                    n_warnings += 1

        if n_warnings > 9:
            warnings.warn("Stopped checking... too many warnings.")
            break
                    
        for br in range(3):
            for bc in range(3):
                rs = br * 3
                re = rs + 3
                cs = bc * 3
                ce = cs + 3
               
                if n not in sudoku[rs:re,cs:ce,0]:
                    if numpy.count_nonzero(sudoku[rs:re,cs:ce,n]) == 0:
                        warnings.warn("br: {:d}, bc: {:d}, n: {:d}: block: no value and no pencilmarks".format(br,bc,n))
                        n_warnings += 1
                else:
                    if numpy.count_nonzero(sudoku[rs:re,cs:ce,n]) != 0:
                        warnings.warn("br: {:d}, bc: {:d}, n: {:d}: block: value exists, not all pencilmarks are zero".format(br,bc,n)) 
                        n_warnings += 1
                        
    return n_warnings    
    
    
    
    
    
    
    
    
    
def find_block_indices_r_c(r, c, verbose = 0):
    """

    Arguments
    ---------
    r : int
        Row
    c : int
        Column

    Returns
    -------
    br : int
        Index of block row
    rs : int
        Start index for row
    re : int
        End index for row
    bc : int
        Index of block column
    cs : int
        Start index for column
    ce : int
        End index for column

    Notes
    -----


    """ 
    
    if verbose > 1:
        print("SudokuSolver.routines.find_block_indices_r_c()") 
        
    if r < 3:
        br = 0
    elif r >= 6:
        br = 2
    else:
        br = 1
    
    if c < 3:
        bc = 0
    elif c >= 6:
        bc = 2
    else:
        bc = 1
    
    rs = br * 3
    re = rs + 3
    cs = bc * 3
    ce = cs + 3
    
    return br, rs, re, bc, cs, ce
    
    
def find_block_indices_br_bc(br, bc, verbose = 0):
    """

    Arguments
    ---------
    br : int
        Block row
    bc : int
        Block column

    Returns
    -------
    rs : int
        Start index for row
    re : int
        End index for row
    cs : int
        Start index for column
    ce : int
        End index for column

    Notes
    -----


    """ 
    
    if verbose > 1:
        print("SudokuSolver.routines.find_block_indices_br_bc()") 

    
    rs = br * 3
    re = rs + 3
    cs = bc * 3
    ce = cs + 3
    
    return rs, re, cs, ce
    
    
    
def unfinished_rcnbrbc(sudoku, verbose = 0):
    """

    Arguments
    ---------
    sudoku : sudoku
        Standard sudoku

    Returns
    -------


    Notes
    -----


    """ 
    
    if verbose > 1:
        print("SudokuSolver.routines.unfinished_rcnbrbc()") 
    
    rows = []
    cols = []
    nums = []
    blocks = []
    
    for r in range(9):
        if numpy.count_nonzero(sudoku[r,:,1:10]) > 0:
            rows.append(r)
 
    for c in range(9):
        if numpy.count_nonzero(sudoku[:,c,1:10]) > 0:
            cols.append(c)

    for n in range(1,10):
        if numpy.count_nonzero(sudoku[:,:,n]) > 0:
            nums.append(n)

    for br in range(3):
        for bc in range(3):
            rs, re, cs, ce = find_block_indices_br_bc(br, bc, verbose)
            if numpy.count_nonzero(sudoku[rs:re,cs:ce,1:10]) > 0:    
                blocks.append([br,bc])
    
    return rows, cols, nums, blocks


    
    
    
    


    
if __name__ == "__main__": 
    pass