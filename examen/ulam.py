#!/usr/bin/env python3

# ulam
# First, create the prime array

from sys import stdin

global cost

def nextPrime(limit):
   flags = [False]*(limit+1)
   for i in range(2,limit):
     if flags[i]:
        continue
     for j in range(2*i,limit+1,i):
        flags[j]=True
     yield i

def findValue(v):
    # Find value v in a ulam spiral of side SIZE
    y=x=int(SIZE/2)
    s=1
    c=1
    dx=1
    dy=0
    #print('c=%i, [dx,dy]=[%i,%i], [x,y]=[%i,%i]'%(c,dx,dy,x,y))
    while c<v:
      if c+s>=v:
         s=v-c
         #print('c=%i, resized s to %i to jump to %i'%(c,s,v))
         if   dx>0: dx=s
         elif dx<0: dx=-s
         elif dy>0: dy=s
         elif dy<0: dy=-s
         c+=s
         x+=dx
         y+=dy
         #print('c=%i, [dx,dy]=[%i,%i], [x,y]=[%i,%i]'%(c,dx,dy,x,y))
      else:
         c+=s
         x+=dx
         y+=dy
         #print('c=%i, [dx,dy]=[%i,%i], [x,y]=[%i,%i]'%(c,dx,dy,x,y))
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

def play(x,y,x2,y2,c):
    global cost
    if cost[x][y] == -1:         return
    if c>SIZE or c>cost[x2][y2]: return
    if cost[x][y]<=c:            return
    cost[x][y]=c
    if x>minx   : play(x-1, y ,x2,y2,c+1)
    if x<maxx-1 : play(x+1, y ,x2,y2,c+1)
    if y>miny   : play( x ,y-1,x2,y2,c+1)
    if y<maxy-1 : play( x ,y+1,x2,y2,c+1)

def printCost():
  for i in range(miny,maxy+1):
     for j in range(minx,maxx+1):
        print('%5i'%cost[j][i],end='')
     print()

OFFSET=40
SIZE  = 101+OFFSET
minx=miny=0
maxx=maxy=SIZE
MAXCOST = 999
limit = SIZE*SIZE
cost=[[0]*SIZE for i in range(SIZE)]
primes=[]
for p in nextPrime(limit):
  primes.append(p)
  x,y=findValue(p)
  cost[x][y]=p

case = 0
for line in stdin:
    if line.strip() != '':
        case += 1
        values=line.split(' ')
        v1    = int(values[0])
        v2    = int(values[1])
        x1,y1 = findValue(v1)
        x2,y2 = findValue(v2)
        # Lets limit the search
        minx = max(min(x1,x2)-OFFSET,0)
        maxx = min(max(x1,x2)+OFFSET,SIZE)
        miny = max(min(y1,y2)-OFFSET,0)
        maxy = min(max(y1,y2)+OFFSET,SIZE)
        #printCost()
        # Initialize cost matrix to max values
        for i in range(minx,maxx):
          for j in range(miny,maxy):
            cost[i][j]=MAXCOST
        for p in primes:
          x,y = findValue(p)
          cost[x][y]=-1
        play(x1,y1,x2,y2,0)
        r = cost[x2][y2]
        if r == MAXCOST:
           print ('Case %i: impossible'%(case))
        else:
           print ('Case %i: %i'%(case,r))
        #printCost()
