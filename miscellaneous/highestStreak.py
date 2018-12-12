#!/usr/bin/python
import random
import sys

def printVector(text,v):
  print text,
  for i in range(len(v)):
    print repr(v[i]).ljust(5),
  print

verbose = False
if len(sys.argv)>1:
  verbose = True

# This program selects the first and last index to use to get the streak that will return the highest value

arrayLength=int(input("\nEnter the length of the input array (0 to terminate):"))

while arrayLength > 0:
  minV=int(input("Enter minimum random value: "))
  maxV=int(input("Enter maximum random value: "))
  v=[random.randrange(minV,maxV) for _ in range(arrayLength)]
  printVector("Vector: ",v)
  printVector("Index : ",range(len(v)))

  currMax=0
  indexMin=0
  indexMax=0
  bestMax = 0
  indexBestMin=0
  indexBestMax=0
  currSum=0
  vectCurrSum=[]
  for i in range(arrayLength):
    currSum += v[i]
    if currSum < 0:
      #Reset current values
      currSum = 0
      indexMin=i+1
      indexMax=i+1
      currMax=0
    elif currSum > currMax:
      # This is the new max for this streak
      indexMax = i
      currMax  = currSum
      # And is it the best ever?
      if currSum > bestMax:
        indexBestMin=indexMin
        indexBestMax=indexMax
        bestMax = currSum
    #vectCurrSum is there just to present the results
    vectCurrSum.append(currSum)
  # Present results
  printVector("Sum...: ",vectCurrSum)
  print "The best streak has a value of ",bestMax
  print "It starts at index ",indexBestMin," and ends at index ",indexBestMax

  arrayLength=int(input("\nEnter the length of the input array (0 to terminate):"))

