#!/usr/bin/python

# This problem is to identify if a list of word is sorted
# according to a dictionary.
# For instance, with dictionary order:   ['m','y','d','i','c','t']
# The following list of words is sorted: ['mmdy','dim','cid','cit','tidi','tic']
#
order='zyxwvutsrqponmlkjihgfedcba'
maxWordLength=10

def checkSort(words):
  indexes=[0 for i in range(maxWordLength)]
  prevWord=''
  fail=False

  print 'Order of letters is this:',order
  print 'Words to sort:           ',words

  for w in words:
    wordOK=False
    for i in range(maxWordLength):
      if i < len(w):
         letter= w[i]
         index = order.index(letter)
      else:
         index = 0
      # wordOK means that we already found the words are in correct order.
      # We continue the loop to fill up the indexes array but without
      # checking for a failure anymor
      if not wordOK:
         if indexes[i]>index:
            print 'Words %s and %s are in the wrong order'%(prevWord,w)
            fail=True
            break
         elif indexes[i]<index:
            wordOK=True
            # print '%s < %s'%(prevWord,w)
      indexes[i] = index
    # put zeros for the rest of the indexes
    if fail:
      break
    prevWord=w
  for j in range(i+1, maxWordLength):
    indexes[j]=0
  if fail:
    print 'List is NOT ordered'
  else:
    print 'List is ordered'
  print

myList = ['goodbye','diamant' ,'diamond' ,'carrot','bonjour','allo']
checkSort(myList)
myList = ['goodbye','diamond' ,'diamant' ,'carrot','bonjour','allo']
checkSort(myList)
myList = ['goodbye','diamond' ,'diamonds','carrot','bonjour','allo']
checkSort(myList)
myList = ['goodbye','diamonds','diamond' ,'carrot','bonjour','allo']
checkSort(myList)
