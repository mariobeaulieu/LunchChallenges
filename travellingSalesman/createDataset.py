#!/usr/bin/env python
import random
import sys

# Coordinates of cities to visit
coords    = []

numItems = 100
if sys.argv > 1:
  try:
     numItems = int(sys.argv[1])
     if numItems<1:
        numItems = 100
  except:
     pass

# City coordinates will be chosen randomly
