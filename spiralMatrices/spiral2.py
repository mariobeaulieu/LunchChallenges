#!/usr/bin/python

# Create a square matrix of side X where
# elements are disposed in a spiral
# Values to be put in the matrix are 
# numbers from 0 to XxX-1

# This version only prints array indexes

n = input ("Enter the size of the square matrix (ex: 4 for a 4x4): ")
while n>0:
   n1=n-1
   v=0
   for offset in range(n/2):
      for i in range(offset,n1-offset): print "[",i,",",offset,"]",                                                                                 
      print
      for i in range(offset,n1-offset): print '[',n1-offset,',',i,']',                                                                              
      print
      for i in range(offset,n1-offset): print '[',n1-i,',',n1-offset,']',                                                                           
      print
      for i in range(offset,n1-offset): print '[',offset,',',n1-i,']',
      print
   # In the case of odd-valued size matrix, we need to add the middle element
   if n%2 == 1: print '[',n/2,',',n/2,']'
   n = input ("Enter the size of the square matrix (ex: 4 for a 4x4): ")

