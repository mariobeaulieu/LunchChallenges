#!/usr/bin/env python3

# ulam
# First, create the prime array

from sys import stdin

def ulam(width,u):
    w2     = width*width
    x      = int(width/2)
    y      = x
    step   = 1
    dx     = 1
    dy     = 0
    nbSteps= 0
    # To find primes
    flags  = [True]*(w2+1)
    p      = 2
    for i in range(2*p,w2+1,p):
        flags[i]=False
    for v in range(1,w2+1):
       print(x,y,v,p)
       if v == p:
          u[x][y]= 0
          # Find the next prime after p
          for p in range(p+1,w2+1):
              if flags[p]:
                  break
          # This is for when we reach the end of flags
          # otherwise the last value is considered prime
          if p == w2:
             p +=1
          # Mark multiples of that new prime as not primes
          for i in range(2*p,w2+1,p):
              flags[i]=False
       else:
          u[x][y]= v
       x       += dx
       y       += dy
       nbSteps += 1
       if nbSteps == step:
          if dx==1:
             dx=0
             dy=-1
          elif dy==-1:
             dx=-1
             dy=0
             step+=1
          elif dx==-1:
             dx=0
             dy=1
          elif dy==1:
             dx=1
             dy=0
             step+=1
          nbSteps=0

def findValue(w,v):
    # Find value v in a ulam spiral of side w
    y=x=int(w/2)
    s=1
    c=1
    dx=1
    dy=0
    print('c=%i, [dx,dy]=[%i,%i], [x,y]=[%i,%i]'%(c,dx,dy,x,y))
    while c<v:
      if c+s>=v:
         s=v-c
         print('c=%i, resized s to %i to jump to %i'%(c,s,v))
         if   dx>0: dx=s
         elif dx<0: dx=-s
         elif dy>0: dy=s
         elif dy<0: dy=-s
         c+=s
         x+=dx
         y+=dy
         print('c=%i, [dx,dy]=[%i,%i], [x,y]=[%i,%i]'%(c,dx,dy,x,y))
      else:
         c+=s
         x+=dx
         y+=dy
         print('c=%i, [dx,dy]=[%i,%i], [x,y]=[%i,%i]'%(c,dx,dy,x,y))
         if dx==s:
            dx=0
            dy=-s
         elif dy==-s:
            s+=1
            dx=-s
            dy=0
         elif dx==-s:
            dx=0
            dy=s
         elif dy==s:
            s+=1
            dx=s
            dy=0
    return x,y

def printmatrix(w,u):
    for row in range(w):
        for col in range(w):
           print('%4i'%(u[col][row]),end=' ')
        print()

w=5
u=[[0]*w for i in range(w)]
ulam(w,u)
printmatrix(w,u)

case = 0
for line in stdin:
    if line.strip() != '':
        case += 1
        values=line.split(' ')
        v1    = int(values[0])
        v2    = int(values[1])
        print(v1,v2)
        x,y = findValue(w,v1)
        print(v1,x,y)
        x,y = findValue(w,v2)
        print(v2,x,y)

