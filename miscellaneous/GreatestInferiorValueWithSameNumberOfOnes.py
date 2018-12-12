#!/usr/bin/python

import sys

def printBin(v):
  mask=0x8000
  bin='Binary: '
  while mask > 0:
    if (mask & v) == 0:
        bin+='0'
    else:
        bin+='1'
    mask >>= 1
  print bin

try:
  v=int(sys.argv[1])
except:
  print "Usage: ",sys.argv[0]," <integer>"
  print "Ex:  ",sys.argv[0]," 123"
  sys.exit(1)

print "Value is ",v
if v<=0 or v>=0xffff:
  print "The value should be between 0 and ",0xffff
  sys.exit(0)

printBin(v)

nbBits = 0
nbOnes = 0
mask   = 0xffff
# val2 will be the value to replace the whole lsb part
# The initial "1" represents the "1" in the "10" that will be flipped
val2   = 1

# Find first 0 from right
while ( (v>>nbBits) % 2 == 1 ):
  nbBits += 1
  nbOnes += 1
  val2   =  val2 * 2 + 1
  mask   <<= 1
  #print "Found a ONE"

# Now find the first 1 from there
while ( (v>>nbBits) % 2 == 0 ):
  nbBits += 1
  val2   =  val2 * 2
  mask   <<= 1
  if nbBits > 31:
    print "Error: no solution"
    sys.exit(0)
  #print "Found a ZERO"

#We multiplied val2 by 2 once too many times:
val2 /= 2
# We need to expand the mask to cover that "1" we found
mask <<= 1

print "mask and val2:"
printBin(mask)
printBin(val2)

result = ( v & mask ) | val2
print "Result: ",result
printBin(result)

