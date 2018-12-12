#!/usr/bin/python
import math

# Solution of a trigonometric equation using a function and its derivative

def f(a):
   return 2*math.pi*math.sin(a/2) - math.pi/2 - 4*a*math.sin(a/2) + a - math.sin(a)/2

def fp(a):
   return math.pi*math.cos(a/2) - 2*a*math.cos(a/2) - 4*math.sin(a/2) + 1 - math.cos(a)/2

a=math.pi*2/5
da=0.00001
maxIter=30
i=0
while i<maxIter :
   fa1   = f(a)
   # The commented lines were to calculate the slope using a point close to a.
   #fa2   = f(a+da)
   #slope = (fa2-fa1)/da
   # This part is to calculate the slope using the derivative function
   slope = fp(a)
   deltaA = -fa1/slope
   print i,"alpha=",a,'Function returns',fa1,'with slope',slope,' deltaAlpha:',deltaA
   a += deltaA
   i += 1

print 'For a field of 1 unit of radius, the rope has to be L = ',2*math.sin(a/2)
