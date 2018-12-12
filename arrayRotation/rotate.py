#!/usr/bin/python
import sys

def inverse(a):
	global ops
	length  = len(a)
	if length < 2:
		if verbose:
			 print "Array length is ",length
		return a
        length2 = length//2
	if verbose:
		print "Array to inverse: ",a
	for i in range(0, length2):
		a[i],a[length-i-1] = a[length-i-1],a[i]
		ops += 1
	if verbose:
		print "Inversed array:   ",a
	return a

def rotate(n, array):
	length=len(array)
	# Just in case rotation count is larger than array size
	n = n % length
	x= inverse( inverse( array[:length-n] ) + inverse( array[length-n:] ) )
	if verbose:
		print "Array of length %i rotated of %i positions: "%(length,n),x
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
		if verbose:
			print ops,") Index ",i," -> index ",i2
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
			t   = raw_input(msg)
			v   = int(t)
			err = 0
		except:
			continue
	return v

arrayLength=1
verbose = False
if len(sys.argv)>1:
	if sys.argv[1] == '-v':
		verbose = True
		print "Verbose is True"

while arrayLength > 0:
  arrayLength = get_int("Enter array length: ")
  if arrayLength > 0:
	shift = get_int("Enter number of positions to rotate: ")
        ops=0
	array = range(0,arrayLength)
	print "Original array: .............. ",array
	arrayWithInversions = rotate(shift, array)
        print "Shifted array with inversions: ",arrayWithInversions
	print "Number of operations: .......  ",ops
        ops=0
	array = range(0,arrayLength)
	print "\nOriginal array: .............. ",array
        arrayWithSequence = rotate_push(shift, array)
        print "Shifted array with sequence:   ",arrayWithSequence
	print "Number of operations: .......  ",ops


