#!/usr/bin/python

# Sudoku Solver
from collections import Counter
import logging
import sys
import os
import copy

# The following import requires: sudo pip install ansicolors
from colors import red,green,blue

class SolutionNotValid(Exception):
   def __init__(self,mismatch):
      Exception.__init__(self,mismatch)

class Cell:
   def __init__(self,row,col):
      self.row   = row
      self.col   = col
      self.values= [1,2,3,4,5,6,7,8,9]
   def setValue(self,v):
      logging.debug('Cell.setValue: Setting cell ['+repr(self.row)+','+repr(self.col)+'] to '+repr(v))
      self.values= [v]
   def getValues(self):
      return self.values
   ###############################
   # delValues
   #
   # Delete a list of values from the list of possibilities in a cell
   # Returns a tuple:
   # True if only 1 possibility remains
   # n    the list of possibilities that were actually removed (will be used for 'undos')
   def delValues(self,valuesToRemove):
      logging.debug('Cell.delValues-1: removing possibilities '+repr(valuesToRemove)+' from cell ['+repr(self.row)+','+repr(self.col)+']')
      for v in valuesToRemove:
         if v in self.values:
            logging.debug('Cell.delValues-2: removing value '+repr(v)+' from cell ('+repr(self.row)+','+repr(self.col)+') which had possibilities '+repr(self.values))
            self.values.remove(v)
            logging.debug("Cell.delValues-3: After removal, cell has possibilities:"+repr(self.values))
            if len(self.values) == 0:
               raise SolutionNotValid("Solution not valid when deleting "+repr(v)+" at ["+repr(self.row)+"]["+repr(self.col)+"]")
            return (len(self.values) == 1)
      # Return True if the number of possible values of this cell is now 1
      return False
   ###############################
   # printCell
   #
   # Prints 1 line of a cell
   # If the cell has many possibilities, print 1,2,and/or3 for the 1st line, 4,5,and/or6 for 2nd, 7,8,and/or9 for 3rd
   # If the cell has only 1 possibility, return blank line for 1st or 3rd and the value for 2nd line in green
   def printCell(self,line):
      # Each cell is 3 line high (lines 0,1,2) to display all its possibilities
      s=''
      if len(self.values)==1:
         if line==1:
            s=repr(self.values[0])
            print green(' '+s+' '),
         else:
            print '   ',
      else:
         for i in range(3*line+1,3*line+4):
            if i in self.values:
               s+=repr(i)
            else:
               s+=' '
         print s,
      
class Game:
   def __init__(self):
      self.cells=[[Cell(j,i) for i in range(9)] for j in range(9)]
   ###############################
   #  setValue
   #
   #  Set a cell to a specific value and remove that value from the list of possibilities in that row, column, and box
   def setValue(self,row,col,value):
      self.cells[row][col].setValue(value)
      self.delValuesFromBox(row,col,[value])
      self.delValuesFromRow (row,col,[value])
      self.delValuesFromCol (row,col,[value])
   ###############################
   #  delValuesFromBox
   #
   #  Delete a list pf possibilities (in values) from all cells in a box except for the cell at [row,col]
   def delValuesFromBox(self,row,col,values):
      logging.info('Game: delValuesFromBox('+repr(row)+','+repr(col)+')')
      # Delete a value from all cells of that box
      # except for the cell at [row,col]
      # Cell at (row,col): what is the cell in the top left corner of that box?
      cr = (row/3) * 3
      cc = (col/3) * 3
      return self.delValues(row,col,cr,cr+3,cc,cc+3,values)
   ###############################
   #  delValuesFromRow
   #
   #  Delete a list pf possibilities (in values) from all cells in a row except for the cell at [row,col]
   def delValuesFromRow(self,row,col,values):
      logging.info('Game: delValuesFromRow('+repr(row)+','+repr(col)+')')
      return self.delValues(row,col,row,row+1,0,9,values)
   ###############################
   #  delValuesFromCol
   #
   #  Delete a list pf possibilities (in values) from all cells in a column except for the cell at [row,col]
   def delValuesFromCol(self,row,col,values):
      logging.info('Game: delValuesFromCol('+repr(row)+','+repr(col)+')')
      return self.delValues(row,col,0,9,col,col+1,values)
   ###############################
   #  delValuesFromListOfCells
   #
   #  Delete a list of possible values from a list of cells.
   #  cells is a list coordinates [r,c]
   def delValuesFromListOfCells(self,cells,values):
      logging.info('Game: delValuesFromListOfCells. Cells are '+repr(cells)+', values are '+repr(values)+')')
      for r,c in cells:
         done = self.cells[r][c].delValues(values)
         if done:
            v = self.cells[r][c].getValues()
            self.cells[r][c].setValue(v[0])
   ###############################
   #  delValues
   #
   #  Delete values from the list of possibilities in cells in range of i0 to i1 rows and j0 to j2 columns.
   #  Except for the cell at the position [row,col]
   def delValues(self,row,col,i0,i1,j0,j1,values):
      logging.info('Game: delValues('+repr(row)+','+repr(col)+') for rows '+repr(i0)+' to '+repr(i1)+' and cols '+repr(j0)+' to '+repr(j1))
      # This method deletes values from cells in rows i0 to i1 and columns j0 to j1 except for cell row,col
      # foundValues is an array with coordinates of cells where after removing "values" only 1 value is now possible
      for i in range(i0,i1):
         for j in range(j0,j1):
            if not (i == row and j == col):
               #try:
               foundValue = self.cells[i][j].delValues(values)
               #except SolutionNotValid as problem:
               #   raise SolutionNotValid(str(problem)+" in block ["+repr(row)+"]["+repr(col)+"]")
               # If deleting that value results in a single possibility for that cell, we just found a value
               # We need to eliminate that value from all other cells in this box, row, and column
               if foundValue:
                  v=self.cells[i][j].getValues()
                  self.setValue(i,j,v[0])
   ###############################
   #  Cell.findLoners
   #     This function finds if a value appears only once in the list of possibilities for a row, col, or box
   #
   def findLoners(self):
      nbChanges=0
      for thing in 'row','col','box':
         for item in range(9):
            # Below, p is the list of possibilities for each cell, and w in the array of where each cell is
            if thing == 'row': p,w = self.getRowPossibilities(item)
            if thing == 'col': p,w = self.getColPossibilities(item)
            if thing == 'box': p,w = self.getBoxPossibilities(item)
            # Create a list of all possibilities without duplicates
            s=set()
            for a in p:
               for b in a:
                  s.add(b)
            # Now for each of the items in s, if it appears only once in p it's a loner
            for v in s:
              n=0
              for i in range(len(p)):
                 if v in p[i]:
                    n+=1
                    index=i
              if n == 1:
                 # We have found a loner, remove it from all other possibilities in that thing
                 logging.debug('Game.findLoners: On '+thing+' '+repr(item)+',found value '+repr(v)+' is only possible in cell ['+repr(w[index][0])+','+repr(w[index][1])+']')
                 self.setValue(w[index][0],w[index][1],v)
                 nbChanges += 1
      return nbChanges

   ###############################
   #  getPossibilities
   #
   #  Get the list of possibilities for all cells in rows r0 to r1(excl) and columns c0 to c1(excl) for which 
   #  there are more than 1 possibility
   def getPossibilities(self,r0,r1,c0,c1):
      p=[] # p is the list of possibilities
      w=[] # w is where those were found (row,col)
      for i in range(r0,r1):
         for j in range(c0,c1):
            v=self.cells[i][j].getValues()
            if len(v)>1:
               p.append(v)
               w.append([i,j])
      return p,w
   ###############################
   #  getBoxPossibilities
   #                                        0,1,2
   # Get the list of possibilities in a box 3,4,5
   # Boxes are numbered as shown on right   6,7,8
   def getBoxPossibilities(self,box):
      r0 = (box/3)*3 # r0 is the row number of the top left corner of that box
      c0 = (box%3)*3 # c0 is the col number of the top left corner of that box
      p,w  = self.getPossibilities(r0,r0+3,c0,c0+3)
      return p,w
   ###############################
   #  getRowPossibilities
   #
   # Get the list of possibilities in a row
   def getRowPossibilities(self,r0):
      p,w  = self.getPossibilities(r0,r0+1,0,9)
      return p,w
   ###############################
   #  getColPossibilities
   #
   # Get the list of possibilities in a column
   def getColPossibilities(self,c0):
      p,w  = self.getPossibilities(0,9,c0,c0+1)
      return p,w
   ###############################
   #  findPairs
   #
   # Find if pairs of possibilities are present.
   # Return the list of pairs found
   #   p is the list of possibilities (array of arrays)
   #   w is the list of coordinates [row,col] for the possibilities tuples
   def findPairs(self,p,w):
      for i in range(len(p)-1):
         if len(p[i]) != 2: continue
         for j in range(i+1,len(p)):
            if p[j] == p[i]:
               # i and j are the indices of cells that contain the pair
               # w contains the list of all cells with more than 1 possibility.
               # We will use that list and remove items i and j to create the list of cells to remove the values
               cellsToClear=w[:]
               # Remove j first because i<j and if we remove i then we would have to pop j-1
               cellsToClear.pop(j)
               cellsToClear.pop(i)
               self.delValuesFromListOfCells(cellsToClear,p[i])
               break
      return

   ###############################
   #  EliminatePairs
   #
   # If 2 cells contains the same pair of ossible values, eliminate those values from other cells
   def eliminatePairs(self):
      # Rows, columns, and boxes combined in one loop
      for x in range(0,9):
         p,w = self.getBoxPossibilities(x)
         self.findPairs(p,w)
         p,w = self.getRowPossibilities(x)
         self.findPairs(p,w)
         p,w = self.getColPossibilities(x)
         self.findPairs(p,w)
   ###############################
   #  Cell.printGame
   #
   def printGame(self):
      horizontalLine="+-------------------+-------------------+-------------------+"
      print horizontalLine
      for row in range(9):
         for line in range(4):
            if row%3 == 2 and line == 3 : break
            print '|',
            for col in range(9):
               self.cells[row][col].printCell(line)
               print ' ',
               if col%3 == 2: print '|',
            print
         if row%3 == 2: print horizontalLine
      print 'done'

testGame=[]
level=[]

# testgame[0]: DEMO
level.append('TEST')
testGame.append([
[1,0,0,0,0,0,0,0,8],
[0,2,0,0,0,0,0,9,0],
[0,0,3,0,0,0,6,0,0],
[0,0,0,4,0,7,0,0,0],
[0,0,0,0,5,0,0,0,0],
[0,0,0,3,0,6,0,0,0],
[0,0,4,0,0,0,7,0,0],
[0,1,0,0,0,0,0,8,0],
[2,0,0,0,0,0,0,0,9]])

# testgame[1]: EASY
level.append('EASY')
testGame.append([
[0,0,0,8,0,5,0,1,3],
[0,0,0,2,0,3,6,0,0],
[6,0,0,0,9,0,2,0,4],
[0,0,0,0,0,0,0,0,5],
[0,4,0,1,0,0,7,0,6],
[2,5,6,3,0,4,8,9,0],
[5,9,0,0,0,7,1,0,2],
[1,0,2,0,8,0,4,7,0],
[0,0,4,9,1,0,0,3,8]])

# testgame[2]: MEDIUM
level.append('MEDIUM')
testGame.append([
[0,0,0,4,0,0,2,0,0],
[0,0,2,0,0,0,0,1,8],
[5,0,6,9,0,0,0,3,0],
[0,6,9,0,0,0,3,0,0],
[0,5,0,0,0,0,0,2,1],
[8,0,0,1,5,7,6,0,9],
[0,0,0,0,3,0,9,6,0],
[9,0,0,6,0,2,0,5,0],
[0,0,0,0,0,0,7,0,2]])

# testgame[3]: HARD
level.append('HARD-1')
testGame.append([
[0,0,7,0,0,0,3,0,2],
[2,0,0,0,0,5,0,1,0],
[0,0,0,8,0,1,4,0,0],
[0,1,0,0,9,6,0,0,8],
[7,6,0,0,0,0,0,4,9],
[0,0,0,0,0,0,0,0,0],
[0,0,0,1,0,3,0,0,0],
[8,0,1,0,6,0,0,0,0],
[0,0,0,7,0,0,0,6,3]])

level.append('HARD-2')
testGame.append([
[0,0,4,8,6,0,0,3,0],
[0,0,1,0,0,0,0,9,0],
[8,0,0,0,0,9,0,6,0],
[5,0,0,2,0,6,0,0,1],
[0,2,7,0,0,1,0,0,0],
[0,0,0,0,4,3,0,0,6],
[0,5,0,0,0,0,0,0,0],
[0,0,9,0,0,0,4,0,0],
[0,0,0,4,0,0,0,1,5]])

# testgame[4]: EXPERT
level.append('EXPERT-1')
testGame.append([
[0,0,0,1,9,0,0,0,0],
[0,0,0,0,0,5,0,0,8],
[0,5,0,8,3,0,4,9,6],
[0,0,5,0,0,0,0,6,0],
[0,0,0,4,0,0,1,8,0],
[9,2,0,0,0,1,0,0,0],
[6,0,0,0,0,0,0,3,0],
[0,0,0,2,0,0,6,4,0],
[5,0,0,6,0,3,0,0,0]])

# testgame[0]: DEMO
level.append('EXPERT-2')
testGame.append([
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,1,0,9,8],
[0,0,5,7,0,0,0,3,0],
[0,0,6,0,5,0,8,0,1],
[0,0,0,0,6,0,0,0,0],
[0,7,0,9,0,0,0,0,0],
[0,6,8,0,0,0,4,0,7],
[3,4,0,0,0,0,0,0,0],
[0,9,0,5,0,2,6,0,0]])

def bruteForce(x):
   # Use brute force to finish it all
   # p is the list of possibilities for all unresolved cells
   # w is the list of coordinates for each of these cells
   p,w = x.getPossibilities(0,9,0,9)
   # We will play on a copy of the game called 'y'
   # We keep 'x' to revert to it if our guess ends up being wrong
   y = copy.deepcopy(x)
   while len(p) > 0:
      # Find a cell with the minimum number of possibilities
      nb_poss= 9
      index  = 0
      i      = 0
      for poss in p:
         if len(poss) < nb_poss or len(poss) == 2:
            index   = i
            nb_poss = len(poss)
         i += 1
      # Trying values from cell 'index'
      for possibility in p[index]:
         r,c = w[index]
         logging.debug('*****bruteForce: trying value '+repr(possibility)+' in cell ('+repr(r)+','+repr(c)+')')
         try:
            y.setValue(r,c,possibility)
            rc=1
            while rc>0:
               logging.debug("bruteForce: Finding values that can be only in 1 location")
               rc = y.findLoners()
               logging.debug("bruteForce: found "+repr(rc)+" values")
               if rc>0: y.printGame()
            logging.debug("bruteForce: Eliminate pairs")
            y.eliminatePairs()
            y.eliminatePairs()
            logging.debug("bruteForce: After trying value "+repr(possibility)+" in cell ["+repr(r)+","+repr(c)+"]:")
            y.printGame()
            # Calling bruteForce will result in an exception if the solution is invalid or if 
            # or after all possibilities from this try have been exhausted
            # So, if we return here, we have found a solution and that solution is 'y'
            result,z = bruteForce(y)
            if result == True:
               # We have found a solution, return it to our caller
               return True,z
         except SolutionNotValid:
            logging.debug("bruteForce: After trying value "+repr(possibility)+" in cell ["+repr(r)+","+repr(c)+"], found invalid solution")
         # If we arrive here, our previous guess was wrong.
         # We now need to reset 'y' and try another one
         y = copy.deepcopy(x)
      # If we are here, then none of the possibilities from p[index] was good.
      # Return saying that we failed so another value can be tried
      return False,y
   # Now if we are here, it means that all value have been found.
   # Success, return True with the game 'x'
   return True,x

try:
  os.remove('sudoku.log')
except Exception:
  pass

logging.basicConfig(filename='sudoku.log',level=logging.DEBUG)

n=len(testGame)-1
if len(sys.argv)>1:
   try:
      v=int(sys.argv[1])
   except:
      print "Usage: "+sys.argv[0]+" [game number]"
      sys.exit(0)
   if v>n:
      print "Invalid number: there are only",n,"games"
      sys.exit(0)
   n=v

print "Playing game number ",n,"of level",level[n]
x=Game()

for i in range(9):
   for j in range(9):
      v = testGame[n][i][j]
      if v != 0:
         print v,
      else:
         print '.',
      if j==2 or j==5: print "|",
   print
   if i==2 or i==5: print "------+-------+------"
print

for i in range(9):
   for j in range(9):
      v = testGame[n][i][j]
      if v != 0:
         x.setValue(i,j,v)

x.printGame()

raw_input("Press ENTER")

rc=1
while rc>0:
   print "Finding values that can be only in 1 location"
   rc = x.findLoners()
   print "Found",rc,"values"
   if rc>0: x.printGame()
print "Eliminate pairs"
raw_input("Press ENTER")
x.eliminatePairs()
x.printGame() 
x.eliminatePairs()
x.printGame() 

print "Brute force"
raw_input("Press ENTER")
 
result,y=bruteForce(x)
if result == True:
   print "We have a solution!"
else:
   print "No solution can be found"
y.printGame()

