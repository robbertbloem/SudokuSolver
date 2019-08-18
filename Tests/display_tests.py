"""

"""
import importlib 
# import pathlib
# import inspect
# import os
# import warnings
import unittest

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SudokuSolver.display as SSD

importlib.reload(SSD)

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_init(self):
        """
        """
        sudoku = numpy.zeros((9,9,10), dtype = int)
        
        SSD.display_sudoku(sudoku, do_not_print = True)


class Test_display(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_display_1(self):
        """
        """
        sudoku = numpy.zeros((9,9,10), dtype = int)
        s = SSD.display_sudoku(sudoku, do_not_print = True)
        test = ". . . | . . . | . . . "
        n = len(test)
        self.assertTrue(s[:n] == test)

       
    def test_display_2(self):
        """
        """
        sudoku = numpy.zeros((9,9,10), dtype = int)      
        sudoku[0,1,0] = 1
        s = SSD.display_sudoku(sudoku, do_not_print = True)
        test = ". 1 . | . . . | . . . "
        n = len(test)
        self.assertTrue(s[:n] == test)
        

    def test_display_3(self):
        """
        """
        sudoku = numpy.zeros((9,9,10), dtype = int)
        sudoku[1,0,0] = 1
        s = SSD.display_sudoku(sudoku, do_not_print = True)
        test = ". . . | . . . | . . . \n1 . . | . . . | . . . "
        n = len(test)
        self.assertTrue(s[:n] == test)


class Test_pencil(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        self.sudoku = numpy.zeros((9,9,10), dtype = int)
        for n in range(1,10):
            self.sudoku[:,:,n] = n
            
        self.sudoku[0,0,0] = 1   
        self.sudoku[0,0,1:] = 0
        self.sudoku[0,1,9] = 0  
        self.sudoku[1,0,1] = 0  


    def test_pencil_1(self):
        """
        """
        test = "111  123  123  |  123  123  123  |  123  123  123  \n111  456  456  |  456  456  456  |  456  456  456  \n111  78.  789  |  789  789  789  |  789  789  789  \n               |                 |               \n.23  123  123  |  123  123  123  |  123  123  123  "
            
        s = SSD.display_pencil(self.sudoku, do_not_print = True, pencil_only = False)
        n = len(test)
        self.assertTrue(s[:n] == test)
        
        
        
    def test_pencil_pencil_only(self):
        """
        """
        test = "...  123  123  |  123  123  123  |  123  123  123  \n...  456  456  |  456  456  456  |  456  456  456  \n...  78.  789  |  789  789  789  |  789  789  789  \n               |                 |               \n.23  123  123  |  123  123  123  |  123  123  123  "
            
        s = SSD.display_pencil(self.sudoku, do_not_print = True, pencil_only = True)
        n = len(test)
        self.assertTrue(s[:n] == test)
        



if __name__ == "__main__": 

    verbosity = 0

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
        
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_display)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
        
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_pencil)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
