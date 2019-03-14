#!/usr/bin/env python
import random
import math
import sys
from sys import stdin

RNDMAX=10000 # Max range for city coordinate
nb=0
coords=[]
print 'If program is stuck here, press ^D'
try:
  for line in stdin:
    if line.strip() != '':
      coordTxt = line.split(' ')
      coords.append([int(coordTxt[0]),int(coordTxt[1])])
      nb+=1
    else:
      break
except Exception as e:
  print 'Error when reading data stream: e'
  sys.exit(1)

if nb==0:
  print 'Usage: %s < infile '%(sys.argv[0])
  print 'The default dataset will be used'
  # Coordinates of cities to visit
  coords    = [[1,1],[4,2],[5,2],[6,4],[4,4],[3,6],[1,5],[2,3]]
  nb = len(coords)

print '\n',nb,'values are in the set\n'

cities    = [i for i in range(nb)]
attempts  = max(int(nb/10),3) # Number of attempts for each section

minDist   = RNDMAX*nb
minPath   = []

distances = {}
for i in range(nb):
    for j in range(i+1,nb):
       distances[cities[i]*RNDMAX+cities[j]] = math.sqrt( (coords[i][0]-coords[j][0])**2 + (coords[i][1]-coords[j][1])**2 )

numIterations = 100
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
  # range is nb-1 because we start with a fixed city
  for n in range(1,nb):
    bestDist=RNDMAX**2
    bestj   =0
    for attempt in range(attempts):
      j=random.randint(1,nb-1)
      while used[j]:
        j=(j+1)%nb
      route = sorted([cities[city],cities[j]])
      d     = distances[route[0]*RNDMAX+route[1]]
      if d<bestDist:
        bestDist=d
        bestj   =j
    used[bestj]=True
    currPath.append(cities[bestj])
    dist += d
    city=bestj
  # Then we link back to start city
  currPath.append(cities[0])
  route = sorted([cities[city],cities[0]])
  dist += distances[route[0]*RNDMAX+route[1]]
  if dist < minDist:
    minPath = currPath
    minDist=dist
print 'Best path found is ',minPath
print 'Distance is ',minDist
