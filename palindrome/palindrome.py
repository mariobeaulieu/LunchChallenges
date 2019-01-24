#!/usr/bin/python
import logging
logging.basicConfig(filename='palindrome.log',level=logging.DEBUG)

def palindromize(text,offset):
  textLength=len(text)
  logging.debug("Processing <%s>"%(text[offset:textLength-offset]))
  if textLength == 2*offset:
    return
  subLength=0
  for i in range(1,textLength/2-offset+1):
    logging.debug("Comparing <%s> with <%s>"%(text[offset:offset+i],text[textLength-offset-i:textLength-offset]))
    if text[offset:offset+i] == text[textLength-offset-i:textLength-offset]:
      subLength=i
      logging.debug("SubLength is %i"%(i))
  if subLength == 0:
    # No palindrome found, parenthesis around the whole thing
    print '('+text[offset:textLength-offset]+')',
  else:
    print '('+text[offset:offset+subLength]+')',
    palindromize(text,offset+subLength)
    print '('+text[offset:offset+subLength]+')',
  
text=" "
while len(text) > 0:
   text=raw_input("Enter text to be palindromized: ")
   palindromize(text,0)
   print
