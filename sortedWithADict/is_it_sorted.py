#!/usr/bin/python

# This problem is to identify if a list of word is sorted
# according to a dictionary.
# For instance, with dictionary order:   ['m','y','d','i','c','t']
# The following list of words is sorted: ['mmdy','dim','cid','cit','tidi','tic']
#
order='zyxwvutsrqponmlkjihgfedcba'
words=['goodbye','diamond','carrot','bonjour','allo']
maxWordLength=10

indexes=[0 for i in range(maxWordLength)]
prevWord=''
fail=False

print 'Order of letters is this:',order

for w in words:
  wordOK=False
  for i in range(len(w)):
    letter=w[i]
    index =order.index(letter)
    # wordOK means that we already found the words are in correct order.
    # We continue the loop to fill up the indexes array but without
    # checking for a failure anymor
    if not wordOK:
       if index<indexes[i]:
          print 'Words %s and %s are in the wrong order'%(prevWord,w)
          fail=True
          break
       elif index>indexes[i]:
          wordOK=True
    indexes[i] = index
  # put zeros for the rest of the indexes
  if fail:
    break
  prevWord=w
  for j in range(i+1, maxWordLength):
    indexes[j]=0
if fail:
  print 'List is not ordered: ',words
else:
  print 'List is ordered:',words


