#!/usr/bin/python

v=input("Enter value to evaluate: ")
while v>0:
  for d in range(10):
    str_v = str(v)
    v_size=len(str_v)
    count = 0 # count is the number of digits found
    f     = 1 # f is the factor for the digit of v being considered. We start with digit 1
    v0    = 1 # v0 is 1 + the value of all digits following curr digit. Ex: in 1234 if cur digit=2 then v0=35
    for i in range(v_size):
      i1=i+1
      n=int(str_v[v_size-i1:v_size-i]) # n is the digit of v being considered. We start with units
      # This is for the current digit
      if   n > d:
           count += f
      elif n ==d:
           count += v0
      # And this is for all lower digits
      count += n*i*f/10
      if d==0 and i>0:
          count -= f
      f *= 10
      v0 = 1+int(str_v[-i1:])
 
    print "There are ",count," digits ",d," in the series from 0 to ",v," (inclusive)"
  v=input("Enter value to evaluate: ")
