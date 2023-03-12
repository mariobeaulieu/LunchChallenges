#!/usr/bin/python3

# Sudoku Solver
from collections import Counter
import logging
import sys
import os
import copy
import re
# The following import requires: sudo pip install ansicolors
from colors import red, green, blue


class SolutionNotValid(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def set_value(self, v):
        logging.debug('Cell.setValue: Setting cell [' + repr(self.row+1) + ',' + repr(self.col+1) + '] to ' + repr(v))
        self.values = [v]

    def get_values(self):
        return self.values

    ###############################
    # del_values
    #
    # Delete a list of values from the list of possibilities in a cell
    # Returns a tuple:
    # True if only 1 possibility remains
    # n    the list of possibilities that were actually removed (will be used for 'undos')
    def del_values(self, values_to_remove):
        logging.debug('Cell.del_values-1: removing possibilities ' + repr(values_to_remove) + ' from cell [' + repr(self.row+1) + ',' + repr(self.col+1) + ']')
        for v in values_to_remove:
            if v in self.values:
                logging.debug('Cell.del_values-2: removing value ' + repr(v) + ' from cell (' + repr(self.row+1) + ',' + repr(self.col+1) + ') which had possibilities ' + repr(self.values))
                self.values.remove(v)
                logging.debug("Cell.del_values-3: After removal, cell has possibilities:" + repr(self.values))
                if len(self.values) == 0:
                    raise SolutionNotValid(
                        "Solution not valid when deleting " + repr(v) + " at [" + repr(self.row+1) + "][" + repr(
                            self.col+1) + "]")
                return len(self.values) == 1
        # Return True if the number of possible values of this cell is now 1
        return False

    ###############################
    # printCell
    #
    # Prints 1 line of a cell
    # If the cell has many possibilities, print 1,2,and/or3 for the 1st line, 4,5,and/or6 for 2nd, 7,8,and/or9 for 3rd
    # If the cell has only 1 possibility, return blank line for 1st or 3rd and the value for 2nd line in green
    def print_cell(self, line):
        # Each cell is 3 line high (lines 0,1,2) to display all its possibilities
        if len(self.values) == 1:
            if line == 1:
                s = repr(self.values[0])
                print(green(' ' + s + ' '), end='')
            else:
                print('   ', end='')
        else:
            for i in range(3 * line + 1, 3 * line + 4):
                if i in self.values:
                    print("%1i" % i, end='')
                else:
                    print(" ", end='')


class Game:
    def __init__(self):
        self.cells = [[Cell(j, i) for i in range(9)] for j in range(9)]

    ###############################
    #  setValue
    #
    #  Set a cell to a specific value and remove that value from the list of possibilities in that row, column, and box
    def set_value(self, row, col, value):
        self.cells[row][col].set_value(value)
        self.del_values_from_box(row, col, [value])
        self.del_values_from_row(row, col, [value])
        self.del_values_from_col(row, col, [value])

    ###############################
    #  del_valuesFromBox
    #
    #  Delete a list pf possibilities (in values) from all cells in a box except for the cell at [row,col]
    def del_values_from_box(self, row, col, values):
        logging.info('Game: del_valuesFromBox(' + repr(row+1) + ',' + repr(col+1) + ')')
        # Delete a value from all cells of that box
        # except for the cell at [row,col]
        # Cell at (row,col): what is the cell in the top le_ft corner of that box?
        cr = (row // 3) * 3
        cc = (col // 3) * 3
        return self.del_values(row, col, cr, cr + 3, cc, cc + 3, values)

    ###############################
    #  del_valuesFromRow
    #
    #  Delete a list pf possibilities (in values) from all cells in a row except for the cell at [row,col]
    def del_values_from_row(self, row, col, values):
        logging.info('Game: del_valuesFromRow(' + repr(row+1) + ',' + repr(col+1) + ')')
        return self.del_values(row, col, row, row + 1, 0, 9, values)

    ###############################
    #  del_valuesFromCol
    #
    #  Delete a list pf possibilities (in values) from all cells in a column except for the cell at [row,col]
    def del_values_from_col(self, row, col, values):
        logging.info('Game: del_valuesFromCol(' + repr(row+1) + ',' + repr(col+1) + ')')
        return self.del_values(row, col, 0, 9, col, col + 1, values)

    ###############################
    #  del_valuesFromListOfCells
    #
    #  Delete a list of possible values from a list of cells.
    #  cells is a list coordinates [r,c]
    def del_values_from_list_of_cells(self, cells, values):
        logging.info('Game: del_valuesFromListOfCells. Cells are ' + repr(cells) + ', values are ' + repr(values) + ')')
        for r, c in cells:
            done = self.cells[r][c].del_values(values)
            if done:
                v = self.cells[r][c].get_values()
                self.set_value(r, c, v[0])

    ###############################
    #  del_values
    #
    #  Delete values from the list of possibilities in cells in range of i0 to i1 rows and j0 to j2 columns.
    #  Except for the cell at the position [row,col]
    def del_values(self, row, col, i0, i1, j0, j1, values):
        logging.info('Game: del_values(' + repr(row+1) + ',' + repr(col+1) + ') for rows ' + repr(i0) + ' to ' + repr(i1) + ' and cols ' + repr(j0) + ' to ' + repr(j1))
        # This method deletes values from cells in rows i0 to i1 and columns j0 to j1 except for cell row,col
        # found_values is an array with coordinates of cells where after removing "values" only 1 value is now possible
        for i in range(i0, i1):
            for j in range(j0, j1):
                if not (i == row and j == col):
                    # try:
                    found_value = self.cells[i][j].del_values(values)
                    # except SolutionNotValid as problem:
                    #   raise SolutionNotValid(str(problem)+" in block ["+repr(row)+"]["+repr(col)+"]")
                    # If deleting that value results in a single possibility for that cell, we just found a value
                    # We need to eliminate that value from all other cells in this box, row, and column
                    if found_value:
                        v = self.cells[i][j].get_values()
                        self.set_value(i, j, v[0])

    ###############################
    #  Cell.find_loners
    #     This function finds if a value appears only once in the list of possibilities for a row, col, or box
    #
    def find_loners(self):
        nb_changes = 0
        for thing in 'row', 'col', 'box':
            for item in range(9):
                # Below, p is the list of possibilities for each cell, and w in the array of where each cell is
                if thing == 'row': p, w = self.get_row_possibilities(item)
                if thing == 'col': p, w = self.get_col_possibilities(item)
                if thing == 'box': p, w = self.get_box_possibilities(item)
                # Create a list of all possibilities without duplicates
                s = set()
                for a in p:
                    for b in a:
                        s.add(b)
                # Now for each of the items in s, if it appears only once in p it's a loner
                for v in s:
                    n = 0
                    for i in range(len(p)):
                        if v in p[i]:
                            n += 1
                            index = i
                    if n == 1:
                        # We have found a loner, remove it from all other possibilities in that thing
                        print ("Found value %i in [row,col] [%i,%i] is the only possibility for that %s"%(v, w[index][0]+1, w[index][1]+1, thing))
                        if debug: self.print_game()
                        self.set_value(w[index][0], w[index][1], v)
                        nb_changes += 1
        return nb_changes

    ###############################
    #  find_pairs
    #
    # Find if pairs of possibilities are present.
    def find_pairs(self):
        nb_changes = 0
        for thing in 'row', 'col', 'box':
            for item in range(9):
                # Below, p is the list of possibilities for each cell, and w in the array of where each cell is
                if thing == 'row': p, w = self.get_row_possibilities(item)
                if thing == 'col': p, w = self.get_col_possibilities(item)
                if thing == 'box': p, w = self.get_box_possibilities(item)
                for i in range(len(p) - 1):
                    if len(p[i]) != 2: continue
                    for j in range(i + 1, len(p)):
                        if p[j] == p[i]:
                            # Check if any of the values in p is in the list of cells to clear
                            need_to_clear = False
                            for k in range(len(p)):
                                if k != i and k != j and (p[i][0] in p[k] or p[i][1] in p[k]):
                                    need_to_clear = True
                                    break
                            if need_to_clear:
                                print ("In %s found pair of values %i and %i in [row,col] [%i,%i] and [%i,%i]" % (thing, p[i][0], p[i][1], w[i][0]+1, w[i][1]+1, w[j][0]+1, w[j][1]+1))
                                if debug: self.print_game()
                                # i and j are the indices of cells that contain the pair
                                # w contains the list of all cells with more than 1 possibility.
                                # We will use that list and remove items i and j to create the list of cells to remove the values
                                cells_to_clear = w[:]
                                # Remove j first because i<j and if we remove i then we would have to pop j-1
                                cells_to_clear.pop(j)
                                cells_to_clear.pop(i)
                                self.del_values_from_list_of_cells(cells_to_clear, p[i])
                                nb_changes += 1
                                break
        return nb_changes

    ###############################
    #  findTriplets
    #
    # Find if 3 values are the only possibilities in a set of 3 cells in a row, column, or box
    def findTriplets(self):
        nb_changes = 0
        for thing in 'row', 'col', 'box':
            for item in range(9):
                # Below, p is the list of possibilities for each cell, and w in the array of where each cell is
                if thing == 'row': p, w = self.get_row_possibilities(item)
                if thing == 'col': p, w = self.get_col_possibilities(item)
                if thing == 'box': p, w = self.get_box_possibilities(item)
                # If there are 3 unknown cells or less in that thing, triplets are useless
                if len(p) < 4: continue
                for i in range(len(p) - 2):
                    # If that cell has more than 3 possibilities, forget it
                    if len(p[i]) > 3: continue
                    for j in range(i + 1, len(p) - 1):
                        if len(p[j]) > 3: continue
                        if len(set(p[i] + p[j])) > 3: continue
                        for k in range(j + 1, len(p)):
                            s = list(set(p[i] + p[j] + p[k]))
                            if len(s) == 3:
                                need_to_clear = False
                                # Check first if thare is anything to clear from the other cells
                                for h in range(len(p)):
                                    if h != i and h != j and h != k and (s[0] in p[h] or s[1] in p[h] or s[2] in p[h]):
                                        need_to_clear = True
                                        break;
                                if need_to_clear:
                                    print ("In %s, found triplet %i,%i,%i in [row,col] [%i,%i],[%i,%i],[%i,%i]" % (thing, s[0], s[1], s[2], w[i][0]+1, w[i][1]+1, w[j][0]+1, w[j][1]+1, w[k][0]+1, w[k][1]+1))
                                    if debug: self.print_game()
                                    # We have found a triplet.
                                    # Remove those 3 values from all other cells in that thing
                                    cells_to_clear = w[:]
                                    cells_to_clear.pop(k)
                                    cells_to_clear.pop(j)
                                    cells_to_clear.pop(i)
                                    self.del_values_from_list_of_cells(cells_to_clear, s)
                                    nb_changes += 1
                                    break
        return nb_changes

    ###############################
    #  getPossibilities
    #
    #  Get the list of possibilities for all cells in rows r0 to r1(excl) and columns c0 to c1(excl) for which
    #  there are more than 1 possibility
    def getPossibilities(self, r0, r1, c0, c1):
        p = []  # p is the list of possibilities
        w = []  # w is where those were found (row,col)
        for i in range(r0, r1):
            for j in range(c0, c1):
                v = self.cells[i][j].get_values()
                if len(v) > 1:
                    p.append(v)
                    w.append([i, j])
        return p, w

    ###############################
    #  get_box_possibilities
    #                                        0,1,2
    # Get the list of possibilities in a box 3,4,5
    # Boxes are numbered as shown on right   6,7,8
    def get_box_possibilities(self, box):
        r0 = (box // 3) * 3  # r0 is the row number of the top left corner of that box
        c0 = (box % 3) * 3  # c0 is the col number of the top left corner of that box
        p, w = self.getPossibilities(r0, r0 + 3, c0, c0 + 3)
        return p, w

    ###############################
    #  get_row_possibilities
    #
    # Get the list of possibilities in a row
    def get_row_possibilities(self, r0):
        p, w = self.getPossibilities(r0, r0 + 1, 0, 9)
        return p, w

    ###############################
    #  get_col_possibilities
    #
    # Get the list of possibilities in a column
    def get_col_possibilities(self, c0):
        p, w = self.getPossibilities(0, 9, c0, c0 + 1)
        return p, w

    ###############################
    #  Cell.print_game
    #
    def print_game(self):
        horizontalLine = "+-------------------+-------------------+-------------------+"
        print(horizontalLine)
        for row in range(9):
            for line in range(4):
                if row % 3 == 2 and line == 3: break
                print('| ', end='')
                for col in range(9):
                    self.cells[row][col].print_cell(line)
                    print('   ', end='')
                    if col % 3 == 2: print('| ', end='')
                print()
            if row % 3 == 2: print(horizontalLine)
        print('done')

    ###############################
    def print_compact_game(self):
        for i in range(9):
            for j in range(9):
                if len(self.cells[i][j].values) == 1:
                    v = repr(self.cells[i][j].values[0])
                else:
                    v="?"
                if v != "0":
                    print("%s " % v, end='')
                else:
                    print('. ', end='')
                if j == 2 or j == 5: print("| ", end='')
            print()
            if i == 2 or i == 5: print("------+-------+------")
        print()


    #  Cell.print_compact_game
    #
    def print_game(self):
        horizontalLine = "+-------------------+-------------------+-------------------+"
        print(horizontalLine)
        for row in range(9):
            for line in range(4):
                if row % 3 == 2 and line == 3: break
                print('| ', end='')
                for col in range(9):
                    self.cells[row][col].print_cell(line)
                    print('   ', end='')
                    if col % 3 == 2: print('| ', end='')
                print()
            if row % 3 == 2: print(horizontalLine)
        print('done')


test_game = []
level = []

# test_game[0]: DEMO
level.append('TEST')
test_game.append([
    [1, 0, 0, 0, 8, 0, 0, 0, 6],
    [0, 2, 0, 0, 6, 0, 0, 7, 0],
    [0, 0, 3, 0, 1, 0, 8, 0, 0],
    [0, 0, 0, 4, 3, 9, 0, 0, 0],
    [3, 6, 9, 2, 5, 8, 1, 4, 7],
    [0, 0, 0, 1, 7, 6, 0, 0, 0],
    [0, 0, 2, 0, 9, 0, 7, 0, 0],
    [0, 3, 0, 0, 4, 0, 0, 8, 0],
    [4, 0, 0, 0, 2, 0, 0, 0, 9]])

# test_game[1]: EASY
level.append('EASY')
test_game.append([
    [0, 0, 0, 8, 0, 5, 0, 1, 3],
    [0, 0, 0, 2, 0, 3, 6, 0, 0],
    [6, 0, 0, 0, 9, 0, 2, 0, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 5],
    [0, 4, 0, 1, 0, 0, 7, 0, 6],
    [2, 5, 6, 3, 0, 4, 8, 9, 0],
    [5, 9, 0, 0, 0, 7, 1, 0, 2],
    [1, 0, 2, 0, 8, 0, 4, 7, 0],
    [0, 0, 4, 9, 1, 0, 0, 3, 8]])

# test_game[2]: MEDIUM
level.append('MEDIUM')
test_game.append([
    [0, 0, 0, 4, 0, 0, 2, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 1, 8],
    [5, 0, 6, 9, 0, 0, 0, 3, 0],
    [0, 6, 9, 0, 0, 0, 3, 0, 0],
    [0, 5, 0, 0, 0, 0, 0, 2, 1],
    [8, 0, 0, 1, 5, 7, 6, 0, 9],
    [0, 0, 0, 0, 3, 0, 9, 6, 0],
    [9, 0, 0, 6, 0, 2, 0, 5, 0],
    [0, 0, 0, 0, 0, 0, 7, 0, 2]])

# test_game[3]: HARD
level.append('HARD-1')
test_game.append([
    [0, 0, 7, 0, 0, 0, 3, 0, 2],
    [2, 0, 0, 0, 0, 5, 0, 1, 0],
    [0, 0, 0, 8, 0, 1, 4, 0, 0],
    [0, 1, 0, 0, 9, 6, 0, 0, 8],
    [7, 6, 0, 0, 0, 0, 0, 4, 9],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 3, 0, 0, 0],
    [8, 0, 1, 0, 6, 0, 0, 0, 0],
    [0, 0, 0, 7, 0, 0, 0, 6, 3]])

level.append('HARD-2')
test_game.append([
    [0, 0, 4, 8, 6, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 9, 0],
    [8, 0, 0, 0, 0, 9, 0, 6, 0],
    [5, 0, 0, 2, 0, 6, 0, 0, 1],
    [0, 2, 7, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 4, 3, 0, 0, 6],
    [0, 5, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 9, 0, 0, 0, 4, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 1, 5]])

# test_game[4]: EXPERT
level.append('EXPERT-1')
test_game.append([
    [0, 0, 0, 1, 9, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 0, 8],
    [0, 5, 0, 8, 3, 0, 4, 9, 6],
    [0, 0, 5, 0, 0, 0, 0, 6, 0],
    [0, 0, 0, 4, 0, 0, 1, 8, 0],
    [9, 2, 0, 0, 0, 1, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 2, 0, 0, 6, 4, 0],
    [5, 0, 0, 6, 0, 3, 0, 0, 0]])

# test_game[0]: DEMO
level.append('EXPERT-2')
test_game.append([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 9, 8],
    [0, 0, 5, 7, 0, 0, 0, 3, 0],
    [0, 0, 6, 0, 5, 0, 8, 0, 1],
    [0, 0, 0, 0, 6, 0, 0, 0, 0],
    [0, 7, 0, 9, 0, 0, 0, 0, 0],
    [0, 6, 8, 0, 0, 0, 4, 0, 7],
    [3, 4, 0, 0, 0, 0, 0, 0, 0],
    [0, 9, 0, 5, 0, 2, 6, 0, 0]])

# test_game[0]: EXPERT
level.append('EXPERT-3')
test_game.append([
    [5, 0, 0, 9, 0, 4, 0, 7, 0],
    [0, 0, 0, 0, 0, 7, 0, 0, 0],
    [0, 2, 0, 0, 1, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 6, 1, 0, 2, 0],
    [0, 8, 5, 4, 0, 0, 0, 0, 0],
    [4, 0, 0, 8, 0, 2, 0, 5, 0],
    [0, 0, 0, 7, 0, 0, 3, 9, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]])

# test_game[0]: EXPERT
level.append('EXPERT-4')
test_game.append([
    [0, 2, 0, 0, 0, 0, 8, 0, 1],
    [0, 0, 0, 0, 0, 6, 0, 0, 0],
    [4, 7, 0, 9, 0, 0, 2, 0, 0],
    [0, 0, 5, 0, 4, 0, 0, 3, 0],
    [7, 0, 0, 6, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 8, 0, 0, 4],
    [0, 0, 0, 5, 0, 0, 0, 0, 3],
    [0, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 6, 0, 1, 0, 0, 0, 0, 7]])


def brute_force(x, debug):
    global numberOfSolutions
    # Use brute force to finish it all
    # p is the list of possibilities for all unresolved cells
    # w is the list of coordinates for each of these cells
    p, w = x.getPossibilities(0, 9, 0, 9)
    # We will play on a copy of the game called 'y'
    # We keep 'x' to revert to it if our guess ends up being wrong
    y = copy.deepcopy(x)
    while len(p) > 0:
        # Find a cell with the minimum number of possibilities
        nb_poss = 9
        index = 0
        i = 0
        for poss in p:
            if len(poss) < nb_poss or len(poss) == 2:
                index = i
                nb_poss = len(poss)
            i += 1
        # Trying values from cell 'index'
        for possibility in p[index]:
            r, c = w[index]
            print("Brute force: trying value %i in cell [%i,%i]" % (possibility, r+1, c+1))
            try:
                y.set_value(r, c, possibility)
                rc = 1
                while rc > 0:
                    logging.debug("brute_force: Find pairs")
                    rc1 = y.find_pairs()
                    logging.debug("brute_force: Find Triplets")
                    rc2 = y.findTriplets()
                    logging.debug("brute_force: Finding values that can be only in 1 location")
                    rc3 = y.find_loners()
                    logging.debug("brute_force: found %i pairs, %i triplets, and %i loners" % (rc1, rc2, rc3))
                    rc = rc1 + rc2 + rc3
                # Calling brute_force will result in an exception if the solution is invalid or if
                # or after all possibilities from this try have been exhausted
                # So, if we return here, we have found a solution and that solution is 'y'
                brute_force(y, debug)
                y.print_compact_game()
            except SolutionNotValid:
                print("Brute force: Value %i at [%i,%i] didn't work out" % (possibility, r+1, c+1))
            # If we arrive here, our previous guess was wrong.
            # We now need to reset 'y' and try another one
            y = copy.deepcopy(x)
        # If we are here, then none of the possibilities from p[index] was good.
        # Return saying that we failed so another value can be tried
        return
    # Now if we are here, it means that all value have been found.
    # Success, return True with the game 'x'
    numberOfSolutions += 1
    print("A solution has been found !\nSolution %i is:" % (numberOfSolutions))
    if numberOfSolutions <= 10:
        x.print_game()
        input("Press ENTER")
    return


try:
    os.remove('sudoku.log')
except Exception:
    pass

logging.basicConfig(filename='sudoku.log', level=logging.DEBUG)

debug = False

n = len(test_game) - 1
if len(sys.argv) > 1:
    try:
        v = int(sys.argv[1])
    except:
        print("Usage: " + sys.argv[0] + " [game number]")
        sys.exit(0)
    if v > n:
        print("Invalid number: there are only", n, "games")
        sys.exit(0)
    n = v
else:
    print("Enter Sudoku grid.")
    print("Enter 81 digits without any space.")
    print("  0 means a blank case,")
    print("  1-9 will put that digit in the case")
    print("  Enter as many digits as you want on each line,")
    print("  the process ends when you reach 81 digits")
    grid = ''
    while len(grid) < 81:
        g = input("Enter digits: ")
        if re.search('\D', g) is None:
            grid += g
        else:
            print('You must use digits 0-9 only, no space or comma')
        if len(grid) < 81:
            print('%i more digits needed' % (81 - len(grid)))
    level.append('Interactive')
    test_game.append([])
    n = len(test_game) - 1
    i = 0
    for row in range(9):
        test_game[n].append([])
        for col in range(9):
            test_game[n][row].append(int(grid[i]))
            i += 1

print("Playing game number ", n, "of level", level[n])
x = Game()

for i in range(9):
    for j in range(9):
        v=test_game[n][i][j]
        if v != 0:
            print("%i " %v, end='')
        else:
            print('. ', end='')
        if j == 2 or j == 5: print("| ", end='')
    print()
    if i == 2 or i == 5: print("------+-------+------")
print()

numberOfSolutions = 0

for i in range(9):
    for j in range(9):
        v = test_game[n][i][j]
        if v != 0:
            x.set_value(i, j, v)
x.print_game()

rc = 1
while rc > 0:
    logging.debug("=======================Initial elimination: Find pairs=============================")
    rc1 = x.find_pairs()
    logging.debug("=====================Initial elimination: Find Triplets============================")
    rc2 = x.findTriplets()
    logging.debug("=========Initial elimination: Finding values that can be only in 1 location========")
    rc3 = x.find_loners()
    logging.debug("==========Initial elimination: found %i pairs, %i triplets, and %i loners==========" % (rc1, rc2, rc3))
    if debug: print("Initial elimination: found %i pairs, %i triplets, and %i loners" % (rc1, rc2, rc3))
    rc = rc1 + rc2 + rc3

p, w = x.getPossibilities(0, 9, 0, 9)
if len(p) > 0:
    print("This is the grid before brute force attempt:")
    x.print_game()
    input("Press ENTER")
    brute_force(x, debug)
else:
    print("This is the solution:")
    x.print_compact_game()
