#!/usr/bin/python
import sys
import random

class MinHeap:
   def __init__(self,maxSize):
      self.maxSize = maxSize
      self.currSize= 0
      # h is the heap
      self.h  = [ 0 for i in range(maxSize+1) ]

   def bubbleUp(self,i):
      # Move a value up the tree to its correct position
      if i==1: return
      p = i/2
      if self.h[p] > self.h[i]:
         self.h[p],self.h[i]=self.h[i],self.h[p]
         self.bubbleUp(p)

   def bubbleDown(self,p):
      i=2*p
      if i > self.currSize: return
      j=i+1
      if j <= self.maxSize and self.h[i] > self.h[j]: i=j
      if self.h[p] > self.h[i]:
         self.h[p],self.h[i] = self.h[i],self.h[p]
         self.bubbleDown(i)

   def insert(self, v):
      # This function adds a node in a min heap
      self.currSize        += 1
      self.h[self.currSize] = v
      self.bubbleUp(self.currSize)

   def replace(self, v):
      # This method replaces the top node by a value and 
      self.h[1]=v
      self.bubbleDown(1)

   def printNodes(self):
      #At 4chars/value, how many chars do we need on the last line?
      global verbose
      myWidth=1
      while myWidth<self.currSize/2: myWidth *= 2
      myWidth  *= 6 # 6 char/value
      newLine= 1
      if verbose: print "Width="+repr(myWidth).rjust(4)+": ",
      for i in range(1,self.currSize+1):
         dashes     = (myWidth/4-1)*u'\u2500'
         valToPrint = repr(self.h[i])
         if dashes != '':
            valToPrint=u'\u256d'+dashes+valToPrint+dashes+u'\u256e'
         print valToPrint.center(myWidth),
         if i==newLine:
            print
            newLine = newLine*2 + 1
            myWidth = (myWidth-1)/2
            if verbose: print "Width="+repr(myWidth).rjust(4)+": ",
      print '\n'

global verbose
verbose=False
if len(sys.argv)>1 and sys.argv[1]=="-h": verbose=True

keep     = input("How many values to keep? ")
maxvalue = 99 #input("What is the largest random int? ")
while keep > 0:
   nval   = input("How many random values to process? ")
   myHeap = MinHeap(keep)
 
   for i in range(nval):
      v = random.randint(0,maxvalue)
      # With the heap structure
      if i < keep:
         myHeap.insert(v)
         if verbose: myHeap.printNodes()
      elif myHeap.h[1] < v:
         myHeap.replace(v)
         if verbose: myHeap.printNodes()

   myHeap.printNodes()
   keep = input("\nHow many values to keep? ")
