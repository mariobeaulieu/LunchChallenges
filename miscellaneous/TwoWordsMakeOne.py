#!/usr/bin/python

#This program finds the longest word in a list that is composed of 2 other words

nbLength=20 # Words are from 1 to 100 letters long
showAllWords = True

# Initialize arrays
# nbLetters[i] is the number of words of i letters long in the list
nbLetters = [ 0 for i in range(nbLength) ]
# words[i] is the list of indexes of words of i letters long
words  = [[] for i in range(nbLength)]

f=open('warandpeace.txt','r')
numWords=0
for line in f:
   for word in line.split():
      numWords+=1
      i = len(word)
      nbLetters[i] += 1
      words[i].append(word)
f.close()

# Convert into a set to remove duplicates
nn=0
for i in range(nbLength):
   words[i] = set(words[i])
   nn += len(words[i])

print 'We have',numWords,'words (',nn,'unique words)'

# Look at the list in reverse order to find the longest one
done = False
for i in range(nbLength-1, 1, -1):
   if nbLetters[i] > 0:
      for word in words[i]:
         # Now test words starting with lenght 1 up to length i-1
         for j in range(1,i):
            k=i-j
            if nbLetters[j]>0 and nbLetters[k]>0:
               for w1 in words[j]:
                  if word.startswith(w1):
                     for w2 in words[k]:
                        if word.endswith(w2):
                           done = True
                           break
                  if done:
                     print word,'is composed of words ',w1,'and',w2
                     done = not showAllWords
                     break
            if done: break
         if done: break
   if done: break
