#!/usr/bin/python
import random
import logging

logging.basicConfig(filename='subgraphs.log',level=logging.DEBUG)

n=input('Enter the number of nodes and edges: ')
while n>0:
  # e is a list of edges
  e=[]
  for i in range(n):
    e.append([i,random.randint(0,n)])

  logging.debug("List of edges: ")
  for i in e:
    logging.debug("[%i,%i] "%(i[0],i[1]))
  print 'There are',n,'nodes and ',len(e),'edges:'
  print e

  # The first graph is composed of the nodes of the first edge
  # g is the list of sets. We start with an empty list
  g=[]
  for i in e:
    print "Processing edge [%i,%i]"%(i[0],i[1])
    found=None # found is the first graph matching an element of i
    join =None # join is when a second graph matches. It means we need to join graphs
    #print "for j in i, where i is ",i
    for j in i:
      logging.debug("Processing element %i"%(j))
      # Each element i of e is a pair of nodes.
      #print "for k in g, where g is ",g
      for k in g:
        #print "k is ",k
        logging.debug("Checking set graph that starts with [%i,%i,...]"%(k[0],k[1]))
        # k is one of the graphs contained in g
        if j in k:
          logging.debug("Found that element %i is in the graph"%(j))
          #If the element j of the edge i is in the graph k
          if found == None:
             found = k
          else:
             # If both ends of edge i point to the same node, don't join
             if found != k:
               logging.debug("Will merge set starting with [%i,%i...] with set starting with [%i,%i...]"%(found[0],found[1],k[0],k[1]))
               join  = k
          # If we found a match, no need to scan through the other graphs
          break
    if found == None:
      # This edge is distinct from all graphs, let's create a new graph
      logging.debug("Edge [%i,%i] is distinct. Create a new set"%(i[0],i[1]))
      # If both elements of i are the same, remove the second one
      if i[0] == i[1]:
        i.remove(i[0])
      g.append(i)
    else:
      # The graph 'found' contains a point from edge i
      if join == None:
        # Add the 2 points from this edge to graph k
        for j in i:
          #print 'Adding node ',j,'to set',found
          if j not in found:
            found.append(j)
      else:
        # This edge connects 2 graphs. Join them
        #print 'Joining sets ',found,'and',join
        found+=join
        g.remove(join)
    print 'There are ',len(g),'distinct sets:'
    for k in g:
      print k
  n=input('Enter the number of nodes and edges: ')

