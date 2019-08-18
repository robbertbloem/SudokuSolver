"""

"""

import numpy
import matplotlib 
import matplotlib.pyplot as plt




def display_sudoku(sudoku, do_not_print = False, verbose = 0):
    """
    Display the sudoku.     


    Arguments
    ---------
    sudoku : sudoku
        The sudoku in the standard format. 
    do_not_print : Bool (opt, False)
        Make the string, but do no print it. Mostly for unittests. 

    Returns
    -------
    string
        The printable sudoku.
    
    """

    if verbose > 1:
        print("SudokuSolver.display.display_sudoku()")
    
    s = ""
    for r in range(9):
        for c in range(9):
            s = "{:s}{:d} ".format(s, sudoku[r,c,0])
            if c in [2,5]:
                s = "{:s}| ".format(s)
        s = "{:s}\n".format(s)        
        if r in [2,5]:
            s = "{:s}------+-------+------\n".format(s)
    
    s = s.replace("0", ".")
    
    if do_not_print == False:     
        print(s)
    
    return s
                
        
def display_pencil(sudoku, do_not_print = False, pencil_only = False, verbose = 0):
    """
    Display the pencilmarks of the sudoku. Filled in numbers are shown in all nine positions.   


    Arguments
    ---------
    sudoku : sudoku
        The sudoku in the standard format. 
    do_not_print : Bool (opt, False)
        Make the string, but do no print it. Mostly for unittests. 
    pencil_only : Bool (opt, False)
        Do not show the filled sudoku square. For debugging, to check that numbers are correctly removed after filling in a number. 

    Returns
    -------
    string
        The printable sudoku.
    
    """

    if verbose > 1:
        print("SudokuSolver.display.display_pencil()")
    
    m = numpy.zeros((27,27), dtype = int)
    
    for r in range(9):
        for c in range(9):
            _r = 3 * r
            _c = 3 * c
            if sudoku[r,c,0] == 0 or pencil_only == True:
                for n in range(9):
                    c2 = _c + n % 3
                    if n in [0,1,2]:
                        r2 = _r 
                    elif n in [3,4,5]:
                        r2 = _r + 1
                    else:
                        r2 = _r + 2
                    m[r2,c2] = sudoku[r,c,n+1]

            else:
                m[_r:_r+3, _c:_c+3] = sudoku[r,c,0]
   
    s = ""    
    line = "-" * 49
    line2 = "               |                 |               "
    for r in range(27):
        for c in range(27):
            s = "{:s}{:d}".format(s, m[r,c])
            if c % 3 == 2:
                s = "{:s}  ".format(s)
            if c in [8, 17]:
                s = "{:s}|  ".format(s)
        
        s = "{:s}\n".format(s)

        
        if r in [8,17]:
            s = "{:s}{:s}\n".format(s,line)
        elif r == 26:
            pass
        elif r % 3 == 2:
            s = "{:s}{:s}\n".format(s, line2)
            
    s = s.replace("0", ".")        

    if do_not_print == False:     
        print(s)
   
    return s
                
     
    
    
    
    


    
    





    
if __name__ == "__main__": 
    pass