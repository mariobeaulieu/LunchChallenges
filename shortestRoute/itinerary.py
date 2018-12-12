#!/usr/bin/python
import sys
import getopt

usage = '''
In a rectangular array 20 x 20 containing blocked cells, calculate the best
itinerary to go from initial position to destination

Usage:  ./itinerary.py [-d] [-s 'x,y'] [-d 'x,y'] [-b 'x,y'] [-b 'x,y'] ...
        where -d is to allow diagonal moves
              -s 'x,y' is to specify the starting position
              -e 'x,y' is to specify the ending position
              -b 'x,y' is to add positions to block the path

'''
MAX=99
SIZE=20
DIAGONALS=False
showCost = False

class P:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
class Cell:
    def __init__(self,cost):
        self.cost      = cost
        self.previous  = []
        self.blocked   = False
        self.start     = False
        self.dest      = False
        self.path      = False

    def printCell(self):
        if self.blocked: print u"\b\u2588\u2588\u2588",
        elif self.start: print "S ",
        elif self.dest:  print "E ",
        elif showCost:   print '%2i'%(self.cost),
        elif self.path:  print "* ",
        else:            print ". ",

class Game:
    def __init__(self,n):
        self.size = n
        # Create the array:
        self.m=[[Cell(MAX) for i in range(n)] for j in range(n)]

    def cell(self,p):
        return self.m[p.x][p.y]

    def setStart(self,p):
        self.cell(p).start = True

    def setDest(self,p):
        self.cell(p).dest = True

    def blockCells(self,points):
        for p in points:
            self.cell(p).blocked = True

    def printGame(self):
        print '--',
        for j in range(SIZE): print '%2i'%(j),
        print
        for i in range(SIZE):
            print '%3i'%(i),
            for j in range(SIZE):
                self.m[j][i].printCell()
            print

def play(xp,yp,x,y,c):
    # I just landed at position p
    # If my cost is lower than actual cost of this cell, I move in
    # If my cost is same or higher, I return
    g=game.m[x][y]
    if g.cost > c and not g.blocked:
        g.cost = c
        g.previous = P(xp,yp)
        if x>0      : play(x,y,x-1, y ,c+1)
        if x<SIZE-1 : play(x,y,x+1, y ,c+1)
        if y>0      : play(x,y, x ,y-1,c+1)
        if y<SIZE-1 : play(x,y, x ,y+1,c+1)
        if DIAGONALS:
            if x>0 and y>0           : play(x,y,x-1,y-1,c+1.4)
            if x<SIZE-1 and y<SIZE-1 : play(x,y,x+1,y+1,c+1.4)
            if x<SIZE-1 and y>0      : play(x,y,x+1,y-1,c+1.4)
            if x>0 and y<SIZE-1      : play(x,y,x-1,y+1,c+1.4)

def decodePoint(pair):
    # pair is expected to be in the form of the text x,y such as 12,14
    v=pair.split(',')
    try:
        p=P(int(v[0]),int(v[1]))
    except:
        print 'Invalid point coordinates: <',pair,'>'
        sys.exit(1)
    return p

def main():
    global game
    global DIAGONALS
    global showCost

    # Parse arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdcs:e:b:",['help',"diagonal",'cost','start=','end=','block='])
    except getopt.GetoptError:
        print usage
        sys.exit(2)

    start = P(6,6)
    dest  = P(12,12)
    block = []
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print usage
            sys.exit()
        elif opt in ("-d", "--diagonal"):
            DIAGONALS = True
        elif opt in ("-c", "--cost"):
            showCost = True
        elif opt in ('-s', '--start'):
            start = decodePoint(arg)
        elif opt in ('-e', '--end'):
            dest  = decodePoint(arg)
        elif opt in ('-b', '--block'):
            block.append(decodePoint(arg))

    game = Game(20)
    game.blockCells(block)
    game.blockCells({P(i,10) for i in range(5,15)})
    game.blockCells({P(7, i) for i in range(3,15)})
    game.blockCells({P(13,i) for i in range(7,13)})
    game.setStart(start)
    game.setDest(dest)
    game.printGame()

    print "\nStarting game..."
    play(0,0,start.x,start.y,0)
    # Mark the best path
    p=dest
    while True:
      p=game.m[p.x][p.y].previous
      g=game.m[p.x][p.y]
      if g.cost == 0: break
      g.path = True

    print "Solution:"
    game.printGame()

main()

