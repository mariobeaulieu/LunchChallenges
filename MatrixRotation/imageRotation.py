#!/usr/bin/python
import sys
from PIL import Image


def usage():
    print('''
Program to rotate an array by 90 degrees.

The algorithm used is to switch the values of A->B->C->D->A
based on the diagram below:
   0 1 2 3 4 5 6 7 8 9
 0 . . . . . . . . . .
 1 . . A . . . . . . .
 2 . . . . . . . . B .
 3 . . . . . . . . . .
 4 . . . . . . . . . .
 5 . . . . . . . . . .
 6 . . . . . . . . . .
 7 . D . . . . . . . .
 8 . . . . . . . C . .
 9 . . . . . . . . . .

We proceed starting at row 0 from columns 0 to 8,
Then row 1, from columns 1 to 7, etc.
First, A <-> B, then A <-> C, then A <-> D
(It's like if A is the temp variable)
If i is the row, and j is the column:
  (i,j) <-> ( j ,n-i) (where n is 9-1 = 8)
  (i,j) <-> (n-i,n-j)
  (i,j) <-> (n-j, i )

The default is a matrix of 10x10, but if a numerical
parameter is given, verbosity is activated and that
value is used.
''')


usage()


# Image rotation


def rotate(m):
    num_rows = m.height
    n = num_rows - 1
    for i in range(num_rows):
        for j in range(i, num_rows - i - 1):
            i2 = j
            j2 = n - i
            i3 = n - i
            j3 = n - j
            i4 = n - j
            j4 = i
            temp = m.getpixel((i, j))
            m.putpixel((i, j), m.getpixel((i4, j4)))
            m.putpixel((i4, j4), m.getpixel((i3, j3)))
            m.putpixel((i3, j3), m.getpixel((i2, j2)))
            m.putpixel((i2, j2), temp)


imgFile = 'Apples.png'
try:
    img = Image.open(imgFile)
except:
    print("Cannot read image file ", imgFile)
    sys.exit(1)

# https://pillow.readthedocs.io/en/latest/reference/PixelAccess.html
# Pixels can be addressed with raw[i,j] and return (r,g,b)
N = img.height

print("Using an image of ", N, " x ", N)

img.show()

while True:
    print("Rotating image...")
    rotate(img)
    img.show()
    r = input("Press ENTER")
