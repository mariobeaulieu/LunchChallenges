#!/usr/bin/python


# This project is to find if a word partially matches with a list of words
# Example:
# Word: banana
# List: [bana, apple, bananas, bahama]
# The comparison should say that bananas matches with 1 error
# A missing letter counts as 1 error
# A letter inserted anywhere counts as 1 error
# A letter substituted for another counts as 1 error

def partialMatch(target, word):
  lt = len(target)
  lw = len(word)
  for i in range(lt):
    if lw<=i:
       # If we reached the end of the word, each additional letter in target counts as 1 error
       return lt - i
    #print 'Comparing letters %s and %s'%(target[i],word[i])
    if target[i] != word[i]:
       # 3 possibilities here, assuming the target word is good:
       # 1-The word has 1 missing letter
       #   We need to continue by checking word[i+1...] against target[i...]
       #
       # If we reached the end of word, numbers of errors is the number of extra letters in target
       if lw<=i+1:
          e1=lt-lw
       else:
          t=target[i:]
          w=word[i+1:]
          #print 'Comparing %s and %s'%(t,w)
          e1 = partialMatch(t, w)
       #print 'Got %i errors'%(e1)
       # 2-The target's letter has been replaced by another letter
       #   We need to continue by checking word[i+1...] against target[i+1...]
       #
       if lw<=i+1:
          # If we reached the end of word, numbers of errors is the number of extra letters in target
          e2=lt-lw
       elif lt<=i+1:
          # If we reached the end of target, numbers of errors is the number of extra letters in word
          e2=lw-lt
       else:
          t=target[i+1:]
          w=word[i+1:]
          #print 'Comparing %s and %s'%(t,w)
          e2 = partialMatch(t, w)
          #print 'Got %i errors'%(e2)
       # 3-The word have 1 letter that has been inserted
       #   We need to continue by checking word[i...] against target[i+1...]
       if lt<=i+1:
          # If we reached the end of target, numbers of errors is the number of extra letters in word
          e3=lw-lt
       else:
          t=target[i+1:]
          w=word[i:]
          #print 'Comparing %s and %s'%(t,w)
          e3 = partialMatch(t, w)
       #print 'Got %i errors for a minimum of %i'%(e3,min(e1,e2,e3)+1)
       # The number of errors to return is the minimum of e1, e2, e3
       return min(e1,e2,e3)+1
  # If we have reached the end of a word, each letter left in the 
  # other word counts as an additional error
  return lw-lt

def evaluateList(t,ml):
  for v in ml:
     r = partialMatch(t,v)
     print 'Comparing %s with %s returned %i differences'%(t,v,r)

myTarget='banana'
myList  =['apple','pomme','grapefruit','avocado','bannana','ananas','pineapple','banane']
evaluateList(myTarget,myList)

myTarget = input ('Enter a target word between quotes such as "banana": ')
myList   = input ('Enter a list of words in quotes in square brackets such as ["ape","monkey","horse"]: ')
evaluateList(myTarget,myList)

