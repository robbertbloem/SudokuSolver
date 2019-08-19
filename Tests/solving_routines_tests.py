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
            for _r in r:
                for _c in c:
                    for _n in n:
                        with self.subTest(test[3]):
                            self.assertTrue(numpy.all(s[_r,_c,0] == _n))  


        for test in test_no_pencil:
            r,c,n = make_range(test)
            for _r in r:
                for _c in c:
                    for _n in n:
                        with self.subTest(test[3]):
                            self.assertTrue(numpy.all(s[_r,_c,_n] == 0))  

        for test in tests_pencils:
            r,c,n = make_range(test)
            for _r in r:
                for _c in c:
                    for _n in n:
                        with self.subTest(test[3]):
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
            for _r in r:
                for _c in c:
                    for _n in n:
                        with self.subTest(test[3]):
                            self.assertTrue(numpy.all(s[_r,_c,0] == _n))  


        for test in test_no_pencil:
            r,c,n = make_range(test)
            for _r in r:
                for _c in c:
                    for _n in n:
                        with self.subTest(test[3]):
                            self.assertTrue(numpy.all(s[_r,_c,_n] == 0))  

        for test in tests_pencils:
            r,c,n = make_range(test)
            for _r in r:
                for _c in c:
                    for _n in n:
                        with self.subTest(test[3]):
                            self.assertTrue(numpy.all(s[_r,_c,_n] == _n))  


    def test_check_naked_pair_col(self):
        """
        Two squares can hold exactly two (the same) values. The values can be removed from the other squares in the column. 
        Pencil marks outside the column are not affected.
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
#             [0,0,1,"test test"]
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
        Similar to ``test_check_naked_pair_col``, but now with the number 1 already filled in. This is to test the mechanism where finished nums are not checked. 
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
        Similar to ``test_check_naked_pair_col``, but now with the a column already finished. This is to test the mechanism where finished cols are not checked. 
        The finished column is 0, the column with the naked pair is 1 with values 8 and 9. 
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
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [[1,2,3,5,6,7,8],1,[8,9], "no 8 or 9"],
        ]
        tests_pencils = [
            [[0,4],1,[8,9], "8 and 9 present"],
            [(0,6),2,[8,9], "8 and 9 present in c=2"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_naked_pair_col_with_col_complete_2(self):
        """
        Similar to above, but with naked pair in column 8 (the last column).
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
        test_filled = [
        ]
        test_no_pencil = [
            [[1,2,3,5,6,7,8],8,[8,9], "no 8 or 9"],
        ]
        tests_pencils = [
            [[0,4],8,[8,9], "8 and 9 present"],
            [(0,6),7,[8,9], "8 and 9 present in c=7"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_naked_pair_col_with_col_complete_3(self):
        """
        Similar to above, but with naked pair in column 0 (the last column).
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
        test_filled = [
        ]
        test_no_pencil = [
            [[1,2,3,5,6,7,8],0,[8,9], "no 8 or 9"],
        ]
        tests_pencils = [
            [[0,4],0,[8,9], "8 and 9 present"],
            [(0,6),1,[8,9], "8 and 9 present in c=1"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_naked_pair_col_with_row_complete(self):
        """
        As above, but now with a row complete.
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
        test_filled = [
        ]
        test_no_pencil = [
            [[1,2,3,4,5,6,7],1,[8,9], "no 8 or 9"],
        ]
        tests_pencils = [
            [[0,4],0,[8,9], "8 and 9 present"],
            [0,(0,6),[8,9], "8 and 9 present in top column"],
            [(2,9),0,[8,9], "8 and 9 present in c=0"],
            [(2,9),(2,6),[8,9], "8 and 9 present in columns (but not in left three cols because last two rows contain 8 and 9"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)
               
        
    def test_check_naked_pair_col_with_row_complete_2(self):
        """
        As above, but now with a row complete.
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
        test_filled = [
        ]
        test_no_pencil = [
            [[1,2,3,5,6,7,8],1,[8,9], "no 8 or 9"],
        ]
        tests_pencils = [
            [[0,4],0,[8,9], "8 and 9 present"],
            [0,(0,6),[8,9], "8 and 9 present in top column"],
            [(2,9),0,[8,9], "8 and 9 present in c=0"],
            [(2,9),(2,6),[8,9], "8 and 9 present in columns (but not in left three cols because last two rows contain 8 and 9"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)
    

    def test_check_naked_pair_row(self):
        """
        Naked pair in row 8. Other rows are not affected.
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
        test_filled = [
        ]
        test_no_pencil = [
            [8,[0,1,2,4,5,7,8],[8,9], "no 8 or 9"],
            [8,[3,6],(1,8), "not anything else then 8 or 9"],
        ]
        tests_pencils = [
            [8,[0,1,2,4,5,7,8],(1,8), "everything but 8 or 9"],
            [8,[3,6],[8,9], "8 or 9"],
            [(0,8),(0,9),(1,10), "other cells not affected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_naked_pair_block(self):
        """
        Naked pair in block (1,1) (middle). Only block is affected.
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
        test_filled = [
        ]
        test_no_pencil = [
            [3,[4,5],[8,9], "no 8 or 9"],
            [4,[3,5],[8,9], "no 8 or 9"],
            [5,[3,4,5],[8,9], "no 8 or 9"],
            [3,3,(1,8), "nothing but 8 and 9"],
            [4,4,(1,8), "nothing but 8 and 9"],
        ]
        tests_pencils = [
            [3,[4,5],(1,8), "everything but 8 or 9"],
            [4,[3,5],(1,8), "everything but 8 or 9"],
            [5,[3,4,5],(1,8), "everything but 8 or 9"],
            [3,3,[8,9], "nothing but 8 and 9"],
            [4,4,[8,9], "nothing but 8 and 9"],        
            [(0,9),(0,3),(1,10), "other cells not affected left 3 blocks"],
            [(0,3),(3,6),(1,10), "other cells not affected block above"],
            [(6,9),(3,6),(1,10), "other cells not affected block below"],
            [(0,9),(6,9),(1,10), "other cells not affected right 3 blocks"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_naked_pair_row_block(self):
        """
        Naked pair is in both block and row.
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
        test_filled = [
        ]
        test_no_pencil = [
            [3,5,[8,9], "no 8 or 9"],
            [[4,5],[3,4,5],[8,9], "no 8 or 9"],
            [3,3,(1,8), "nothing but 8 and 9"],
            [3,4,(1,8), "nothing but 8 and 9"],
        ]
        tests_pencils = [
            [3,(0,3),(1,8), "everything but 8 or 9 row left"],
            [3,(5,9),(1,8), "everything but 8 or 9 row right and one in block"],
            [[4,5],[3,4,5],(1,8), "everything but 8 or 9 block"],
            [3,3,[8,9], "nothing but 8 and 9"],
            [3,4,[8,9], "nothing but 8 and 9"],        
            [(0,3),(0,9),(1,10), "other cells not affected top 3 blocks"],
            [(6,9),(0,9),(1,10), "other cells not affected bottom 3 blocks"],
            [[4,5],(0,3),(1,10), "most other cells not affected block left"],
            [[4,5],(6,9),(1,10), "most other cells not affected block right"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)
        

    def test_check_naked_triple_row(self):
        """
        Naked triple in top row. Row should be affected, the rest not.
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
        test_filled = [
        ]
        test_no_pencil = [
            [0,[0,3,6],(1,7), "no 7, 8 or 9"],
            [0,[1,2,4,5,7,8],(7,10), "not 1-7"],
        ]
        tests_pencils = [
            [0,[0,3,6],[7,8,9], "nothing but 7, 8 or 9"],
            [0,[1,2,4,5,7,8],(1,7), "everything but 7, 8, 9"],
            [(1,9),(0,9),(1,10), "Other cells not affected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_naked_triple_row_partial(self):
        """
        Naked triple in top row. Not all cells contain the digit. Row should be affected, the rest not.
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
        test_filled = [
        ]
        test_no_pencil = [
            [0,[0,3,6],[1,3,4,5,7,9], "nothing but 2,6,8"],
            [0,[1,2,4,5,7,8],[2,6,8], "nothing but 2,6,8"],
            [0,6,8, "Partial naked triple, 8 misses"],
        ]
        tests_pencils = [
            [0,[0,3],[2,6,8], "nothing but 2,6,8"],
            [0,6,[2,6], "Partial naked triple, 8 misses"],
            [0,[1,2,4,5,7,8],[1,3,4,5,7,9], "nothing but 2,6,8"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_naked_triple_col(self):
        """
        Naked triple in column. Column should be affected, the rest not.
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
        test_filled = [
        ]
        test_no_pencil = [
            [[0,3,6],0,(1,7), "no 7, 8 or 9"],
            [[1,2,4,5,7,8],0,(7,10), "not 1-7"],
        ]
        tests_pencils = [
            [[0,3,6],0,[7,8,9], "nothing but 7, 8 or 9"],
            [[1,2,4,5,7,8],0,(1,7), "everything but 7, 8, 9"],
            [(0,9),(1,9),(1,10), "Other cells not affected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)        


    def test_check_naked_triple_col_with_1_complete(self):
        """
        Naked triple in column. 1 value is already finished Column should be affected, the rest not.
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
        test_filled = [
        ]
        test_no_pencil = [
            [[0,3,6],1,(1,7), "not 1-7"],
            [[1,2,4,5,7,8],1,(7,10), "not 1-7"],
        ]
        tests_pencils = [
            [[0,3,6],1,[7,8,9], "nothing but 7, 8 or 9"],
            [[2,4,5,7,8],1,(2,7), "everything but 7, 8, 9"],
            [(0,2),(2,9),(2,10), "Other cells not affected (limited)"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)        

        
    def test_check_naked_triple_block(self):
        """
        Naked triple in block. Only block should be affected.
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
        test_filled = [
        ]
        test_no_pencil = [ 
            [0,0,[1,3,4,5,7,9], "not other"],
            [2,0,[1,3,4,5,7,9], "not other"],
            [1,1,[1,3,4,5,7,9], "not other"],
            [0,[1,2],[2,6,8], "not vals"],
            [1,[0,2],[2,6,8], "not vals"],
            [2,[1,2],[2,6,8], "not vals"],
        ]
        tests_pencils = [
            [0,0,[2,6,8], "not other"],
            [2,0,[2,6,8], "not other"],
            [1,1,[2,6,8], "not other"],
            [0,[1,2],[1,3,4,5,7,9], "not vals"],
            [1,[0,2],[1,3,4,5,7,9], "not vals"],
            [2,[1,2],[1,3,4,5,7,9], "not vals"],  
            [(0,9),(3,9),(1,10), "others not affected 6 cols to left"],
            [(3,9),(0,3),(1,10), "others not affect 2 blocks below"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)        


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
        test_filled = [
        ]
        test_no_pencil = [
            [[0,3,4,6],0,(1,6), "no 6, 7, 8 or 9"],
            [[1,2,5,7,8],0,(6,10), "not 1-6"],
        ]
        tests_pencils = [
            [[0,3,4,6],0,[6,7,8,9], "nothing but 6, 7, 8 or 9"],
            [[1,2,5,7,8],0,(1,6), "everything but 6, 7, 8, 9"],
            [(0,9),(1,9),(1,10), "Other cells not affected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils) 
        

    def test_check_naked_quad_row(self):
        """
        Naked quad in a row.
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
        test_filled = [
        ]
        test_no_pencil = [
            [1,[1,4,5,7],(1,6), "not 6, 7, 8 or 9"],
            [1,[0,2,3,6,8],(6,10), "not 1-6"],
        ]
        tests_pencils = [
            [1,[1,4,5,7],[6,7,8,9], "nothing but 6, 7, 8 or 9"],
            [1,[0,2,3,6,8],(1,6), "everything but 6, 7, 8, 9"],
            [0,(0,9),(1,10), "Other cells not affected"],
            [(2,9),(0,9),(1,10), "Other cells not affected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


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
        test_filled = [
        ]
        test_no_pencil = [ 
            [0,0,[1,4,5,7,9], "not other"],
            [2,0,[1,4,5,7,9], "not other"],
            [1,1,[1,4,5,7,9], "not other"],
            [2,1,[1,4,5,7,9], "not other"],
            [0,[1,2],[2,3,6,8], "not vals"],
            [1,[0,2],[2,3,6,8], "not vals"],
            [2,2,[2,3,6,8], "not vals"],
        ]
        tests_pencils = [
            [0,0,[2,3,6,8], "not other"],
            [2,0,[2,3,6,8], "not other"],
            [1,1,[2,3,6,8], "not other"],
            [2,1,[2,3,6,8], "not other"],
            [0,[1,2],[1,4,5,7,9], "not vals"],
            [1,[0,2],[1,4,5,7,9], "not vals"],
            [2,2,[1,4,5,7,9], "not vals"],  
            [(0,9),(3,9),(1,10), "others not affected 6 cols to left"],
            [(3,9),(0,3),(1,10), "others not affect 2 blocks below"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)        


        
        for _rc in rc:
            self.assertTrue(numpy.all(s[_rc[0],_rc[1],_rc[2]] == 0))


class Test_check_hidden_subsets(unittest.TestCase):

    def setUp(self):
        self.verbose = 1


    def do_tests(self, s, test_filled, test_no_pencil, tests_pencils):
        for test in test_filled:
            r,c,n = make_range(test)
            for _r in r:
                for _c in c:
                    for _n in n:
                        with self.subTest(test[3]):
                            self.assertTrue(numpy.all(s[_r,_c,0] == _n))  


        for test in test_no_pencil:
            r,c,n = make_range(test)
            for _r in r:
                for _c in c:
                    for _n in n:
                        with self.subTest(test[3]):
                            self.assertTrue(numpy.all(s[_r,_c,_n] == 0))  

        for test in tests_pencils:
            r,c,n = make_range(test)
            for _r in r:
                for _c in c:
                    for _n in n:
                        with self.subTest(test[3]):
                            self.assertTrue(numpy.all(s[_r,_c,_n] == _n))  


    def test_check_hidden_pair_col(self):
        """
        Hidden pair: N digits are possible in N cells in a house. Other pencil marks should be removed from the N cells.
        
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_r = [4,6]
        c = 2
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = [1,3], verbose = self.verbose) 
        s = SSS.check_hidden_pair(s, self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
#             [0,0,1,"test test"]
        ]
        test_no_pencil = [
            [[4,6],2,[2,4,5,6,7,8,9], "removed pencil marks"],
            [[0,1,2,3,5,7,8],2,[1,3], "other cells don't contain 1 and 3"],
        ]
        tests_pencils = [
            [[4,6],2,[1,3], "remaining pencil marks"],
            [[0,1,2,3,5,7,8],2,[2,4,5,6,7,8,9], "remaining pencil marks other cells."], # more a test for erase function, really
            [(0,9),[0,1],(1,10), "cells to the left unaffected"],
            [(0,9),(3,9),(1,10), "cells to the right unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)
        
        
    def test_check_hidden_pair_row(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        
        r = 2
        except_c = [4,6]
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = [1,3], verbose = self.verbose) 
        s = SSS.check_hidden_pair(s, self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [2,[4,6],[2,4,5,6,7,8,9], "removed pencil marks"],
            [2,[0,1,2,3,5,7,8],[1,3], "other cells don't contain 1 and 3"],
        ]
        tests_pencils = [
            [2,[4,6],[1,3], "remaining pencil marks"],
            [2,[0,1,2,3,5,7,8],[2,4,5,6,7,8,9], "remaining pencil marks other cells."], # more a test for erase function, really
            [[0,1],(0,9),(1,10), "cells to the top unaffected"],
            [(3,9),(0,9),(1,10), "cells to the bottom unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)
        

    def test_check_hidden_pair_block(self):
        """
        Hidden pair: N digits are possible in N cells in a house. Other pencil marks should be removed from the N cells.
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        
        r = 2
        except_rc = [[1,4],[2,5]]
        s  = SSR.erase_pencil_block(s, br = 0, bc = 1, except_rc = except_rc, n = [1,3], verbose = self.verbose) 
        s = SSS.check_hidden_pair(s, self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [1,4,[2,4,5,6,7,8,9], "removed pencil marks"],
            [2,5,[2,4,5,6,7,8,9], "removed pencil marks"],
            [0,(3,6),[1,3], "other cells don't contain 1 and 3"],
            [1,[3,5],[1,3], "other cells don't contain 1 and 3"],
            [2,[3,4],[1,3], "other cells don't contain 1 and 3"],
        ]
        tests_pencils = [
            [1,4,[1,3], "remaining pencil marks"],
            [2,5,[1,3], "remaining pencil marks"],
            [(0,3),(0,3),(1,10), "cells to the left unaffected"],
            [(0,3),(6,9),(1,10), "cells to the right unaffected"],
            [(3,9),(0,9),(1,10), "cells to the bottom unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_hidden_pair_block_row(self):
        """
        Hidden pair: N digits are possible in N cells in a house. Other pencil marks should be removed from the N cells. In this case it exists in both a block and row. 
        Note: a naked pair is left. That has to be found with a different function.
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        

        except_rc = [[1,4],[1,5]]
        s  = SSR.erase_pencil_block(s, br = 0, bc = 1, except_rc = except_rc, n = [1,3], verbose = self.verbose) 
        r = 1
        s = SSS.check_hidden_pair(s, self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [1,[4,5],[2,4,5,6,7,8,9], "removed pencil marks"],
            [0,(3,6),[1,3], "other cells don't contain 1 and 3"],
            [1,3,[1,3], "other cells don't contain 1 and 3"],
            [2,(3,6),[1,3], "other cells don't contain 1 and 3"],
        ]
        tests_pencils = [
            [1,[4,5],[1,3], "remaining pencil marks"],
            [(0,3),(0,3),(1,10), "cells to the left unaffected"],
            [(0,3),(6,9),(1,10), "cells to the right unaffected"],
            [(3,9),(0,9),(1,10), "cells to the bottom unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)
        
    
    def test_check_hidden_triple_col(self):
        """
        Hidden triple: N digits are possible in N cells in a house. Other pencil marks should be removed from the N cells.
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_r = [2,4,6]
        c = 2
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = [1,3,7], verbose = self.verbose) 
        s = SSS.check_hidden_triple(s, self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [[2,4,6],2,[2,4,5,6,8,9], "removed pencil marks"],
            [[0,1,3,5,7,8],2,[1,3,7], "other cells don't contain 1, 3 and 7"],
        ]
        tests_pencils = [
            [[2,4,6],2,[1,3,7], "remaining pencil marks"],
            [[0,1,3,5,7,8],2,[2,4,5,6,8,9], "remaining pencil marks other cells."], # more a test for erase function, really
            [(0,9),[0,1],(1,10), "cells to the left unaffected"],
            [(0,9),(3,9),(1,10), "cells to the right unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


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
        test_filled = [
        ]
        test_no_pencil = [
            [[2,4,6],2,[2,4,5,6,8,9], "removed pencil marks"],
            [[0,1,3,5,7,8],2,[1,3,7], "other cells don't contain 1, 3 and 7"],
        ]
        tests_pencils = [
            [2,2,[3,7], "remaining pencil marks"],
            [4,2,[1,3], "remaining pencil marks"],
            [6,2,[1,3,7], "remaining pencil marks"],
            [[0,1,3,5,7,8],2,[2,4,5,6,8,9], "remaining pencil marks other cells."], # more a test for erase function, really
            [(0,9),[0,1],(1,10), "cells to the left unaffected"],
            [(0,9),(3,9),(1,10), "cells to the right unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)
        

    def test_check_hidden_triple_row(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        except_c = [2,4,6]
        r = 2
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = [1,3,7], verbose = self.verbose) 
        s = SSS.check_hidden_triple(s, self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [2,[2,4,6],[2,4,5,6,8,9], "removed pencil marks"],
            [2,[0,1,3,5,7,8],[1,3,7], "other cells don't contain 1 and 3"],
        ]
        tests_pencils = [
            [2,[2,4,6],[1,3,7], "remaining pencil marks"],
            [2,[0,1,3,5,7,8],[2,4,5,6,8,9], "remaining pencil marks other cells."], # more a test for erase function, really
            [[0,1],(0,9),(1,10), "cells to the top unaffected"],
            [(3,9),(0,9),(1,10), "cells to the bottom unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


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
        test_filled = [
        ]
        test_no_pencil = [
            [2,[2,4,6],[2,4,5,6,8,9], "removed pencil marks"],
            [2,[0,1,3,5,7,8],[1,3,7], "other cells don't contain 1 and 3"],
        ]
        tests_pencils = [
            [2,2,[3,7], "remaining pencil marks"],
            [2,4,[1,3], "remaining pencil marks"],
            [2,6,[1,3,7], "remaining pencil marks"],
            [2,[0,1,3,5,7,8],[2,4,5,6,8,9], "remaining pencil marks other cells."], # more a test for erase function, really
            [[0,1],(0,9),(1,10), "cells to the top unaffected"],
            [(3,9),(0,9),(1,10), "cells to the bottom unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)
        
        
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
        test_filled = [
        ]
        test_no_pencil = [
            [1,4,[2,4,5,6,8,9], "removed pencil marks"],
            [2,5,[2,4,5,6,8,9], "removed pencil marks"],
            [2,5,[2,4,5,6,8,9], "removed pencil marks"],
            [0,(3,6),[1,3,7], "other cells don't contain 1, 3, 7 A"],
            [1,5,[1,3,7], "other cells don't contain 1, 3, 7 B"],
            [2,[3,4],[1,3,7], "other cells don't contain 1, 3, 7 C"],
        ]
        tests_pencils = [
            [1,4,[1,3,7], "remaining pencil marks"],
            [2,5,[1,3,7], "remaining pencil marks"],
            [1,3,[1,3,7], "remaining pencil marks"],
            [(0,3),(0,3),(1,10), "cells to the left unaffected"],
            [(0,3),(6,9),(1,10), "cells to the right unaffected"],
            [(3,9),(0,9),(1,10), "cells to the bottom unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


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
        test_filled = [
        ]
        test_no_pencil = [
            [1,4,[2,4,5,6,8,9], "removed pencil marks"],
            [2,5,[2,4,5,6,8,9], "removed pencil marks"],
            [2,5,[2,4,5,6,8,9], "removed pencil marks"],
            [0,(3,6),[1,3,7], "other cells don't contain 1, 3, 7 A"],
            [1,5,[1,3,7], "other cells don't contain 1, 3, 7 B"],
            [2,[3,4],[1,3,7], "other cells don't contain 1, 3, 7 C"],
        ]
        tests_pencils = [
            [1,4,[3,7], "remaining pencil marks"],
            [2,5,[1,3], "remaining pencil marks"],
            [1,3,[1,3,7], "remaining pencil marks"],
            [(0,3),(0,3),(1,10), "cells to the left unaffected"],
            [(0,3),(6,9),(1,10), "cells to the right unaffected"],
            [(3,9),(0,9),(1,10), "cells to the bottom unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


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
        test_filled = [
        ]
        test_no_pencil = [
            [[2,4,6,8],2,[2,5,6,8,9], "removed pencil marks"],
            [[0,1,3,5,7],2,[1,3,4,7], "other cells don't contain 1, 3 and 7"],
        ]
        tests_pencils = [
            [[2,4,6,8],2,[1,3,4,7], "remaining pencil marks"],
            [[0,1,3,5,7],2,[2,5,6,8,9], "remaining pencil marks other cells."], # more a test for erase function, really
            [(0,9),[0,1],(1,10), "cells to the left unaffected"],
            [(0,9),(3,9),(1,10), "cells to the right unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)
        

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
        test_filled = [
        ]
        test_no_pencil = [
            [2,[2,4,6,8],[2,5,6,8,9], "removed pencil marks"],
            [2,[0,1,3,5,7],[1,3,4,7], "other cells don't contain 1 and 3"],
        ]
        tests_pencils = [
            [2,[2,4,6,8],[1,3,4,7], "remaining pencil marks"],
            [2,[0,1,3,5,7],[2,5,6,8,9], "remaining pencil marks other cells."], # more a test for erase function, really
            [[0,1],(0,9),(1,10), "cells to the top unaffected"],
            [(3,9),(0,9),(1,10), "cells to the bottom unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


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
        test_filled = [
        ]
        test_no_pencil = [
            [0,4,[4,5,6,8,9], "removed pencil marks"],
            [1,3,[4,5,6,8,9], "removed pencil marks"],
            [1,4,[4,5,6,8,9], "removed pencil marks"],
            [2,5,[4,5,6,8,9], "removed pencil marks"],
            [0,[3,5],[1,2,3,7], "other cells don't contain 1,2,3,7 top row of block"],
            [1,5,[1,2,3,7], "other cells don't contain 1,2,3,7 middle row of block"],
            [2,[3,4],[1,2,3,7], "other cells don't contain 1,2,3,7 bottom row of block"],
        ]
        tests_pencils = [
            [0,4,[1,2,3,7], "remaining pencil marks"],
            [1,3,[1,2,3,7], "remaining pencil marks"],
            [1,4,[1,2,3,7], "remaining pencil marks"],
            [2,5,[1,2,3,7], "remaining pencil marks"],
            [(0,3),(0,3),(1,10), "cells to the left unaffected"],
            [(0,3),(6,9),(1,10), "cells to the right unaffected"],
            [(3,9),(0,9),(1,10), "cells to the bottom unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)
        

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
        test_filled = [
        ]
        test_no_pencil = [
            [0,4,[4,5,6,8,9], "removed pencil marks"],
            [1,3,[4,5,6,8,9], "removed pencil marks"],
            [1,4,[4,5,6,8,9], "removed pencil marks"],
            [2,5,[4,5,6,8,9], "removed pencil marks"],
            [0,[3,5],[1,2,3,7], "other cells don't contain 1,2,3,7 top row of block"],
            [1,5,[1,2,3,7], "other cells don't contain 1,2,3,7 middle row of block"],
            [2,[3,4],[1,2,3,7], "other cells don't contain 1,2,3,7 bottom row of block"],
        ]
        tests_pencils = [
            [0,4,[2,3,7], "remaining pencil marks"],
            [1,3,[1,2,3,7], "remaining pencil marks"],
            [1,4,[1,2,3,7], "remaining pencil marks"],
            [2,5,[1,2,3,7], "remaining pencil marks"],
            [(0,3),(0,3),(1,10), "cells to the left unaffected"],
            [(0,3),(6,9),(1,10), "cells to the right unaffected"],
            [(3,9),(0,9),(1,10), "cells to the bottom unaffected"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


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





class Test_check_locked_sets(unittest.TestCase):

    def setUp(self):
        self.verbose = 1


    def do_tests(self, s, test_filled, test_no_pencil, tests_pencils):
        for test in test_filled:
            r,c,n = make_range(test)
            for _r in r:
                for _c in c:
                    for _n in n:
                        with self.subTest(test[3]):
                            self.assertTrue(numpy.all(s[_r,_c,0] == _n))  


        for test in test_no_pencil:
            r,c,n = make_range(test)
            for _r in r:
                for _c in c:
                    for _n in n:
                        with self.subTest(test[3]):
                            self.assertTrue(numpy.all(s[_r,_c,_n] == 0))  

        for test in tests_pencils:
            r,c,n = make_range(test)
            for _r in r:
                for _c in c:
                    for _n in n:
                        with self.subTest(test[3]):
                            self.assertTrue(numpy.all(s[_r,_c,_n] == _n))  


    def test_check_locked_set_experiment(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 0
        except_c = [0,1,2]
        n = [1]
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = n, verbose = self.verbose) 
                
        except_r = [3,4,5]
        c = 1
        n = [2]
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = n, verbose = self.verbose) 

        r = 4
        except_c = [0,1,2,6,7,8]
        n = [3]
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = n, verbose = self.verbose) 
        r = 5
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = n, verbose = self.verbose) 

        except_r = [0,1,2,3,4,5]
        c = 6
        n = [5]
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = n, verbose = self.verbose) 
        c = 7
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = n, verbose = self.verbose) 
       
        s = SSS.check_locked_sets(s, verbose = self.verbose)
#         SSD.display_pencil(s)

    def test_check_locked_sets_row_pointing(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 4
        except_c = [0,1,2,6,7,8]
        n = [3]
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = n, verbose = self.verbose) 
        r = 5
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = n, verbose = self.verbose) 
        r = 3
        c = 5
        s  = SSR.erase_pencil(s, r = r, c = c, n = n, verbose = self.verbose) 
        s = SSS.check_locked_sets(s, verbose = self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [3,(0,3),3, "removed pencil marks in row left"],
            [3,(6,9),3, "removed pencil marks in row right"],
        ]
        tests_pencils = [
            [3,(3,5),(1,10), "remaining pencil marks at intersection"],
            [[4,5],(3,6),[1,2,4,5,6,7,8,9], "remaining pencil marks except 3"],
            [(0,3),(0,9),(1,10), "no change above"],
            [[4,5],(0,3),(1,10), "no change left"],
            [[4,5],(6,9),(1,10), "no change right"],
            [(6,9),(0,9),(1,10), "no change below"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_locked_sets_col_pointing(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        c = 4
        except_r = [0,1,2,6,7,8]
        n = [3]
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = n, verbose = self.verbose) 
        c = 5
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = n, verbose = self.verbose) 
        c = 3
        r = 5
        s  = SSR.erase_pencil(s, r = r, c = c, n = n, verbose = self.verbose) 
        s = SSS.check_locked_sets(s, verbose = self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [(0,3),3,3, "removed pencil marks in col top"],
            [(6,9),3,3, "removed pencil marks in col bottom"],
        ]
        tests_pencils = [
            [(3,5),3,(1,10), "remaining pencil marks at intersection"],
            [(3,6),[4,5],[1,2,4,5,6,7,8,9], "remaining pencil marks except 3"],
            [(0,9),(0,3),(1,10), "no change above"],
            [(0,3),[4,5],(1,10), "no change left"],
            [(6,9),[4,5],(1,10), "no change right"],
            [(0,9),(6,9),(1,10), "no change below"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_locked_set_triple_row_pointing(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 4
        except_c = [0,1,2,6,7,8]
        n = [3]
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = n, verbose = self.verbose) 
        r = 5
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = n, verbose = self.verbose) 
        s = SSS.check_locked_sets(s, verbose = self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [3,(0,3),3, "removed pencil marks"],
            [3,(6,9),3, "removed pencil marks"],
        ]
        tests_pencils = [
            [3,(3,6),(1,10), "remaining pencil marks"],
            [[4,5],(3,6),[1,2,4,5,6,7,8,9], "remaining pencil marks"],
            [(0,3),(0,9),(1,10), "no change above"],
            [[4,5],(0,3),(1,10), "no change left"],
            [[4,5],(6,9),(1,10), "no change right"],
            [(6,9),(0,9),(1,10), "no change below"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_locked_set_triple_col_pointing(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        c = 4
        except_r = [0,1,2,6,7,8]
        n = [3]
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = n, verbose = self.verbose) 
        c = 5
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = n, verbose = self.verbose) 
        s = SSS.check_locked_sets(s, verbose = self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [(0,3),3,3, "removed pencil marks"],
            [(6,9),3,3, "removed pencil marks"],
        ]
        tests_pencils = [
            [(3,6),3,(1,10), "remaining pencil marks"],
            [(3,6),[4,5],[1,2,4,5,6,7,8,9], "remaining pencil marks"],
            [(0,9),(0,3),(1,10), "no change above"],
            [(0,3),[4,5],(1,10), "no change left"],
            [(6,9),[4,5],(1,10), "no change right"],
            [(0,9),(6,9),(1,10), "no change below"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_locked_sets_row_claiming(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 0
        except_c = [0,1,2]
        n = [1]
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = n, verbose = self.verbose) 
        r = 0
        c = 1
        s  = SSR.erase_pencil(s, r = r, c = c, n = n, verbose = self.verbose) 
        s = SSS.check_locked_sets(s, verbose = self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [[1,2],(0,3),1, "removed pencil marks"],
        ]
        tests_pencils = [
            [0,[0,2],(1,10), "remaining pencil marks intersection"],
            [0,1,(2,10), "remaining pencil marks not part of triple"],
            [[1,2],(0,3),(2,10), "remaining pencil marks rest of block"],
            [(1,9),(3,9),(1,10), "no change left"],
            [(3,9),(0,3),(1,10), "no change below"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_locked_sets_col_claiming(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        c = 0
        except_r = [0,2]
        n = [1]
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = n, verbose = self.verbose) 
        s = SSS.check_locked_sets(s, verbose = self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [(0,3),[1,2],1, "removed pencil marks"],
        ]
        tests_pencils = [
            [[0,2],0,(1,10), "remaining pencil marks intersection"],
            [1,0,(2,10), "remaining pencil marks not part of triple"],
            [(0,3),[1,2],(2,10), "remaining pencil marks rest of block"],
            [(3,9),(1,9),(1,10), "no change left"],
            [(0,3),(3,9),(1,10), "no change below"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_locked_set_triple_row_claiming(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        r = 0
        except_c = [0,1,2]
        n = [1]
        s  = SSR.erase_pencil_row(s, r = r, except_c = except_c, n = n, verbose = self.verbose) 
        s = SSS.check_locked_sets(s, verbose = self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [[1,2],(0,3),1, "removed pencil marks"],
        ]
        tests_pencils = [
            [0,(0,3),(1,10), "remaining pencil marks intersection"],
            [[1,2],(0,3),(2,10), "remaining pencil marks rest of block"],
            [(1,9),(3,9),(1,10), "no change left"],
            [(3,9),(0,3),(1,10), "no change below"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)


    def test_check_locked_set_triple_col_claiming(self):
        """
        """
        s = SSR.construct_sudoku(verbose = self.verbose)
        c = 0
        except_r = [0,1,2]
        n = [1]
        s  = SSR.erase_pencil_col(s, except_r = except_r, c = c, n = n, verbose = self.verbose) 
        s = SSS.check_locked_sets(s, verbose = self.verbose)
#         SSD.display_pencil(s)
        test_filled = [
        ]
        test_no_pencil = [
            [(0,3),[1,2],1, "removed pencil marks"],
        ]
        tests_pencils = [
            [(0,3),0,(1,10), "remaining pencil marks intersection"],
            [(0,3),[1,2],(2,10), "remaining pencil marks rest of block"],
            [(3,9),(1,9),(1,10), "no change left"],
            [(0,3),(3,9),(1,10), "no change below"],
        ]
        self.do_tests(s, test_filled, test_no_pencil, tests_pencils)



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
        
    if 0:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_check_wings)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_check_locked_sets)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
        
        
        
        
        