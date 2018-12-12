#!/usr/bin/python

import sys, pygame,time
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
            m[i , j ], m[i4, j4] = m[i4, j4], m[i , j ]
            m[i4, j4], m[i3, j3] = m[i3, j3], m[i4, j4]
            m[i3, j3], m[i2, j2] = m[i2, j2], m[i3, j3]
        if i % 20 == 0:
            pygame.display.flip()
            time.sleep(0.5)
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
screen = pygame.display.set_mode((width,width),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
screen.blit(picture, p)
pygame.display.flip()
array = pygame.PixelArray(screen)

print "Click top left corner to rotate, bottom right to exit"
top = int(width * 5 / 100)
bot = width - top
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            coord = pygame.mouse.get_pos()
            print "Mouse down at ", coord
            if coord[0]<top and coord[1]<top: 
               rotate(width, array)
            if coord[0]>bot and coord[1]>bot:
               sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            newSize = event.dict['size']
            print "New screen size: ", newSize
            screen = pygame.display.set_mode(newSize,pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
            #screen.blit(picture, p)
            screen.blit(pygame.transform.scale(picture, newSize), (0, 0))
            pygame.display.flip()
