#!/usr/bin/env python3

from sys import stdin

def checkSequence(word,sentence):
   wl    = len(word)
   sl    = len(sentence)
   p     = 0
   while p < sl:
     #print ('p=%i, sl=%i, word=%s, sentence=%s'%(p, sl, word, sentence[p:p+wl]))
     if word != sentence[p:p+wl]:
        #print ("Didn't match")
        return False
     p += wl
   #print('Match found with %i values'%count)
   return True

# This function will return True if items in myList have a periodicity with index i
def checkSerie(di,myList):
  print ('Using di=',di)
  posi = myList[di]
  dpos = posi - myList[0]
  for i in range(2*di,len(myList),di):
    if myList[i] - posi != dpos:
      #print ('In list',myList,'index',i,'failed:',myList[i],'-',posi,'!=',dpos)
      return False
    #print ('In list',myList,'index',i,'passed:',myList[i],'-',posi,'==',dpos)
    posi = myList[i]
  return True

case = 0
for line in stdin:
    line       = line.strip()
    lineLength = seqLength = len(line)
    letters    = set(line)
    positions  = dict.fromkeys(letters)
    for i,c in enumerate(line):
      if positions[c] == None:
         positions[c] = [i]
      else:
         positions[c].append(i)
    # Find the list of positions with the least number of entries
    n = lineLength
    v = line[0]
    for c in letters:
      if len(positions[c])<n:
         n = len(positions[c])
         v = c
    print ('Using letter',v,'with list of positions=',positions[v])
    # index 0 starts the first pattern
    # find at which index the pattern repeats
    for i in range(1,n):
      if checkSerie(i,positions[v]):
        # The letter repeats at every i intervals, check if the whole pattern works
        seqL = positions[v][i]-positions[v][0]
        if checkSequence(line[:seqL],line[seqL:]):
           #print('checkSequence(',line[:seqL],',',line[seqL:],') passed')
           seqLength = seqL
           break
    numSeq = lineLength / seqLength
    print ('%s is composed of %i sequences of %s\n'%(line,numSeq,line[:seqLength]))
