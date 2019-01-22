#/usr/bin/python
import random

n=raw_input('Enter the number of nodes and edges: ')
while n>0:
  # e is the set of edges
  e=()
  for i in range(n):
    e.add([i,random.randint(0,n)])

  print 'There are',n,'nodes and ',len(e),'edges:'
  print e

  # The first graph is composed of the nodes of the first edge
  # g is the list of sets. We start with an empty list
  g=[]
  for i in e:
    found=None # found is the first graph matching an element of i
    join =None # join is when a second graph matches. It means we need to join graphs
    for j in i:
      # Each element i of e is a pair of nodes.
      for k in g:
        # k is one of the graphs contained in g
        if j in k:
          #If the element j of the edge i is in the graph k
          if found == None:
             found = k
          else:
             join  = k
          # If we found a match, no need to scan through the other graphs
          break
    if found == None:
      # This edge is distinct from all graphs, let's create a new graph
      g+=set(i)
    else
      # The graph 'found' contains a point from edge i
      if join == None:
        # Add the 2 points from this edge to graph k
        for j in i:
          found.add(j)
      else:
        # This edge connects 2 graphs. Join them
        found.union(join)
        g.remove(join)
  print 'There are ',len(g),'distinct sets:'
  for k in g:
    print k

