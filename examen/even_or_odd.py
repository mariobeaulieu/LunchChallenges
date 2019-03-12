# Test question 1
from sys import stdin
input()
for line in stdin:
    if line.strip() != '':
        n=int(line)
        if n%2:
            print(str(n)+" is odd")
        else:
            print(str(n)+" is even") 


