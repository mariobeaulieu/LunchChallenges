#!/usr/bin/python

def subsets(s):
  if len(s) > 1:
    s2 = subsets(s[1:])
    ss = s2 + [s[0] + j for j in s2]
  else:
    ss = ['', s[0]]
  return ss

n=input("\nHow many entries in the set? ")
while n>0:
  mySet=[str(i) for i in range(n)]
  print "Set:    ",mySet
  print "Subsets:",sorted(subsets(mySet))
  n=input("\nHow many entries in the set? ")
