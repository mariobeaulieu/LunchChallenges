#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt

c=0

def get_gaussian_random():
    global c
    c += 1
    m = 0
    while m == 0:
        m = round(np.random.random() * 100)
    numbers = np.random.random(int(m))
    #print c,"values, m=",m,len(numbers),"numbers generated"
    summation = float(np.sum(numbers))
    gaussian = (summation - m/2) / math.sqrt(m/12.0)

    return gaussian

def generate_known_gaussian(dimensions):
    count = 1000

    ret = []
    for i in xrange(count):
        current_vector = []
        for j in xrange(dimensions):
            g = get_gaussian_random()
            current_vector.append(g)

        ret.append( tuple(current_vector) )

    return ret

def plotData(array):
    numCategories = 20
    myMax=myMin=array[0]
    for v in array:
       if myMax<v: myMax=v*1.05
       if myMin>v: myMin=v
    numValues = [0 for i in range(numCategories)]
    dv = (myMax-myMin)/numCategories
    for v in array:
       c = int((v-myMin)/dv)
       numValues[c] += 1
    maxCount=0
    for i in range(numCategories):
       if maxCount<numValues[i]: maxCount=numValues[i]

    plt.scatter(range(numCategories), numValues)
    #plt.axis(0, numCategories, 0, maxCount)
    #plt.hlines(0, 0, numCategories)
    #plt.vlines(0, 0, maxCount)
    plt.show()

def main():
    known = generate_known_gaussian(2)
    target_mean = np.matrix([ [1.0], [5.0]])
    target_cov  = np.matrix([[  1.0, 0.7], 
                             [  0.7, 0.6]])

    [eigenvalues, eigenvectors] = np.linalg.eig(target_cov)
    l = np.matrix(np.diag(np.sqrt(eigenvalues)))
    Q = np.matrix(eigenvectors) * l
    x1_tweaked = []
    x2_tweaked = []
    tweaked_all = []
    for i, j in known:
        original = np.matrix( [[i], [j]]).copy()
        tweaked = (Q * original) + target_mean
        x1_tweaked.append(float(tweaked[0]))
        x2_tweaked.append(float(tweaked[1]))
        tweaked_all.append( tweaked )
    # print 'x1_tweaked=',x1_tweaked
    # print 'x2_tweaked=',x2_tweaked
    plt.scatter(x1_tweaked, x2_tweaked)
    plt.scatter([-1,-1,1,1], [-1,1,1,-1])
    plt.axis([-6, 10, -6, 10])
    plt.hlines(0, -6, 10)
    plt.vlines(0, -6, 10)
    plt.show()

    # Graph of x1_tweaked
    plotData(x1_tweaked)
    # Graph of x2_tweaked
    plotData(x2_tweaked)

if __name__ == "__main__":
    main()

