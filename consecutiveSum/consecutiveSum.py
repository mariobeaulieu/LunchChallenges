#!/usr/bin/python

# This program takes a list of values as input followed by a value
# and if some conssecutive values in the list equal to the other
# value provided then return TRUE.

def findSequence(myList, mySum):
  for i0 in range(len(myList)):
    total = 0
    for i1 in range(i0, len(myList)):
      total += myList[i1]
      if total == mySum:
         print 'Sequence found:',
         for k in range(i0,i1+1):
            print myList[k],
         return True
  print 'No sequence found in',myList,'that sums to',mySum
  return False

myList = [1,2,3,4,5,6,7,8,9]
mySum  = 22
print findSequence(myList, mySum)

while mySum != 0:
  mySum  = input('Enter the target sum (0 to terminate): ')
  if mySum != 0:
    myList = input('Enter a list of values in the form: [1,2,3,4]: ')
    print findSequence(myList, mySum)
