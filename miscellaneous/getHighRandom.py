#!/usr/bin/python
import sys
import random

usage='''
This program requests a large list of integers and will keep the N largest ones.

Usage:  getHighRandom.py [-h]

'''

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
      newLine=1
      for i in range(1,self.currSize+1):
         print "{0:4d}-".format(self.h[i]),
         if i==newLine:
            print
            newLine = newLine*2 + 1
      print

class Node:
   def __init__(self, suiv, value):
      self.suiv = suiv
      self.value= value

class LinkedListOfBigValues:
   def __init__(self,length):
      self.length = length
      self.firstNode = None
      self.numNodes  = 0
   def addNode(self, prev, node, val):
      # Find between which nodes the new value ought to be
      if node.value >= val:
         if prev == None:
            # This is the new first node and its next is the current firstNode
            self.firstNode = Node(self.firstNode, val)
            self.numNodes  += 1
         else:
            # The new node is inserted between this node and prev
            prev.suiv = Node(node, val)
            self.numNodes  += 1
      elif node.suiv == None:
         # The node is added at the end of the list
         node.suiv       = Node(None, val)
         self.numNodes  += 1
      elif node.value < val:
         # Go further down the list
         self.addNode(node, node.suiv, val)
   def moveNode(self, prev, node, val):
      # Find between which nodes the new value ought to be
      if node.value >= val:
         # The node must be moved between this node and the previous one
         self.firstNode.value = val
         # If we are replacing the first node, nothing else to do
         if prev != self.firstNode:
            newFirstNode         = self.firstNode.suiv
            self.firstNode.suiv  = node
            prev.suiv            = self.firstNode
            self.firstNode       = newFirstNode
      elif node.suiv == None:
         # The node is added at the end of the list
         self.firstNode.value = val
         newFirstNode         = self.firstNode.suiv
         node.suiv            = self.firstNode
         self.firstNode.suiv  = None
         self.firstNode       = newFirstNode
      elif node.value < val:
         # Go further down the list
         self.moveNode(node, node.suiv, val)
   def insert(self,v):
      if self.firstNode == None:
         self.firstNode = Node(None, v)
      else:
         if self.numNodes < self.length-1:
            self.addNode(None, self.firstNode, v)
         elif v>self.firstNode.value:
            self.moveNode(None, self.firstNode, v)
   def printNodes(self):
      n=self.firstNode
      while n != None:
         print "{0:d}-".format(n.value),
         n=n.suiv
      print

if len(sys.argv) > 1:
   if sys.argv[1] == '-h': print usage; sys.exit(0)

keep     = input("How many values to keep? ")
maxvalue = input("What is the largest random int? ")
while keep > 0:
   nval   = input("How many random values to process? ")
   myList = LinkedListOfBigValues(keep)
   myHeap = MinHeap(keep)
 
   for i in range(nval):
      v = random.randint(0,maxvalue)
      #print "({0:d})".format(v),
      if i < keep or myList.firstNode.value < v:
         myList.insert(v)
         #print
         #myList.printNodes()
      # With the heap structure
      if i < keep:
         myHeap.insert(v)
         #myHeap.printNodes()
      elif myHeap.h[1] < v:
         myHeap.replace(v)
         #myHeap.printNodes()

   myList.printNodes()
   myHeap.printNodes()
   keep = input("\nHow many values to keep? ")
