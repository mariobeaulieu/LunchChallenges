#!/usr/bin/env python
import math
import sys
import mlrose
import numpy as np
from sys import stdin

nb=0
coordsi_list=[]
try:
  for line in stdin:
    if line.strip() != '':
      coordTxt = line.split(' ')
      coords_list.append([int(coordTxt[0]),int(coordTxt[1])])
      nb+=1
except Exception as e:
  print 'Error when reading data stream: e'

if nb==0:
  print 'Usage: %s < infile '%(sys.argv[0])
  sys.exit(1)


# Coordinates of cities to visit
#cities      = [ 'A',  'B',  'C',  'D',  'E',  'F',  'G',  'H' ]
#coords_list = [(1,1),(4,2),(5,2),(6,4),(4,4),(3,6),(1,5),(2,3)]
nb_cities   = nb
use_coords  = True

if use_coords:
  # Initialize fitness function object using coord_list
  fitness_function = mlrose.TravellingSales(coords = coords_list)
else:
  # Create a distance list between pairs of cities
  dist_list   = []
  for i in range(nb_cities):
      for j in range(i+1,nb_cities):
         dist_list.append( (i,j,math.sqrt( (coords_list[i][0]-coords_list[j][0])**2 + (coords_list[i][1]-coords_list[j][1])**2 ) ) )
  # Initialize fitness function object using dist_list
  fitness_function = mlrose.TravellingSales(distances = dist_list)

problem_fit = mlrose.TSPOpt(length=nb_cities, fitness_fn=fitness_function, maximize=False)

# Solve the problem using the genetic algorithm
best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state=2)

print "The best state found is: ",best_state
print "The fitness at the best state is: ",best_fitness

