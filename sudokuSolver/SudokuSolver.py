#!/usr/bin/python

# Sudoku Solver

import logging
import sys
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
      self.delValuesFromBox(row,col,[value])
      self.delValuesFromRow (row,col,[value])
      self.delValuesFromCol (row,col,[value])
   def delValuesFromBox(self,row,col,values):
      logging.info('Game: delValuesFromBox('+repr(row)+','+repr(col)+')')
      # Delete a value from all cells of that box
      # except for the cell at [row,col]
      # Cell at (row,col): what is the cell in the top left corner of that box?
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
                  raise SolutionNotValid(str(problem)+" in block ["+repr(row)+"]["+repr(col)+"]")
               # If deleting that value results in a single possibility for that cell, we just found a value
               # We need to eliminate that value from all other cells in this box, row, and column
               if foundValue:
                  v=self.cells[i][j].getValues()
                  self.setValue(i,j,v[0])
#
#  Cell.findLoners
#     This function finds if a value appears only once in the list of possibilities for a row, col, or box
#
   def findLoners(self):
      nbChanges=0
      # See if a number can be in a single cell for 1 row
      for row in range(9):
         # Find the list of unknown digits on that row
         unknowns=[1,2,3,4,5,6,7,8,9]
         for col in range(9):
            v=self.cells[row][col].getValues()
            if len(v) == 1:
               unknowns.remove(v[0])
         logging.debug('Game.findLoners: On row '+repr(row)+': list of possibilities is: '+repr(unknowns))
         for v in unknowns:
            n=0
            c=[]
            for col in range(9):
               if v in self.cells[row][col].getValues():
                  n += 1
                  c.append(col)
            if n == 1:
               # The value can be onlyin column c of that row
               self.setValue(row,c[0],v)
               nbChanges += 1
            elif n<=3:
               allInSameBox=True
               c1=(c[0]/3)*3
               for i in range(1,len(c)):
                  if (c[i]/3)*3 != c1 : allInSameBox = False
               if allInSameBox:
                  logging.info('Game.findLoners: removing '+repr(v)+' from possibilities for other rows in box of cell ('+repr(row)+','+repr(c[0])+')')
                  # All possibilities of "v" are in the same box. We can remove "v" from all other cels of that box
                  r1=(row/3)*3
                  # r1,c1 is the coordinate of the top left cell of that box
                  for rr in range(r1,r1+3):
                     if rr == row: continue
                     self.delValues(row,c[0],rr,rr+1,c1,c1+3,[v])
                        
      # See if a number can be in a single cell for 1 column
      for col in range(9):
         # Find the list of unknown digits on that column
         unknowns=[1,2,3,4,5,6,7,8,9]
         for row in range(9):
            v=self.cells[row][col].getValues()
            if len(v) == 1:
               unknowns.remove(v[0])
         for v in unknowns:
            n=0
            r=[]
            for row in range(9):
               if v in self.cells[row][col].getValues():
                  n += 1
                  r.append(row)
            if n == 1:
               # The value can be only in row r of that column
               self.setValue(r[0],col,v)
               nbChanges += 1
            elif n<=3:
               allInSameBox=True
               r1=(r[0]/3)*3
               for i in range(1,len(r)):
                  if (r[i]/3)*3 != r1 : allInSameBox = False
               if allInSameBox:
                  logging.info('Game.findLoners: removing '+repr(v)+' from possibilities for other cols in box of cell ('+repr(r[0])+','+repr(col)+')')
                  # All possibilities of "v" are in the same box. We can remove "v" from all other cels of that box
                  c1=(col/3)*3
                  # r1,c1 is the coordinate of the top left cell of that box
                  for cc in range(c1,c1+3):
                     if cc == col: continue
                     self.delValues(r[0],col,r1,r1+3,cc,c1+1,[v])
      # See if a number can be in a single cell for 1 column
      for rr in range(0,9,3):
         for cc in range(0,9,3):
            # Find the list of unknown digits on that box
            unknowns=[1,2,3,4,5,6,7,8,9]
            for row in range(rr,rr+3):
               for col in range(cc,cc+3):
                  v=self.cells[row][col].getValues()
                  if len(v) == 1:
                     unknowns.remove(v[0])
            n=0
            for v in unknowns:
               for row in range(rr,rr+3):
                  for col in range(cc,cc+3):
                     if v in self.cells[row][col].getValues():
                        n += 1
                        r = row
                        c = col
               if n == 1:
                  # The value can be onlyin row r column c of that box
                  self.setValue(r,c,v)
                  nbChanges += 1
      return nbChanges
#
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

# testgame[0]: DEMO
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

# testgame[1]: EASY
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

# testgame[4]: EXPERT
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

rc=1
while rc>0:
  print "Finding values that can be only in 1 location"
  rc = x.findLoners()
  print "Found",rc,"values"
  if rc>0: x.printGame()

