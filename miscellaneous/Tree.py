#!/usr/bin/python
import sys

class Tree:
  __verbosity=False
  __nbNodes = 0
  # Values for distance
  __minDist = 1000
  __maxDist = 0

  def __init__(self, v):
    self.value = v
    self.right = None
    self.left  = None
    Tree.__nbNodes += 1

  def toggleVerbose(self):
    Tree.__verbosity=not Tree.__verbosity

  def getVerbose(self):
    return Tree.__verbosity

  def getNumNodes(self):
    return Tree.__nbNodes

  def insert(self, v):
    if v < self.value:
      if self.left is None:
        self.left = Tree(v)
      else:
        self.left.insert(v)
    elif v > self.value:
      if self.right is None:
        self.right = Tree(v)
      else:
        self.right.insert(v)
    else:
      print "Duplicate entry ignored: ",v

  def printTree(self, depth):
    if self.left is not None:
      self.left.printTree(depth+1)
    print self.value," (depth = ", depth, ")"
    if self.right is not None:
      self.right.printTree(depth+1)

  def setMinDist(self,v):
    Tree.minDist = v
  def setMaxDist(self,v):
    Tree.maxDist = v
  def getMinDist(self):
    return Tree.minDist
  def getMaxDist(self):
    return Tree.maxDist

  def updateDist(self, v):
    if v < self.getMinDist():
      self.setMinDist(v)
      if self.getVerbose():
        print "minDist updated to ",v
    if v > self.getMaxDist():
      self.setMaxDist(v)
      if self.getVerbose():
        print "maxDist updated to ",v

  def balance(self, d):
    if d == 0:
      # Reset distances
      if self.getVerbose():
        print "Distances reset to 1000 and 0"
      self.setMinDist(1000)
      self.setMaxDist(0)

    if self.left is None or self.right is None:
      self.updateDist(d)
    if self.left is not None:
      self.left.balance(d+1)
    if self.right is not None:
      self.right.balance(d+1)

  def getMinDist(self):
    return Tree.minDist
  def getMaxDist(self):
    return Tree.maxDist
  def setMinDist(self,v):
    Tree.minDist=v
  def setMaxDist(self,v):
    Tree.maxDist=v

verbose=0
if len(sys.argv) > 1:
  if sys.argv[1] == '-v':
    print "Verbose ON"
    verbose=1
  else:
    print "Invalid option: ",sys.argv[1]
    print "The only valid option is -v"

v = raw_input("Enter value of root node: ")
myTree = Tree(int(v))
if verbose == 1:
  myTree.toggleVerbose()

while True:
  v = raw_input("Enter node value (x to exit, p to print tree, b to check balancing): ")
  if v == 'x':
    sys.exit(0)
  elif v == 'b':
    myTree.balance(0)
    print "Min distance from leaf to root is ",myTree.getMinDist()
    print "Max distance from leaf to root is ",myTree.getMaxDist()
    print
  elif v == 'p':
    print "\nThere are ",myTree.getNumNodes," entries in the tree"
    myTree.printTree(0)
    print
  elif unicode(v,'utf-8').isnumeric():
    myTree.insert(int(v))
  elif v == 'v':
    print "\nVerbose is ",myTree.getVerbose()
    myTree.toggleVerbose()
    print "Verbose is now ",myTree.getVerbose()
  else:
    print "Invalid entry ignored: ",v
