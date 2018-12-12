#!/usr/bin/python
import sys

verbose = False

def usage():
  print '''
Program to rotate an array by 90 degrees.

The algorithm used is to switch the values of A->B->C->D->A
based on the diagram below:
   0 1 2 3 4 5 6 7 8 9
 0 . . . . . . . . . .
 1 . . A . . . . . . .
 2 . . . . . . . . B .
 3 . . . . . . . . . .
 4 . . . . . . . . . .
 5 . . . . . . . . . .
 6 . . . . . . . . . .
 7 . D . . . . . . . .
 8 . . . . . . . C . .
 9 . . . . . . . . . .

We proceed starting at row 0 from columns 0 to 8,
Then row 1, from columns 1 to 7, etc.
First, A <-> B, then A <-> C, then A <-> D
(It's like if A is the temp variable)
If i is the row, and j is the column:
  (i,j) <-> ( j ,n-i) (where n is 9-1 = 8)
  (i,j) <-> (n-i,n-j)
  (i,j) <-> (n-j, i )

The default is a matrix of 10x10, but if a numerical
parameter is given, verbosity is activated and that
value is used.
'''

usage()
try:
  N = int(sys.argv[1])
  verbose = True
except:
  N = 10

print "Using a matrix of ",N," x ",N

# Image rotation

# Function to print the image
def printImage(M,N):
  for i in range(N):
    for j in range(N):
      print "%4i" % M[i][j],
    print

def rotate(M,N):
  n=N-1
  for i in range(N):
    for j in range(i,N-i-1):
      if verbose:
        print repr(M[i][j]).ljust(4),'(', i ,',', j ,') --> (', j ,',',n-i,')'
      M[i][j],M[ j ][n-i] = M[ j ][n-i],M[i][j]
      if verbose:
        print  repr(M[i][j]).ljust(4),'(', j ,',',n-i,') --> (',n-i,',',n-j,')'
      M[i][j],M[n-i][n-j] = M[n-i][n-j],M[i][j]
      if verbose:
        print repr(M[i][j]).ljust(4),'(',n-i,',',n-j,') --> (',n-j,',', i ,')'
      M[i][j],M[n-j][ i ] = M[n-j][ i ],M[i][j]
      if verbose:
        print repr(M[i][j]).ljust(4),'(',n-j,',', i ,') --> (', i ,',', j ,')'

# Create image:
m=[[0]*N for i in range(N)]
v=0
for i in range(0,N):
  for j in range(0,N):
    m[i][j] = v
    v += 1

printImage(m,N)

print "Rotating image..."
rotate(m,N)
print "Image now rotated:"
printImage(m,N)

print "Image rotated again (180 deg)"
verbose = False
rotate(m,N)
printImage(m,N)

print "And rotated twice again to return to original state:"
rotate(m,N)
rotate(m,N)
printImage(m,N)

