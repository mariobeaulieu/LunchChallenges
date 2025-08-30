#!/usr/bin/python3
import sys

def inverse(a):
    global ops
    length  = len(a)
    if length < 2:
        if verbosity:
             print (f"Array length is {length}")
        return a
    length2 = length//2
    if verbosity:
        print (f"Array to inverse: {a}")
    for i in range(0, length2):
        a[i],a[length-i-1] = a[length-i-1],a[i]
        ops += 1
    if verbosity:
        print (f"Inversed array:   {a}")
    return a

def rotate(n, array):
    length=len(array)
    # Just in case rotation count is larger than array size
    n = n % length
    x= inverse( inverse( array[:length-n] ) + inverse( array[length-n:] ) )
    if verbosity:
        print (f"Array of length {length} rotated of {n} positions: {x}")
    return x

def rotate_push(n, array):
    global ops
    i0 = i = 0
    n_done = 0
    v = array[0]
    L = len(array)
    while n_done < L:
        ops    += 1
        i2 = (i+n)%L
        if verbosity:
            print (f"{ops}) Index {i} -> index {i2}")
        array[i2],v  = v, array[i2]
        n_done += 1
        if i2 == i0:
            i0 = i2 = (i2+1)%L
            v=array[i0]
        i = i2
    return array

def get_int(msg):
    err=1
    v=0
    while err == 1:
        try:
            v   = int(input(msg))
            err = 0
        except:
            continue
    return v

arrayLength=0
shift=0
verbosity = False
if len(sys.argv)>1:
    if sys.argv[1] == '-v':
        verbosity = True
        print ("Verbose is True")

if arrayLength == 0:
    arrayLength = get_int("Enter array length: ")
    shift = get_int("Enter number of positions to rotate: ")

ops=0
array = list(range(0,arrayLength))
print (f"Original array: .............. {array}")
arrayWithInversions = rotate(shift, array)
print (f"Shifted array with inversions: {arrayWithInversions}")
print (f"Number of operations: .......  {ops}")
ops=0
array = list(range(0,arrayLength))
print (f"\nOriginal array: .............. {array}")
arrayWithSequence = rotate_push(shift, array)
print (f"Shifted array with sequence:   {arrayWithSequence}")
print (f"Number of operations: .......  {ops}")
