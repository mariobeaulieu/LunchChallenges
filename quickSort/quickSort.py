#!/usr/bin/python
import random
import sys
global c

def quickSort(alist):
   quickSortHelper(alist,0,len(alist)-1)

def quickSortHelper(alist,first,last):
   global c
   c+=1
   print "c=",repr(c).ljust(2),"first:",first,"last=",last,"v=",alist
   if first<last:
       splitpoint = partition(alist,first,last)
       quickSortHelper(alist,first,splitpoint-1)
       quickSortHelper(alist,splitpoint+1,last)

def partition(alist,first,last):
   pivotvalue = alist[first]
   leftmark = first+1
   rightmark = last
   done = False
   while not done:
       while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
           leftmark = leftmark + 1
       while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
           rightmark = rightmark -1
       if rightmark < leftmark:
           done = True
       else:
           alist[leftmark],alist[rightmark] = alist[rightmark],alist[leftmark]
   alist[first],alist[rightmark] = alist[rightmark],alist[first]
   return rightmark

def bubbleSort(alist):
   for i in range(len(alist)-1,0,-1):
      for j in range(i):
         if alist[j] > alist[j+1]:
            #print 'Switching values {} and {}'.format(alist[j],alist[j+1])
            alist[j],alist[j+1] = alist[j+1],alist[j]

def doIt(alist):
   blist = list(alist)
   print "Original list:",alist
   quickSort(alist)
   print "Sorted  list :",alist
   #bubbleSort(blist)
   #print "Bubble  sort :",blist

c=0
if len(sys.argv)>2:
   alist = [ int(sys.argv[i]) for i in range(1,len(sys.argv))]
   doIt(alist)
else:
   maxValue=1000
   n = input ("How many random values to use? ")
   while n>0:
      alist = [random.randint(8,maxValue) for i in range(0,n)]
      doIt(alist)
      n = input ("How many random values to use? ")

