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

import SudokuSolver.solving_routines as SSS
import SudokuSolver.routines as SSR
import SudokuSolver.display as SSD

importlib.reload(SSS)
importlib.reload(SSR)
importlib.reload(SSD)


def make_range_helper(t):
    if type(t) == tuple:
        res = numpy.arange(t[0], t[1], dtype = int)
    elif type(t) == list:
        res = numpy.array(t)
    else:
        res = numpy.array([t])
    return res



def make_range(test):

    r = make_range_helper(test[0])
    c = make_range_helper(test[1])
    n = make_range_helper(test[2])
    return r,c,n
    




class Test_singles(unittest.TestCase):

    def setUp(self):
        self.verbose = 1


    def do_tests(self, s, test_filled, test_no_pencil, tests_pencils):
        for test in test_filled:
            r,c,n = make_range(test)
#             self.assertTrue(numpy.all(s[r,c,0] == n))
            for _r in r:
                for _c in c:
                    for _n in n:
                        self.assertTrue(numpy.all(s[_r,_c,0] == _n))  


        for test in test_no_pencil:
            r,c,n = make_range(test)
#             print(r,c,n)
#             self.assertTrue(numpy.all(s[r,c,n] == 0))
            for _r in r:
                for _c in c:
                    for _n in n:
                        self.assertTrue(numpy.all(s[_r,_c,_n] == 0))  

        for test in tests_pencils:
            r,c,n = make_range(test)
            for _r in r:
                for _c in c:
                    for _n in n:
                        self.assertTrue(numpy.all(s[_r,_c,_n] == _n))  
     

    def test_check_last_digit(self):
        """
        Fill in last digit in a house.
        Number 1 in r=0, c=0.
        Check no pencil marks present in row and column.
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        s[0,0,2:10] = 0
        s, cc, f = SSS.check_last_digit(s, verbose = self.verbose)
        n_warnings = SSR.check_sanity(s)
#         SSD.display_pencil(s)
        self.assertTrue(n_warnings == 0)
        self.assertTrue(cc == 1)
        self.assertFalse(f)
        test_filled = [
            [0,0,1, "one"]
        ]
        test_no_pencil = [
            [0,(0,9),1, "one row"],
            [(0,9),0,1, "one col"],
            [(0,3),(0,3),1, "one block"]
        ]
        tests_pencils = [
            [(1,9),(3,9),(1,10), "all pencils A"],
            [(3,9),[1,2],(1,10), "all pencils B"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)

    def test_check_last_digit_sudoku_finished(self):
        """
        This is not a valid sudoku, but that is not important here. 
        """
        s = SSR.construct_sudoku(verbose = self.verbose)

        s[:,:,0] = 1
        s[0,0,0] = 0
        s[0,0,2:10] = 0
        s, cc, f = SSS.check_last_digit(s, verbose = self.verbose)
        
        with self.assertWarns(Warning):
            n_warnings = SSR.check_sanity(s)
            self.assertFalse(n_warnings == 0)

        self.assertTrue(s[0,0,0] == 1)
        self.assertTrue(cc == 1)
        self.assertTrue(f)


    def test_full_house_row_col(self):
        """
        Last possible location for a digit.
        Fill in [0,0,1] and [0,4,2].
        Check if pencil marks are removed from rows and cols.
        """
        s = SSR.construct_sudoku(verbose = self.verbose)

        s[0,1:,1] = 0
        s[1:,4,2] = 0
        s, cc, f = SSS.check_full_house(s, verbose = self.verbose)
        n_warnings = SSR.check_sanity(s)
        self.assertTrue(n_warnings == 0)
#         SSD.display_pencil(s)
        test_filled = [
            [0,0,1, "one"],
            [0,4,2, "two"]
        ]
        test_no_pencil = [
            [0,(0,9),1, "one row"],
            [(0,9),0,1, "one col"],
            [(0,3),(0,3),1, "one block"],
            [0,(0,9),2, "two row"],
            [(0,9),4,2, "two col"],
            [(0,3),(3,6),2, "two block"],
        ]
        tests_pencils = [
            [(3,9),[1,2,3,5],(1,10), "all pencils A"],
            [(1,9),(6,9),(1,10), "all pencils B"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)
        self.assertFalse(f)
        
        


    def test_full_house_block(self):
        """
        Last possible location for digit in a block
        
        """
        s = SSR.construct_sudoku(verbose = self.verbose)

        s[0:3,0:3,4] = 0
        s[1,1,4] = 4
        s, cc, f = SSS.check_full_house(s, verbose = self.verbose)
        n_warnings = SSR.check_sanity(s)
        self.assertTrue(n_warnings == 0)
        self.assertFalse(f)
#         SSD.display_pencil(s)
        test_filled = [
            [1,1,4, "four"],
        ]
        test_no_pencil = [
            [1,(0,9),4, "four row"],
            [(0,9),1,4, "four col"],
            [(0,3),(0,3),4, "four block"],
        ]
        tests_pencils = [
            [(2,9),(3,9),(1,10), "all pencils A"],
            [0,(3,9),(1,10), "all pencils B"],
            [(3,9),[0,2],(1,10), "all pencils C"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


class Test_check_naked_subsets(unittest.TestCase):

    def setUp(self):
        self.verbose = 1


    def do_tests(self, s, test_filled, test_no_pencil, tests_pencils):
        for test in test_filled:
            r,c,n = make_range(test)
#             self.assertTrue(numpy.all(s[r,c,0] == n))
            for _r in r:
                for _c in c:
                    for _n in n:
                        self.assertTrue(numpy.all(s[_r,_c,0] == _n))  


        for test in test_no_pencil:
            r,c,n = make_range(test)
#             print(r,c,n)
#             self.assertTrue(numpy.all(s[r,c,n] == 0))
            for _r in r:
                for _c in c:
                    for _n in n:
                        self.assertTrue(numpy.all(s[_r,_c,_n] == 0))  

        for test in tests_pencils:
            r,c,n = make_range(test)
            for _r in r:
                for _c in c:
                    for _n in n:
                        self.assertTrue(numpy.all(s[_r,_c,_n] == _n))  

    def test_check_naked_pair_col(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 0
        c = 0
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        r = 4
        c = 0
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        SSS.check_naked_pair(s, self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [[1,2,3,5,6,7,8],0,8, "no 8"],
            [[1,2,3,5,6,7,8],0,9, "no 9"],
        ]
        tests_pencils = [
            [(0,9),(1,9),(1,10), "all pencils A"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_naked_pair_col_with_1_complete(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        
        for i in range(9):        
            s, f = SSR.fill_value(s, i, i, 1, self.verbose)
        r = 1
        c = 0
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        r = 4
        c = 0
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        SSS.check_naked_pair(s, self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [[0,2,3,5,6,7,8],0,[8,9], "no 8 or 9"],
            [(0,9),(0,9),1, "no 1"],
            [[1,4],0,(1,8), "no 1-7 where 8 or 9"],
        ]
        tests_pencils = [
            [[1,4],0,[8,9], "8 and 9 present"],
            [[2,3,5,6,7,8],0,[2,3,4,5,6,7], "pencils present"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)



    def test_check_naked_pair_col_with_col_complete(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 0
        c = 1
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        r = 4
        c = 1
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        for i in range(9):
            s, f = SSR.fill_value(s, i, 0, i+1, self.verbose)
        
        SSS.check_naked_pair(s, self.verbose)
        SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [[1,2,3,5,6,7,8],1,[8,9], "no 8 or 9"],
#             [0,(0,9),1, "no 1"],
#             [[1,4],0, (1,8), "no 1"],
        ]
        tests_pencils = [
            [[0,4],1,[8,9], "8 and 9 present"],
            [(0,6),2,[8,9], "8 and 9 present in c=2"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)

        self.assertTrue(numpy.all(s[0,1,1:8] == 0))
        self.assertTrue(numpy.all(s[4,1,1:8] == 0))
        self.assertTrue(numpy.all(s[0,1,8:10] != 0))
        self.assertTrue(numpy.all(s[4,1,8:10] != 0))
        self.assertTrue(numpy.all(s[1:3,1,4:8] != 0))
        self.assertTrue(numpy.all(s[3,1,(1,2,3,7)] != 0))
        self.assertTrue(numpy.all(s[5,1,(1,2,3,7)] != 0))


    def test_check_naked_pair_col_with_col_complete_2(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 0
        c = 8
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        r = 4
        c = 8
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        for i in range(9):
            s, f = SSR.fill_value(s, i, 0, i+1, self.verbose)
        
        SSS.check_naked_pair(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[0,8,1:8] == 0))
        self.assertTrue(numpy.all(s[4,8,1:8] == 0))
        self.assertTrue(numpy.all(s[0,8,8:10] != 0))
        self.assertTrue(numpy.all(s[4,8,8:10] != 0))
        self.assertTrue(numpy.all(s[1:3,8,4:8] != 0))
        self.assertTrue(numpy.all(s[3,8,(1,2,3,7)] != 0))
        self.assertTrue(numpy.all(s[5,8,(1,2,3,7)] != 0))


    def test_check_naked_pair_col_with_col_complete_3(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 0
        c = 0
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        r = 4
        c = 0
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        for i in range(9):
            s, f = SSR.fill_value(s, i, 2, i+1, self.verbose)
        
        SSS.check_naked_pair(s, self.verbose)
#         SSD.display_pencil(s)
#         self.assertTrue(numpy.all(s[0,8,1:8] == 0))
#         self.assertTrue(numpy.all(s[4,8,1:8] == 0))
#         self.assertTrue(numpy.all(s[0,8,8:10] != 0))
#         self.assertTrue(numpy.all(s[4,8,8:10] != 0))
#         self.assertTrue(numpy.all(s[1:3,8,4:8] != 0))
#         self.assertTrue(numpy.all(s[3,8,(1,2,3,7)] != 0))
#         self.assertTrue(numpy.all(s[5,8,(1,2,3,7)] != 0))



    def test_check_naked_pair_col_with_row_complete(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 0
        c = 1
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        r = 8
        c = 1
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        for i in range(9):
            s, f = SSR.fill_value(s, 1, i, i+1, self.verbose)
        
        SSS.check_naked_pair(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[0,1,1:8] == 0))
        self.assertTrue(numpy.all(s[8,1,1:8] == 0))
        self.assertTrue(numpy.all(s[0,1,8:10] != 0))
        self.assertTrue(numpy.all(s[8,1,8:10] != 0))
#         self.assertTrue(numpy.all(s[2,1,4:8] != 0))
#         self.assertTrue(numpy.all(s[3,1,(1,3,4,5,6,7)] != 0))
#         self.assertTrue(numpy.all(s[5,1,(1,3,4,5,6,7)] != 0))
        
        
    def test_check_naked_pair_col_with_row_complete_2(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 0
        c = 1
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        r = 4
        c = 1
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        for i in range(9):
            s, f = SSR.fill_value(s, 1, i, i+1, self.verbose)
        
        SSS.check_naked_pair(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[0,1,1:8] == 0))
        self.assertTrue(numpy.all(s[4,1,1:8] == 0))
        self.assertTrue(numpy.all(s[0,1,8:10] != 0))
        self.assertTrue(numpy.all(s[4,1,8:10] != 0))
        self.assertTrue(numpy.all(s[2,1,4:8] != 0))
        self.assertTrue(numpy.all(s[3,1,(1,3,4,5,6,7)] != 0))
        self.assertTrue(numpy.all(s[5,1,(1,3,4,5,6,7)] != 0))
        

    def test_check_naked_pair_row(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 8
        c = 3
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        r = 8
        c = 6
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        SSS.check_naked_pair(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[8,3,1:8] == 0))
        self.assertTrue(numpy.all(s[8,6,1:8] == 0))
        self.assertTrue(numpy.all(s[8,3,8:10] != 0))
        self.assertTrue(numpy.all(s[8,6,8:10] != 0))
        self.assertTrue(numpy.all(s[8,4:6,8:10] == 0))
        self.assertTrue(numpy.all(s[8,4:6,1:8] != 0))



    def test_check_naked_pair_block(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 3
        c = 3
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        r = 4
        c = 4
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        SSS.check_naked_pair(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[3,3,1:8] == 0))
        self.assertTrue(numpy.all(s[4,4,1:8] == 0))
        self.assertTrue(numpy.all(s[3,3,8:10] != 0))
        self.assertTrue(numpy.all(s[4,4,8:10] != 0))
        self.assertTrue(numpy.all(s[0:3,0:3,1:10] != 0))
        self.assertTrue(numpy.all(s[6:,6:,1:10] != 0))


    def test_check_naked_pair_row_block(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 3
        c = 3
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        r = 3
        c = 4
        n = numpy.arange(7) + 1
        s  = SSR.erase_pencil(s, r, c, n, self.verbose)
        SSS.check_naked_pair(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[3,3,1:8] == 0))
        self.assertTrue(numpy.all(s[3,4,1:8] == 0))
        self.assertTrue(numpy.all(s[3,3,8:10] != 0))
        self.assertTrue(numpy.all(s[3,4,8:10] != 0))
        self.assertTrue(numpy.all(s[0:3,0:3,1:10] != 0))
        self.assertTrue(numpy.all(s[6:,6:,1:10] != 0))




    def test_check_naked_triple_row(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        rc = [
            [0,0],
            [0,3],
            [0,6],
        ]
        n = numpy.arange(6) + 1
        for _rc in rc:       
            s  = SSR.erase_pencil(s, _rc[0], _rc[1], n, self.verbose)
        SSS.check_naked_triple(s, self.verbose)
#         SSD.display_pencil(s) 
        for _rc in rc:
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],1:7] == 0))
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],7:10] != 0))
        
        self.assertTrue(numpy.all(s[0,1:3,1:7] != 0))
        self.assertTrue(numpy.all(s[0,1:3,7:10] == 0))
        





    def test_check_naked_triple_row_partial(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        rc = [
            [0,0,[1,  3,4,5,  7,  9]],
            [0,3,[1,  3,4,5,  7,  9]],
            [0,6,[1,  3,4,5,  7,8,9]],
        ]
        for _rc in rc:       
            s  = SSR.erase_pencil(s, _rc[0], _rc[1], _rc[2], self.verbose)
        s[0,1,2] = 0    
        SSS.check_naked_triple(s, self.verbose)
#         SSD.display_pencil(s) 
        for _rc in rc:
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],_rc[2]] == 0))




    def test_check_naked_triple_col(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        rc = [
            [0,0],
            [3,0],
            [6,0],
        ]
        n = numpy.arange(6) + 1
        for _rc in rc:       
            s  = SSR.erase_pencil(s, _rc[0], _rc[1], n, self.verbose)
        SSS.check_naked_triple(s, self.verbose)
#         SSD.display_pencil(s) 
        for _rc in rc:
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],1:7] == 0))
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],7:10] != 0))
        
        self.assertTrue(numpy.all(s[1:3,0,1:7] != 0))
        self.assertTrue(numpy.all(s[1:3,0,7:10] == 0))

    def test_check_naked_triple_col_with_1_complete(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        
        for i in range(9):        
            s, f = SSR.fill_value(s, i, i, 1, self.verbose)

        rc = [
            [0,1],
            [3,1],
            [6,1],
        ]
        n = numpy.arange(6) + 1
        for _rc in rc:       
            s  = SSR.erase_pencil(s, _rc[0], _rc[1], n, self.verbose) 
        SSS.check_naked_triple(s, self.verbose)
#         SSD.display_pencil(s) 
        for _rc in rc:
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],1:7] == 0))
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],7:10] != 0))
        
#         self.assertTrue(numpy.all(s[1:3,1,2:7] != 0))
        self.assertTrue(numpy.all(s[1:3,1,7:10] == 0))


        
    def test_check_naked_triple_block(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        rc = [
            [0,0,[1,  3,4,5,  7,  9]],
            [2,0,[1,  3,4,5,  7,  9]],
            [1,1,[1,  3,4,5,  7,  9]],
        ]
        for _rc in rc:       
            s  = SSR.erase_pencil(s, _rc[0], _rc[1], _rc[2], self.verbose)        
        SSS.check_naked_triple(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[0,0,(2,6,8)] != 0))
        self.assertTrue(numpy.all(s[2,0,(2,6,8)] != 0))
        self.assertTrue(numpy.all(s[1,1,(2,6,8)] != 0))
        self.assertTrue(numpy.all(s[0,0,rc[0][2]] == 0))
        self.assertTrue(numpy.all(s[2,0,rc[0][2]] == 0))
        self.assertTrue(numpy.all(s[1,1,rc[0][2]] == 0))
        self.assertTrue(numpy.all(s[3:,:,1:10] != 0))



    def test_check_naked_quad_col(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        rc = [
            [0,0],
            [3,0],
            [4,0],
            [6,0],
        ]
        n = numpy.arange(5) + 1
        for _rc in rc:       
            s  = SSR.erase_pencil(s, _rc[0], _rc[1], n, self.verbose)
        SSS.check_naked_quad(s, self.verbose)
#         SSD.display_pencil(s) 
        for _rc in rc:
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],1:6] == 0))
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],6:10] != 0))
        
        self.assertTrue(numpy.all(s[1:3,0,1:6] != 0))
        self.assertTrue(numpy.all(s[1:3,0,6:10] == 0))


    def test_check_naked_quad_row(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        rc = [
            [1,1],
            [1,4],
            [1,5],
            [1,7],
        ]
        n = numpy.arange(5) + 1
        for _rc in rc:       
            s  = SSR.erase_pencil(s, _rc[0], _rc[1], n, self.verbose)
        SSS.check_naked_quad(s, self.verbose)
#         SSD.display_pencil(s) 
        for _rc in rc:
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],1:6] == 0))
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],6:10] != 0))
        
        self.assertTrue(numpy.all(s[0,:,1:10] != 0))



    def test_check_naked_quad_block(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        rc = [
            [0,0,[1,    4,5,  7,  9]],
            [2,0,[1,    4,5,  7,  9]],
            [1,1,[1,    4,5,  7,  9]],
            [2,1,[1,    4,5,  7,  9]],
        ]
        for _rc in rc:       
            s  = SSR.erase_pencil(s, _rc[0], _rc[1], _rc[2], self.verbose)        
        SSS.check_naked_quad(s, self.verbose)
#         SSD.display_pencil(s)
        for _rc in rc:
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],_rc[2]] == 0))



class Test_check_hidden_subsets(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_check_hidden_pair_col(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_r = [4,6]
        c = 2
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = [1,3], verbose = self.verbose) 
        s = SSS.check_hidden_pair(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[4,2,(1,3)] != 0))
        self.assertTrue(numpy.all(s[6,2,(1,3)] != 0))
        self.assertTrue(numpy.all(s[0:4,2,(1,3)] == 0))
        self.assertTrue(numpy.all(s[5,2,(1,3)] == 0))
        self.assertTrue(numpy.all(s[7:9,2,(1,3)] == 0))
        self.assertTrue(numpy.all(s[0:9,3:,(1,3)] != 0))
        
    def test_check_hidden_pair_row(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        
        r = 2
        except_c = [4,6]
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = [1,3], verbose = self.verbose) 
        s = SSS.check_hidden_pair(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[2,4,(1,3)] != 0))
        self.assertTrue(numpy.all(s[2,6,(1,3)] != 0))
        self.assertTrue(numpy.all(s[2,0:4,(1,3)] == 0))
        self.assertTrue(numpy.all(s[2,5,(1,3)] == 0))
        self.assertTrue(numpy.all(s[2,7:9,(1,3)] == 0))
        self.assertTrue(numpy.all(s[3:,0:9,(1,3)] != 0))


    def test_check_hidden_pair_block(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        
        r = 2
        except_rc = [[1,4],[2,5]]
        s  = SSR.erase_pencil_block(s, br = 0, bc = 1, except_rc = except_rc, n = [1,3], verbose = self.verbose) 
        s = SSS.check_hidden_pair(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[1,4,(1,3)] != 0))
        self.assertTrue(numpy.all(s[2,5,(1,3)] != 0))
        self.assertTrue(numpy.all(s[0,3:6,(1,3)] == 0))


    def test_check_hidden_pair_block_row(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        

        except_rc = [[1,4],[1,5]]
        s  = SSR.erase_pencil_block(s, br = 0, bc = 1, except_rc = except_rc, n = [1,3], verbose = self.verbose) 
        r = 1
        except_c = [4,5]
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = [1,3], verbose = self.verbose) 
        s = SSS.check_hidden_pair(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[1,4,(1,3)] != 0))
        self.assertTrue(numpy.all(s[1,5,(1,3)] != 0))
        self.assertTrue(numpy.all(s[0,3:6,(1,3)] == 0))


    def test_check_hidden_triple_col(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_r = [2,4,6]
        c = 2
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = [1,3,7], verbose = self.verbose) 
        s = SSS.check_hidden_triple(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[2,2,(1,3,7)] != 0))
        self.assertTrue(numpy.all(s[4,2,(1,3,7)] != 0))
        self.assertTrue(numpy.all(s[6,2,(1,3,7)] != 0))
        self.assertTrue(numpy.all(s[0:2,2,(1,3,7)] == 0))
        self.assertTrue(numpy.all(s[3,2,(1,3,7)] == 0))
        self.assertTrue(numpy.all(s[5,2,(1,3,7)] == 0))
        self.assertTrue(numpy.all(s[7:9,2,(1,3,7)] == 0))


    def test_check_hidden_triple_col_incomplete(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_r = [2,4,6]
        c = 2
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = [1,3,7], verbose = self.verbose) 
        s[2,2,1] = 0
        s[4,2,7] = 0
        s = SSS.check_hidden_triple(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[2,2,(3,7)] != 0))
        self.assertTrue(numpy.all(s[4,2,(1,3)] != 0))
        self.assertTrue(numpy.all(s[6,2,(1,3,7)] != 0))
        self.assertTrue(numpy.all(s[0:2,2,(1,3,7)] == 0))
        self.assertTrue(numpy.all(s[3,2,(1,3,7)] == 0))
        self.assertTrue(numpy.all(s[5,2,(1,3,7)] == 0))
        self.assertTrue(numpy.all(s[7:9,2,(1,3,7)] == 0))


    def test_check_hidden_triple_row(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_c = [2,4,6]
        r = 2
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = [1,3,7], verbose = self.verbose) 
        s = SSS.check_hidden_triple(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[2,2,(1,3,7)] != 0))
        self.assertTrue(numpy.all(s[2,4,(1,3,7)] != 0))
        self.assertTrue(numpy.all(s[2,6,(1,3,7)] != 0))
        self.assertTrue(numpy.all(s[2,0:2,(1,3,7)] == 0))
        self.assertTrue(numpy.all(s[2,3,(1,3,7)] == 0))
        self.assertTrue(numpy.all(s[2,5,(1,3,7)] == 0))
        self.assertTrue(numpy.all(s[2,7:9,(1,3,7)] == 0))


    def test_check_hidden_triple_row_incomplete(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_c = [2,4,6]
        r = 2
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = [1,3,7], verbose = self.verbose) 
        s[2,2,1] = 0
        s[2,4,7] = 0
        s = SSS.check_hidden_triple(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[2,2,(3,7)] != 0))
        self.assertTrue(numpy.all(s[2,4,(1,3)] != 0))
        self.assertTrue(numpy.all(s[2,6,(1,3,7)] != 0))
        self.assertTrue(numpy.all(s[2,0:2,(1,3,7)] == 0))
        self.assertTrue(numpy.all(s[2,3,(1,3,7)] == 0))
        self.assertTrue(numpy.all(s[2,5,(1,3,7)] == 0))
        self.assertTrue(numpy.all(s[2,7:9,(1,3,7)] == 0))




    def test_check_hidden_triple_block(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_rc = numpy.array([[1,4],[2,5],[1,3]])
        br = 0
        bc = 1
        s  = SSR.erase_pencil_block(s, br = br, bc = bc, except_rc = except_rc, n = [1,3,7], verbose = self.verbose) 
        s = SSS.check_hidden_triple(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[1,3,(1,3,7)] != 0))
        self.assertTrue(numpy.all(s[1,4,(1,3,7)] != 0))
        self.assertTrue(numpy.all(s[2,5,(1,3,7)] != 0))
        self.assertTrue(numpy.all(s[0,3:6,(1,3,7)] == 0))


    def test_check_hidden_triple_block_incomplete(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_rc = numpy.array([[1,4],[2,5],[1,3]])
        br = 0
        bc = 1
        s  = SSR.erase_pencil_block(s, br = br, bc = bc, except_rc = except_rc, n = [1,3,7], verbose = self.verbose) 
        s[1,4,1] = 0
        s[2,5,7] = 0
        s = SSS.check_hidden_triple(s, self.verbose)
#         SSD.display_pencil(s)
        self.assertTrue(numpy.all(s[1,3,(1,3,7)] != 0))
        self.assertTrue(numpy.all(s[1,4,(3,7)] != 0))
        self.assertTrue(numpy.all(s[2,5,(1,3)] != 0))
        self.assertTrue(numpy.all(s[0,3:6,(1,3,7)] == 0))


    def test_check_hidden_quad_col(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_r = [2,4,6,8]
        c = 2
        n = [1,3,4,7]
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = n, verbose = self.verbose) 
        s = SSS.check_hidden_quad(s, self.verbose)
#         SSD.display_pencil(s)
        for _r in except_r:
            self.assertTrue(numpy.all(s[_r,2,n] != 0))
        self.assertTrue(numpy.all(s[0:2,c,n] == 0))
        self.assertTrue(numpy.all(s[3,c,n] == 0))
        self.assertTrue(numpy.all(s[5,c,n] == 0))
        self.assertTrue(numpy.all(s[7,c,n] == 0))


    def test_check_hidden_quad_row(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_c = [2,4,6,8]
        r = 2
        n = [1,3,4,7]
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = n, verbose = self.verbose) 
        s = SSS.check_hidden_quad(s, self.verbose)
#         SSD.display_pencil(s)
        for _c in except_c:
            self.assertTrue(numpy.all(s[r,_c,n] != 0))
        self.assertTrue(numpy.all(s[r,0:2,n] == 0))
        self.assertTrue(numpy.all(s[r,3,n] == 0))
        self.assertTrue(numpy.all(s[r,5,n] == 0))
        self.assertTrue(numpy.all(s[r,7,n] == 0))


    def test_check_hidden_quad_block(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_rc = numpy.array([[0,4],[1,3],[1,4],[2,5]])
        br = 0
        bc = 1
        n = [1,2,3,7]
        s  = SSR.erase_pencil_block(s, br = br, bc = bc, except_rc = except_rc, n = n, verbose = self.verbose) 
        s = SSS.check_hidden_quad(s, self.verbose)
#         SSD.display_pencil(s)
        for _rc in except_rc:
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],n] != 0))  


    def test_check_hidden_quad_block_incomplete(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_rc = numpy.array([[0,4],[1,3],[1,4],[2,5]])
        br = 0
        bc = 1
        n = [1,2,3,7]
        s  = SSR.erase_pencil_block(s, br = br, bc = bc, except_rc = except_rc, n = n, verbose = self.verbose) 
        s[0,4,1] = 0
        s = SSS.check_hidden_quad(s, self.verbose)
#         SSD.display_pencil(s)
        for _rc in except_rc:
            if _rc[0] == 0:
                self.assertTrue(numpy.all(s[_rc[0],_rc[1],[2,3,7]] != 0))  
            else:
                self.assertTrue(numpy.all(s[_rc[0],_rc[1],n] != 0))  



class Test_check_wings(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_check_wing_double_col(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_r = [4,6]
        c = [2,6]
        n = [4]
        for _c in c:
            s  = SSR.erase_pencil_col(s, except_r = except_r, c = _c, n = n, verbose = self.verbose) 
        
        
#         s = SSS.check_wing_double(s, self.verbose)
#         SSD.display_pencil(s)
#         self.assertTrue(numpy.all(s[4,2,(1,3)] != 0))
#         self.assertTrue(numpy.all(s[6,2,(1,3)] != 0))
#         self.assertTrue(numpy.all(s[0:4,2,(1,3)] == 0))
#         self.assertTrue(numpy.all(s[5,2,(1,3)] == 0))
#         self.assertTrue(numpy.all(s[7:9,2,(1,3)] == 0))
#         self.assertTrue(numpy.all(s[0:9,3:,(1,3)] != 0))


    def test_check_wing_triple_col(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_r = [4,6,8]
        c = [2,4,6]
        n = [4]
        for _c in c:
            s  = SSR.erase_pencil_col(s, except_r = except_r, c = _c, n = n, verbose = self.verbose) 
        s[4,4,4] = 0
        
        
#         s = SSS.check_wing_double(s, self.verbose)
#         SSD.display_pencil(s)
#         self.assertTrue(numpy.all(s[4,2,(1,3)] != 0))
#         self.assertTrue(numpy.all(s[6,2,(1,3)] != 0))
#         self.assertTrue(numpy.all(s[0:4,2,(1,3)] == 0))
#         self.assertTrue(numpy.all(s[5,2,(1,3)] == 0))
#         self.assertTrue(numpy.all(s[7:9,2,(1,3)] == 0))
#         self.assertTrue(numpy.all(s[0:9,3:,(1,3)] != 0))




if __name__ == "__main__": 

    verbosity = 0

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_singles)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_check_naked_subsets)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_check_hidden_subsets)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_check_wings)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
        
        
        
        
        
        
        