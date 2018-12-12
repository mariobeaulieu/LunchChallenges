#!/usr/bin/python

# Create a square matrix of side X where
# elements are disposed in a spiral
# Values to be put in the matrix are 
# numbers from 0 to XxX-1

verbose=False
def printMatrix():
   for i in range(n):
      for j in range(n):
         print repr(x[j][i]).rjust(3),
      print
   print

n = input ("Enter the size of the square matrix (ex: 4 for a 4x4): ")
while n>0:
   n1=n-1
   x=[[0 for i in range(n)] for j in range(n)]
   if verbose: printMatrix()
   v=0
   for offset in range(n/2):
      # Top row
      for i in range(offset,n1-offset):
         if verbose: print "Top row:      offset=",offset,"i=",i,"(i,j)=(",i,",",offset,") v=",v
         x[i][offset]=v
         v+=1
      # Right column
      for i in range(offset,n1-offset):
         if verbose: print "Right column: offset=",offset,"i=",i,"(i,j)=(",n1-offset,",",i,") v=",v
         x[n1-offset][i]=v
         v+=1
      # Bottom row
      for i in range(offset,n1-offset):
         if verbose: print "Bottom row:   offset=",offset,"i=",i,"(i,j)=(",n1-i,",",n1-offset,") v=",v
         x[n1-i][n1-offset]=v
         v+=1
      # Left column
      for i in range(offset,n1-offset):
         if verbose: print "Left  column: offset=",offset,"i=",i,"(i,j)=(",offset,",",n1-i,") v=",v
         x[offset][n1-i]=v
         v+=1
   # In the case of odd-valued size matrix, we need to add the middle element
   if n%2 == 1:
      x[n/2][n/2]=v
      if verbose: print "Middle element: (i,j)=(",n/2,n/2,") v=",v

   printMatrix()
   n = input ("Enter the size of the square matrix (ex: 4 for a 4x4): ")

