#!/usr/bin/python

# City traffic

class Tree:
   def __init__(self):
      self.totalTraffic = 0
   def addNode(self,myId,value,children):
      self.totalTraffic += value
      return self.Node(myId,value,children)
   def maxTraffic(self,node):
      # Initially get the max  traffic from the node's parent
      myMax = self.totalTraffic - node.value - node.sumOfChildren
      # Now find if any of its children have more traffic
      for c in node.children:
         if myMax < c.trafficToParent():
            myMax = c.trafficToParent()
      print 'Max traffic from node id %i is %i'%(node.myId,myMax)
   class Node:
      def __init__(self,myId,value,children):
         self.myId          = myId
         self.value         = value
         self.children      = children
         self.sumOfChildren = 0
         for c in children:
             self.sumOfChildren += c.trafficToParent()
      def trafficToParent(self):
         return self.value + self.sumOfChildren

# Create the nodes starting with all leafs
t = Tree()
n10 = t.addNode(10,10, [])
n9  = t.addNode( 9, 9, [])
n8  = t.addNode( 8, 8, [n9, n10])
n7  = t.addNode( 7, 7, [])
n6  = t.addNode( 6, 6, [n7, n8])
n15 = t.addNode(15,15, [])
n2  = t.addNode( 2, 2, [n15, n6])
n4  = t.addNode( 4, 4, [])
n3  = t.addNode( 3, 3, [])
n1  = t.addNode( 1, 1, [])
n5  = t.addNode( 5, 5, [n1, n2, n3, n4])

# The tree represented here is:
#    
#    /--1  /--15
#    |--2--|     /--7
# 5--|--3  \--6--|     /--9
#    \--4        \--8--|
#                      \--10
nodes = [n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n15]

for n in nodes:
    t.maxTraffic(n)

