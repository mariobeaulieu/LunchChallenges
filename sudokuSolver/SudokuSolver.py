#!/usr/bin/python

# Sudoku Solver

class SolutionNotValid(Exception):
   def __init__(self,mismatch):
      Exception.__init__(self,mismatch)

class Cell:
   def __init__(self,row,col):
      self.row   = row
      self.col   = col
      self.values= [1,2,3,4,5,6,7,8,9]
   def setValue(self,v):
      self.values= [v]
   def getValues(self):
      return self.values
   def delValues(self,valuesToRemove):
      for v in valuesToRemove:
         if v in self.values:
            self.values.remove(v)
            if len(self.values) == 0:
               raise SolutionNotValid("Solution not valid when deleting "+repr(v)+" at ["+repr(self.row)+"]["+repr(self.col)+"]")
            # Return True if the number of possible values of this cell is now 1
            return (len(self.values) == 1)
      return False
   def printCell(self,line):
      # Each cell is 3 line high (lines 0,1,2) to display all its possibilities
      s=repr(line)
      for i in range(3*line+1,3*line+4):
         if i in self.values:
            s+=repr(i)
         else:
            s+=' '
      print s,
      
class Cube:
   def __init__(self,row,col):
      self.row   = row
      self.col   = col
      self.cells = [[Cell(i,j) for i in range(3)] for j in range(3)]
   def setValue(self,row,col,values):
      self.cells[row][col].setValue(values)
   def delValuesFromCube(self,row,col,values):
      # Delete a value from all cells of that cube
      # except for the cell at [row,col]
      return self.delValues(row,col,0,3,0,3,values)
   def delValuesFromRow(self,row,col,values):
      return self.delValues(row,col,row,row+1,0,3,values)
   def delValuesFromCol(self,row,col,values):
      return self.delValues(row,col,0,3,col,col+1,values)
   def delValues(self,row,col,i0,i1,j0,j1,values):
      # This method deletes values from cells in rows i0 to i1 and columns j0 to j1 except for cell row,col
      # foundValues is an array with coordinates of cells where after removing "values" only 1 value is now possible
      foundValues=[]
      for i in range(i0,i1):
         for j in range(j0,j1):
            if i != row and j != col:
               try:
                  foundValue = self.cells[i][j].delValues(values)
               except SolutionNotValid as problem:
                  raise SolutionNotValid(problem+" in block ["+repr(self.row)+"]["+repr(self.col)+"]")
               # If deleting that value results in a single possibility for that cell, we just found a value
               # We need to eliminate that value from all other cells in this cube, row, and column
               if foundValue:
                  foundValues.append([i,j])
      return foundValues
   def printCube(self,row,line):
      for col in range(3):
         #self.cells[row][col].printCell(line)
         print "Printing cube[",self.row,",",self.col,"] cell [",row,",",col,"] line",line

class Game:
   def __init__(self):
      self.cubes=[[Cube(i,j) for i in range(3)] for j in range(3)]
   def printGame(self):
      for row in range(3):
         for cubeRow in range(3):
            for line in range(3):
               for col in range(3):
                  self.cubes[row][col].printCube(cubeRow,line)
                  print 'x',
               print "c",
            print 'l'
         print 'cr'
      print 'r'

x=Game()
x.printGame()

