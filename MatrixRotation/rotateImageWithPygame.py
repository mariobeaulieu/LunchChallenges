#!/usr/bin/python

import sys, pygame
pygame.init()

def rotate(w,m):
    num_rows = w
    n = num_rows - 1
    for i in range(num_rows):
        for j in range(i, num_rows - i - 1):
            i2 = j
            j2 = n - i
            i3 = n - i
            j3 = n - j
            i4 = n - j
            j4 = i
            temp = m.get_at((i, j))
            m.set_at((i , j ), m.get_at((i4, j4)))
            m.set_at((i4, j4), m.get_at((i3, j3)))
            m.set_at((i3, j3), m.get_at((i2, j2)))
            m.set_at((i2, j2), temp)
        pygame.display.flip()

imgFile = 'Apples.png'
try:
    picture = pygame.image.load(imgFile)
except:
    print("Cannot read image file ", imgFile)
    sys.exit(1)

p       = picture.get_rect()
width   = p.right
#Use the smaller of width and height
if p.bottom < p.right:
    width = p.bottom

print("Using an image of ", width, " x ", width)
screen = pygame.display.set_mode((width,width))
screen.blit(picture, p)
pygame.display.flip()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    rotate(width, screen)
    r = raw_input("Press ENTER")
