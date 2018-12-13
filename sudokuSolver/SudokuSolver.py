#!/usr/bin/python

# Sudoku Solver
from colors import red,green,blue
import logging
import sys

class SolutionNotValid(Exception):
   def __init__(self,mismatch):
      Exception.__init__(self,mismatch)

class Cell:
   def __init__(self,row,col):
      self.row   = row
      self.col   = col
      self.values= [1,2,3,4,5,6,7,8,9]
   def setValue(self,v):
      logging.debug('Cell: setting ('+repr(self.row)+','+repr(self.col)+') to '+repr(v))
      self.values= [v]
   def getValues(self):
      return self.values
   def delValues(self,valuesToRemove):
      for v in valuesToRemove:
         if v in self.values:
            logging.debug('Cell: removing value '+repr(v)+'from cell ('+repr(self.row)+','+repr(self.col)+')')
            self.values.remove(v)
            if len(self.values) == 0:
               raise SolutionNotValid("Solution not valid when deleting "+repr(v)+" at ["+repr(self.row)+"]["+repr(self.col)+"]")
            # Return True if the number of possible values of this cell is now 1
            return (len(self.values) == 1)
      return False
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
   def setValue(self,row,col,value):
      self.cells[row][col].setValue(value)
      self.delValuesFromCube(row,col,[value])
      self.delValuesFromRow (row,col,[value])
      self.delValuesFromCol (row,col,[value])
   def delValuesFromCube(self,row,col,values):
      logging.info('Game: delValuesFromCube('+repr(row)+','+repr(col)+')')
      # Delete a value from all cells of that cube
      # except for the cell at [row,col]
      # Cell at (row,col): what is the cell in the top left corner of that cube?
      cr = (row/3) * 3
      cc = (col/3) * 3
      return self.delValues(row,col,cr,cr+3,cc,cc+3,values)
   def delValuesFromRow(self,row,col,values):
      logging.info('Game: delValuesFromRow('+repr(row)+','+repr(col)+')')
      return self.delValues(row,col,row,row+1,0,9,values)
   def delValuesFromCol(self,row,col,values):
      logging.info('Game: delValuesFromCol('+repr(row)+','+repr(col)+')')
      return self.delValues(row,col,0,9,col,col+1,values)
   def delValues(self,row,col,i0,i1,j0,j1,values):
      logging.info('Game: delValues('+repr(row)+','+repr(col)+') for rows '+repr(i0)+' to '+repr(i1)+' and cols '+repr(j0)+' to '+repr(j1))
      # This method deletes values from cells in rows i0 to i1 and columns j0 to j1 except for cell row,col
      # foundValues is an array with coordinates of cells where after removing "values" only 1 value is now possible
      for i in range(i0,i1):
         for j in range(j0,j1):
            if not (i == row and j == col):
               try:
                  foundValue = self.cells[i][j].delValues(values)
               except SolutionNotValid as problem:
                  raise SolutionNotValid(problem+" in block ["+repr(self.row)+"]["+repr(self.col)+"]")
               # If deleting that value results in a single possibility for that cell, we just found a value
               # We need to eliminate that value from all other cells in this cube, row, and column
               if foundValue:
                  v=self.cells[i][j].getValues()
                  self.setValue(i,j,v[0])
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

# testgame[0]
testGame.append([
[4,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0]])

# testgame[1]
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

# testgame[2]
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

# testgame[3]
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
print "Playing game number ",n

x=Game()
for i in range(9):
   for j in range(9):
      v = testGame[n][i][j]
      if v != 0:
         x.setValue(i,j,v)

x.printGame()

