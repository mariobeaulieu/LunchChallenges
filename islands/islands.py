#!/usr/bin/python

# This program finds the number of islands
# Spaces in the matrix correspond to water, anything else is land.
m=[]
m.append('                     ###         ##        #         ')
m.append('     ###              ###      ###       ##          ')
m.append('      ###           ###    ######       ##           ')
m.append('                          ########    ###            ')
m.append('         ###########                  #              ')
m.append('  ##        ####                     ##              ')
m.append('   ##      ##         #             ##               ')
m.append('    ########         ###           ##     ##         ')
m.append('         ##         ####          ##     ###         ')
m.append('        ###          ##          ##        #         ')
m.append('      ###    ####               ###                  ')
m.append('        ######  #########   #####                    ')
m.append('                        #####                        ')
m.append('                                                     ')
m.append('                                                     ')
m.append('                                                     ')
m.append('                                                     ')
# In the matrix above, there are 7 islands

islandId   = 0
numIslands = 0
# rowAbove is the list of island ids for the row above the current one.
# zeros mean water, other values is island number.
# We initialize it all zeros
rowAbove = [0 for i in range(len(m[0]))]

for r in range(len(m)):
   # For each character in the current row, we set to 0 if it's water
   # and we give it the number of the island above if there's an
   # island above.
   prev = 0 # This is the value of the cel to our left. We assume 0 initially
   for c in range(len(m[r])):
      idToUse = 0
      if m[r][c] != ' ':
         if rowAbove[c]>0 :
            # The cell we are at is the continuation of the island above
            # But what about the previous cell?
            # If prev cell is another island, it means we just joined
            # 2 islands.
            # This means changing the codes from beginning of row to here
            # and decrement the number of islands since we are merging 2
            idToUse = rowAbove[c]
            if prev != 0 and prev != idToUse:
               numIslands -= 1
               for i in range(c):
                  if rowAbove[i] == prev:
                     rowAbove[i] =  idToUse
         else:
            # We have hit an island and there's water above us
            # Is it the continuation of an island on our left?
            if prev != 0:
               idToUse = prev
            else:
               # It's a new island!
               numIslands += 1
               islandId   += 1
               idToUse     = islandId
      rowAbove[c] = idToUse
      prev        = idToUse
   # At the end of each row, print the list of rowAbove
   for i in range(len(rowAbove)):
       print '%2i'%(rowAbove[i]),
   print

# At the very end, how many islands did we find?
print '%2i islands were found'%(numIslands)

