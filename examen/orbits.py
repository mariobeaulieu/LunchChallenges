#!/usr/bin/env python3

from sys import stdin
case = 0
for line in stdin:
    if line.strip() != '':
        case += 1
        days=line.split(' ')
        e   = int(days[0])
        m   = int(days[1])
        oe=365
        om=687
        de=(oe-e)%oe
        dm=(om-m)%om
        while de != dm:
          while de<dm:
            de+=oe
          if de!= dm:
            dm += om
        print('Case %i: %i'%(case,de))
