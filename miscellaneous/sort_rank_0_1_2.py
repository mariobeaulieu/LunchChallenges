#!/usr/bin/python

import random
import sys

verbose=False
if len(sys.argv)>1:
  verbose = True

def getArray():
  r=input("\n====================\nEnter how many values or the list of values separated by commas : ")
  if type(r) == type(0):
    num = int(r)
    array=[random.randrange(0,3) for _ in range(num)]
  else:
    array=list(r)
    num=len(array)
  return num,array

num,array = getArray()
while num > 0:

  print "Original array: ", array

  p0=0
  p2=num-1
  pr=0

  # We will loop until we hit the pointer p2
  while pr<=p2:
    switch=False
    if array[pr]==0:
      if pr>p0:
        array[pr],array[p0] = array[p0],array[pr]
        if verbose:
          print "Read pointer is ",repr(pr).ljust(2)," Swap ",repr(pr).ljust(2)," <-> ",repr(p0).ljust(2)," New array: ",array
        p0+=1
        switch=True
    elif array[pr]==2:
        array[pr],array[p2] = array[p2],array[pr]
        if verbose:
          print "Read pointer is ",repr(pr).ljust(2)," Swap ",repr(pr).ljust(2)," <-> ",repr(p2).ljust(2)," New array: ",array
        p2-=1
        switch=True
    if not switch:
      pr+=1

  print "Sorted   array: ", array

  num,array = getArray()
