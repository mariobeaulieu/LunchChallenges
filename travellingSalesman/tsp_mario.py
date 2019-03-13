#!/usr/bin/env python
import random
import math
import sys

# Coordinates of cities to visit
cities    = [ 'A',  'B',  'C',  'D',  'E',  'F',  'G',  'H' ]
coords    = [[1,1],[4,2],[5,2],[6,4],[4,4],[3,6],[1,5],[2,3]]
minDist   = 1000
minPath   = []
nb        = len(cities)

distances = {}
for i in range(nb):
    for j in range(i+1,nb):
       distances[cities[i]+cities[j]] = math.sqrt( (coords[i][0]-coords[j][0])**2 + (coords[i][1]-coords[j][1])**2 )

numIterations = 10
if sys.argv > 1:
  try:
     numIterations = int(sys.argv[1])
     if numIterations<1:
        numIterations = 10
  except:
     pass

print 'We will consider',numIterations,'iterations'

for iteration in range(numIterations):
  dist=0
  currPath=[]
  #Cities already visited
  used=[False for i in range(nb)]
  # We start and end with city 'A'
  city=0
  currPath.append(cities[city])
  used[0]=True
  # range isnb-2 because we start with a fixed city
  for n in range(1,nb):
    j=random.randint(1,nb-n)
    while used[j]:
      j=(j+1)%nb
    used[j]=True
    currPath.append(cities[j])
    route = sorted([cities[city],cities[j]])
    dist += distances[route[0]+route[1]]
    city=j
  # Then we link back to start city
  currPath.append(cities[0])
  route = sorted([cities[city],cities[0]])
  dist += distances[route[0]+route[1]]
  if dist < minDist:
    minPath = currPath
    minDist=dist
print 'Best path found is ',minPath
print 'Distance is ',minDist
