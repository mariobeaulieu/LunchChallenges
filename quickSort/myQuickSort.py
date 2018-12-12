#!/usr/bin/python
import random
import sys
global c

def quicksort(v,d,f):
  global c
  c+=1
  print "c=",repr(c).ljust(2),"debut:",d," Fin=",f,"v=",v
  if d>=f : return
  p=v[d]
  j=f
  i=d+1
  if i==j:
    if v[j]<p:
      v[d],v[j] = v[j],v[d]
  else:
    while i<j:
      while v[i]<=p and i<j:
        i+=1
      while v[j]>p:
        j-=1
      if i<j:
        v[i],v[j] = v[j],v[i]
    if j>d:
      v[d],v[j] = v[j],v[d]
  quicksort(v,d,j-1)
  quicksort(v,i,f)

num=len(sys.argv)
if num < 2:
  print "Usage: quicksort <numberOfRandomValues>"
  sys.exit(0)
if num == 2:
  n=int(sys.argv[1])
  v=[random.randint(0,99) for i in range(n)]
else:
  v=[int(sys.argv[i]) for i in range(1,num)]
print v
c=0
quicksort(v,0,len(v)-1)
print v

