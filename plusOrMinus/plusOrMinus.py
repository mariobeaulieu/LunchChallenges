#!/usr/bin/python

# Function to insert '+' or '-' between numbers and 
# return TRUE if it's possible to yield a given value.
# Ex:
# 2, [1,2,3,4] 
# would return TRUE
# because 1+2+3-4 = 2
#
def plusOrMinus(value, numbers):
  # To go through all combinations of '+' and '-',
  # we can proceed using binary values where a
  # '0' would be a '+' and a '1' would be a '-'
  numOperations = len(numbers)-1
  # We can start with a value of all binary '0' and
  # decrement until we reach all ones
  for ops in range(2**numOperations):
     mySum   = numbers[0]
     op      = ops
     myString= repr(mySum)
     for i in range(numOperations):
        if op%2 == 0:
           mySum += numbers[i+1]
           myString += '+'
        else:
           mySum -= numbers[i+1]
           myString += '-'
        myString += repr(numbers[i+1])
        op /= 2
     if mySum == value:
        print 'Found a solution: ',myString
        return True
  print 'No solution found'
  return False

print 'Enter the target value followed by a list of numbers in'
print 'a format similar to this: 2,[1,2,3,4]'
print 'There can be any number of numbers in the list.'
print 'A target value < 0 means exit'
v=0
while v>=0:
   v,n = input('Enter value and list of numbers: ')
   if v>=0:
      plusOrMinus(v,n)
         
