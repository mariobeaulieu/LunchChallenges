#!/usr/bin/env python
import math
import sys
import mlrose
import numpy as np
from sys import stdin
print 'If program is stuck here, press ^D'

nb=0
coords_list=[]
try:
  for line in stdin:
    if line.strip() != '':
      coordTxt = line.split(' ')
      coords_list.append([int(coordTxt[0]),int(coordTxt[1])])
      nb+=1
    else:
      break
except Exception as e:
  print 'Error when reading data stream: e'
  sys.exit(1)

if nb==0:
  print 'Usage: %s < infile '%(sys.argv[0])
  print '\nThe default dataset will be used'
  # Coordinates of cities to visit
  coords_list = [[1,1],[4,2],[5,2],[6,4],[4,4],[3,6],[1,5],[2,3]]
  nb = len(coords_list)

print '\n',nb,'values are in the set\n'


# Coordinates of cities to visit
#cities      = [ 'A',  'B',  'C',  'D',  'E',  'F',  'G',  'H' ]
#coords_list = [(1,1),(4,2),(5,2),(6,4),(4,4),(3,6),(1,5),(2,3)]
nb_cities   = nb
use_coords = len(sys.argv)>1
if use_coords:
  print 'An argument was provided, so coordinates (not distances) will be used'
  # Initialize fitness function object using coord_list
  fitness_function = mlrose.TravellingSales(coords = coords_list)
else:
  print 'No argument was provided, so distances (not coordinates) will be used'
  # Create a distance list between pairs of cities
  dist_list   = []
  for i in range(nb_cities):
      for j in range(i+1,nb_cities):
         dist_list.append( (i,j,math.sqrt( (coords_list[i][0]-coords_list[j][0])**2 + (coords_list[i][1]-coords_list[j][1])**2 ) ) )
  # Initialize fitness function object using dist_list
  fitness_function = mlrose.TravellingSales(distances = dist_list)

problem_fit = mlrose.TSPOpt(length=nb_cities, fitness_fn=fitness_function, maximize=True)

# Solve the problem using the genetic algorithm
best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state=2)

print "The best state found is: ",best_state
print "The fitness at the best state is: ",best_fitness

