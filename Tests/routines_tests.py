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

import SudokuSolver.routines as SSR
import SudokuSolver.display as SSD

importlib.reload(SSR)
importlib.reload(SSD)

class Test_construct_sudoku(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_init(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        self.assertTrue(numpy.shape(s) == (9,9,12))
        self.assertTrue(s[0,0,10] == 0)
        self.assertTrue(s[1,1,10] == 0)
        self.assertTrue(s[1,1,11] == 0)
        self.assertTrue(s[3,0,10] == 1)
        self.assertTrue(s[3,0,11] == 0)
        


class Test_fill_value(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_fill_1(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)

        r = 0
        c = 0 
        n = 1
        s, f = SSR.fill_value(s, r, c, n)
        
        self.assertTrue(s[0,0,0] == 1) # number is filled in
        self.assertTrue(numpy.all(s[0,0,1:10] == 0)) # pencils for num are 0
        self.assertTrue(numpy.all(s[:,0,1] == 0)) # pencils in row are 0
        self.assertTrue(numpy.all(s[0,:,1] == 0)) # pencils in col are 0
        self.assertTrue(numpy.all(s[0:3,0:3,1] == 0)) # pencils in block are 0
#         SSD.display_pencil(s)
        
        
    def test_fill_2(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)

        r = 3
        c = 1 
        n = 2
        s, f = SSR.fill_value(s, r, c, n)
        
        self.assertTrue(s[3,1,0] == 2) # number is filled in
        self.assertTrue(numpy.all(s[3,1,1:10] == 0)) # pencils for num are 0
        self.assertTrue(numpy.all(s[:,1,2] == 0)) # pencils in row are 0
        self.assertTrue(numpy.all(s[3,:,2] == 0)) # pencils in col are 0
        self.assertTrue(numpy.all(s[3:6,0:3,2] == 0)) # pencils in block are 0
#         SSD.display_pencil(s)


class Test_check_finished(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_1(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        
        res = SSR.check_finished(s)
        self.assertFalse(res)
        
        s[:,:,0] = 1
        res = SSR.check_finished(s)
        self.assertTrue(res)


class Test_check_sanity(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_1(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        s[0,0,1:10] = 0
        s[1,1,0] = 2
        SSR.check_sanity(s)
        
    def test_2(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        s[0,:,2] = 0
        SSR.check_sanity(s)


    def test_3(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        s[0:3,0:3,2] = 0
        SSR.check_sanity(s)


class Test_find_block_indices(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_find_block_indices_r_c(self):
        # r,c, br,rs,re, bc,cs,ce
        tests = numpy.array([
            [0,0, 0,0,3, 0,0,3],
            [1,2, 0,0,3, 0,0,3],
            [5,5, 1,3,6, 1,3,6],
        ])
        
        for t in tests:
        
            br, rs, re, bc, cs, ce = SSR.find_block_indices_r_c(r = t[0], c = t[1], verbose = self.verbose)
#             print(t[0], t[1], br, rs, re, bc, cs, ce)
            self.assertTrue(br == t[2])
            self.assertTrue(rs == t[3])
            self.assertTrue(re == t[4])
            self.assertTrue(bc == t[5])
            self.assertTrue(cs == t[6])
            self.assertTrue(ce == t[7])

        
    def test_find_block_indices_br_bc(self):
        # br,bc, rs,re, cs,ce
        tests = numpy.array([
            [0,0, 0,3, 0,3],
            [1,0, 3,6, 0,3],
            [2,0, 6,9, 0,3],
            [0,2, 0,3, 6,9],
            [1,2, 3,6, 6,9],
        ])
        
        
        for t in tests:
        
            rs, re, cs, ce = SSR.find_block_indices_br_bc(br = t[0], bc = t[1], verbose = self.verbose)
            self.assertTrue(rs == t[2])
            self.assertTrue(re == t[3])
            self.assertTrue(cs == t[4])
            self.assertTrue(ce == t[5])



class Test_erase_pencil(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_erase_pencil(self):
        s = SSR.construct_sudoku(verbose = self.verbose)
        SSR.erase_pencil(sudoku = s, r = 0, c = 0, n = 1, verbose = self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(s[0,0,1] == 0)


    def test_erase_pencil_n_array(self):
        s = SSR.construct_sudoku(verbose = self.verbose)
        SSR.erase_pencil(sudoku = s, r = 0, c = 0, n = [1,2], verbose = self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(s[0,0,1] == 0)
        self.assertTrue(s[0,0,2] == 0)


    def test_erase_pencil_rcn(self):
        s = SSR.construct_sudoku(verbose = self.verbose)
        rcn = [[2,2,4],[5,6,7]]
        SSR.erase_pencil_rcn(sudoku = s, rcn = rcn, verbose = self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(s[2,2,4] == 0)
        self.assertTrue(s[5,6,7] == 0)


    def test_erase_pencil_row(self):
        s = SSR.construct_sudoku(verbose = self.verbose) 
        SSR.erase_pencil_row(sudoku = s, r = 0, except_c = [1,2], n = 1, verbose = self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(s[0,0,1] == 0)
        self.assertTrue(numpy.all(s[0,1:3,1] == 1))
        self.assertTrue(numpy.all(s[0,3:,1] == 0))


    def test_erase_pencil_row_n_array(self):
        s = SSR.construct_sudoku(verbose = self.verbose)
        SSR.erase_pencil_row(sudoku = s, r = 0, except_c = [1,2], n = [1,2], verbose = self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(s[0,0,1] == 0)
        self.assertTrue(numpy.all(s[0,1:3,1] == 1))
        self.assertTrue(numpy.all(s[0,3:,1] == 0))
        self.assertTrue(s[0,0,2] == 0)
        self.assertTrue(numpy.all(s[0,1:3,2] == 2))
        self.assertTrue(numpy.all(s[0,3:,2] == 0))


    def test_erase_pencil_col(self):
        s = SSR.construct_sudoku(verbose = self.verbose)    
        SSR.erase_pencil_col(sudoku = s, except_r = [3,4,5], c = 3, n = 9, verbose = self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[0:3,3,9] == 0))
        self.assertTrue(numpy.all(s[3:6,3,9] == 9))
        self.assertTrue(numpy.all(s[6:,3,9] == 0))


    def test_erase_pencil_col_n_array(self):
        s = SSR.construct_sudoku(verbose = self.verbose)    
        SSR.erase_pencil_col(sudoku = s, except_r = [3,4,5], c = 3, n = [8,9], verbose = self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[0:3,3,8] == 0))
        self.assertTrue(numpy.all(s[3:6,3,8] == 8))
        self.assertTrue(numpy.all(s[6:,3,8] == 0))
        self.assertTrue(numpy.all(s[0:3,3,9] == 0))
        self.assertTrue(numpy.all(s[3:6,3,9] == 9))
        self.assertTrue(numpy.all(s[6:,3,9] == 0))


    def test_erase_pencil_block(self):
        s = SSR.construct_sudoku(verbose = self.verbose)    
        SSR.erase_pencil_block(sudoku = s, br = 1, bc = 1, except_rc = [[3,3],[4,4],[5,5]], n = 9, verbose = self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(s[3,3,9] == 9)
        self.assertTrue(s[4,4,9] == 9)
        self.assertTrue(s[5,5,9] == 9)
        self.assertTrue(s[4:5,3,9] == 0)
        self.assertTrue(numpy.all(s[0:3,:,9] == 9))
        self.assertTrue(numpy.all(s[:,0:3,9] == 9))



    def test_erase_pencil_block_n_array(self):
        s = SSR.construct_sudoku(verbose = self.verbose)    
        SSR.erase_pencil_block(sudoku = s, br = 1, bc = 1, except_rc = [[3,3],[4,4],[5,5]], n = [1,9], verbose = self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(s[3,3,1] == 1)
        self.assertTrue(s[4,4,1] == 1)
        self.assertTrue(s[5,5,1] == 1)
        self.assertTrue(s[4:5,3,1] == 0)
        self.assertTrue(numpy.all(s[0:3,:,1] == 1))
        self.assertTrue(numpy.all(s[:,0:3,1] == 1))
        self.assertTrue(s[3,3,9] == 9)
        self.assertTrue(s[4,4,9] == 9)
        self.assertTrue(s[5,5,9] == 9)
        self.assertTrue(s[4:5,3,9] == 0)
        self.assertTrue(numpy.all(s[0:3,:,9] == 9))
        self.assertTrue(numpy.all(s[:,0:3,9] == 9))


class Test_unfinished_rcnbrbc(unittest.TestCase):


    def setUp(self):
        self.verbose = 1
        
    def test_1(self):
        s = SSR.construct_sudoku(verbose = self.verbose) 
        rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(s, self.verbose)
        self.assertTrue(len(rows) == 9)
        self.assertTrue(len(cols) == 9)
        self.assertTrue(len(nums) == 9)
        self.assertTrue(len(blocks) == 9)
        
        
    def test_row(self):
        s = SSR.construct_sudoku(verbose = self.verbose) 
        for i in range(9):
            s,f = SSR.fill_value(s, i, 0, i+1, verbose = self.verbose)
#         SSD.display_pencil(s)
        rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(s, self.verbose)
#         print(rows, cols, nums, blocks)
        self.assertTrue(len(rows) == 9)
        self.assertTrue(len(cols) == 8)
        self.assertTrue(len(nums) == 9)
        self.assertTrue(len(blocks) == 9)

    def test_col(self):
        s = SSR.construct_sudoku(verbose = self.verbose) 
        for i in range(9):
            s,f = SSR.fill_value(s, 3, i, i+1, verbose = self.verbose)
#         SSD.display_pencil(s)
        rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(s, self.verbose)
#         print(rows, cols, nums, blocks)
        self.assertTrue(len(rows) == 8)
        self.assertTrue(len(cols) == 9)
        self.assertTrue(len(nums) == 9)
        self.assertTrue(len(blocks) == 9)       

    def test_block(self):
        s = SSR.construct_sudoku(verbose = self.verbose) 
        
        s,f = SSR.fill_value(s, 0, 0, 1, verbose = self.verbose)
        s,f = SSR.fill_value(s, 1, 0, 2, verbose = self.verbose)
        s,f = SSR.fill_value(s, 2, 0, 3, verbose = self.verbose)
        
        s,f = SSR.fill_value(s, 0, 1, 4, verbose = self.verbose)
        s,f = SSR.fill_value(s, 1, 1, 5, verbose = self.verbose)
        s,f = SSR.fill_value(s, 2, 1, 6, verbose = self.verbose)

        s,f = SSR.fill_value(s, 0, 2, 7, verbose = self.verbose)
        s,f = SSR.fill_value(s, 1, 2, 8, verbose = self.verbose)
        s,f = SSR.fill_value(s, 2, 2, 9, verbose = self.verbose)
#         SSD.display_pencil(s)
        rows, cols, nums, blocks = SSR.unfinished_rcnbrbc(s, self.verbose)
#         print(rows, cols, nums, blocks)
        self.assertTrue(len(rows) == 9)
        self.assertTrue(len(cols) == 9)
        self.assertTrue(len(nums) == 9)
        self.assertTrue(len(blocks) == 8)     



if __name__ == "__main__": 

    verbosity = 0

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_construct_sudoku)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_fill_value)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_check_finished)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
        
    if 0:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_check_sanity)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
         
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_find_block_indices)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
              
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_erase_pencil)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)     
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_unfinished_rcnbrbc)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
        