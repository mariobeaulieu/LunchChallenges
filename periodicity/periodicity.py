#!/usr/bin/env python3

from sys import stdin

def checkSequence(word,sentence):
   wl    = len(word)
   sl    = len(sentence)
   p     = 0
   count = 0
   while p < sl:
     #print ('p=%i, sl=%i, word=%s, sentence=%s'%(p, sl, word, sentence[p:p+wl]))
     if word != sentence[p:p+wl]:
        #print ("Didn't match")
        return 0
     p     += wl
     count += 1
   #print('Match found with %i values'%count)
   return count

case = 0
for line in stdin:
    line = line.strip()
    if line != '':
        c        = 0
        currChar = 0
        nextChar = 1
        strLength= len(line)
        repetCount = 0
        seqLength  = 1
        found      = False
        while 2*seqLength <= strLength:
           c = checkSequence(line[0:seqLength],line[seqLength:])
           if c > 0: 
              found = True
              break
           seqLength += 1
        if not found:
           seqLength = strLength
        print ('%s is composed of %i sequences of %s\n'%(line,c+1,line[:seqLength]))
