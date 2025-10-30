# Memory Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *
from datetime import date, datetime

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
# Initialize these variables so they'll be accessible by functions
BOARDWIDTH = 10 # number of columns of icons
BOARDHEIGHT = 7 # number of rows of icons
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
name = ""

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

def main():
    global name, FPSCLOCK, DISPLAYSURF, BOARDWIDTH, BOARDHEIGHT, XMARGIN, YMARGIN
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    name = getInput("Enter your name")

    newLevel = True
    playAgain = True
    while playAgain:  # main game loop
        while newLevel:    # For text on top of the screen
            count = 0
            games = 0
            stats = []
            prev_ave = prev_count = 0

            size = getButtons("Select Game Size", ["2x4", "4x4", "4x6", "6x6", "6x8", "8x8", "QUIT"])
            if size == 6:
                pygame.quit()
                sys.exit(0)
            lastdate = "NEVER"
            lastaverage = "0"
            prev_ave = prev_count = 0
            today = str(date.today())
            try:
                with open(name.lower() + ".dat", 'r') as file:
                    # print("File exists and is ready to read")
                    for line in file:
                        line = line.strip()
                        data = line.split(":")
                        # if len(data) is not 4, there's a problem with the file and we skip that line
                        if len(data) == 4 and int(data[0]) == size:
                            lastdate = data[1]
                            lastcount = data[2]
                            lastaverage = data[3]
                # If the player already played today, today's stats will be added
                # How many days since that level was played?
                if lastdate != "NEVER":
                    days = (datetime.strptime(today, "%Y-%m-%d") - datetime.strptime(lastdate, "%Y-%m-%d")).days
                    if days == 0:
                        lastdate = "today"
                        prev_ave = float(lastaverage)
                        prev_count = int(lastcount)
                    elif days == 1:
                        lastdate = "yesterday"
                    else:
                        lastdate = str(days) + " days ago"
                getButtons("Level last played on " + lastdate + " with average of " + str(
                    (int(float(lastaverage) * 100)) / 100) + " tries", "Continue")
            except FileNotFoundError:
                getButtons("Welcome " + name + " as a new user ", ["OK"])

            i = (size + 3) % 2
            BOARDWIDTH = size + 3 + i  # number of columns of icons
            BOARDHEIGHT = size + 3 - i  # number of rows of icons
            XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
            YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

            BASICFONT = pygame.font.SysFont('chilanka', 32)
            playerName = BASICFONT.render(name, True, WHITE)
            playerNameRect = playerName.get_rect()
            playerNameRect.topleft = (10, 10)
            score = BASICFONT.render(str(count), True, WHITE)
            scoreRect = score.get_rect()
            scoreRect.topright = (WINDOWWIDTH - 10, 10)

            mousex = 0 # used to store x coordinate of mouse event
            mousey = 0 # used to store y coordinate of mouse event
            pygame.display.set_caption('Memory Game')

            mainBoard = getRandomizedBoard()
            revealedBoxes = generateRevealedBoxesData(False)

            firstSelection = None # stores the (x, y) of the first box clicked.

            DISPLAYSURF.fill(BGCOLOR)
            startGameAnimation(mainBoard)
            newLevel = False

        mouseClicked = False
        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, revealedBoxes)
        DISPLAYSURF.blit(playerName, playerNameRect)
        DISPLAYSURF.blit(score, scoreRect)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
               drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else: # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                    count += 1
                    score = BASICFONT.render(str(count), True, WHITE)
                    scoreRect = score.get_rect()
                    scoreRect.topright = (WINDOWWIDTH - 10, 10)
                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection [1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes): # check if all pairs found
                        gameWonAnimation(mainBoard)
                        stats.append(count)
                        games += 1

                        # Calculate current average
                        ave = 0
                        for v in stats:
                            ave += v
                        nbGames = len(stats) + prev_count
                        ave = (ave + prev_ave * prev_count) / nbGames

                        if lastdate == "NEVER":
                            mess = ["Your score is " + str(count), "Play again?"]
                        elif lastdate == "today":
                            mess = ["Your score is "+str(count), "Today you've played "+str(nbGames)+" times with an average of "+str(int(ave*100)/100), "Play again?"]
                        else:
                            mess = ["Your score is "+str(count), lastdate+" you've played "+str(lastcount)+" times with an average of "+str(int(float(lastaverage)*100)/100), "Play again?"]
                        rc = getButtons(mess, ["Yes", "No"])
                        print(rc)
                        if rc == 1:
                            # Save the score and exit
                            newLevel = True
                            with open(name.lower() + ".dat", 'a') as file:
                                file.write(str(size)+":"+ str(date.today())+":"+str(nbGames)+":"+str(ave)+"\n")

                        else:
                            # Reset the board
                            mainBoard = getRandomizedBoard()
                            revealedBoxes = generateRevealedBoxesData(False)

                            count = 0
                            score = BASICFONT.render(str(count), True, WHITE)
                            scoreRect = score.get_rect()
                            scoreRect.topright = (WINDOWWIDTH - 10, 10)

                            # Show the fully unrevealed board for a second.
                            drawBoard(mainBoard, revealedBoxes)
                            pygame.display.update()

                            # Replay the start game animation.
                            startGameAnimation(mainBoard)
                    firstSelection = None # reset firstSelection variable

        if playAgain:
            # Redraw the screen and wait a clock tick.
            pygame.display.update()
            FPSCLOCK.tick(FPS)


def getOkButton(message):
    DISPLAYSURF.fill((0,0,0))
    base_font = pygame.font.SysFont('', 32)
    # create rectangle
    mess_rect = pygame.Rect(200, 100, 140, 32)
    text_surface = base_font.render(message, True, (255, 0, 255))
    text_width = text_surface.get_width() + 10
    mess_rect.w = max(100, text_width)
    mess_rect.center=(WINDOWWIDTH/2, WINDOWHEIGHT/3)
    DISPLAYSURF.blit(text_surface, (mess_rect.x + 5, mess_rect.y + 5))
    pygame.display.flip()

    # Image of button
    btn_img = pygame.image.load('Button.png')
    btn_surface = pygame.transform.scale(btn_img, (100, 50))
    btn_rect = pygame.Rect(200, 250, 100, 50)
    btn_rect.center=(WINDOWWIDTH/2, WINDOWHEIGHT/2)
    DISPLAYSURF.blit(btn_surface, btn_rect)
    done = False
    mousex = mousey = 0
    while not done:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                print(mousex, mousey)
                minx=btn_rect.x
                miny=btn_rect.y
                maxx=btn_rect.x+btn_rect.w
                maxy=btn_rect.y+btn_rect.h
                if mousex>minx and mousex<maxx and mousey>miny and mousey<maxy:
                    done = True
            # elif event.key == pygame.K_RETURN:
            #      done = True
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos

        # Write the text in the button
        text_surface = base_font.render("OK", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        # render at position stated in arguments
        DISPLAYSURF.blit(text_surface, (btn_rect.centerx-text_rect.centerx, btn_rect.centery-text_rect.centery))
        pygame.display.flip()

        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        FPSCLOCK.tick(FPS)


def getButtons(mess, texts):
    DISPLAYSURF.fill((0,0,0))
    base_font = pygame.font.SysFont('', 32)

    # Is the message a list (many lines) or just one line?
    if isinstance(mess, list):
        numMess = len(mess)
    else:
        numMess = 1
        mess = [mess]
    messHeight = 32
    btnHeight = 50
    interspace = ( WINDOWHEIGHT - numMess*messHeight - btnHeight )/(numMess + 4)

    # create rectangle(s) for message(s)
    mess_rect=[]
    for m in range(numMess):
        mess_rect = pygame.Rect(200, 100, 140, messHeight)
        text_surface = base_font.render(mess[m], True, (255, 0, 255))
        text_width = text_surface.get_width() + 10
        mess_rect.w = max(100, text_width)
        messVertPos = int(2*interspace + messHeight/2 + (messHeight+interspace)*m)
        mess_rect.center=(WINDOWWIDTH/2, messVertPos)
        DISPLAYSURF.blit(text_surface, (mess_rect.x + 5, mess_rect.y + 5))
        pygame.display.flip()

    # Image of buttons
    btn_img = pygame.image.load('Button.png')
    btn_surf=[]
    btn_rect=[]
    txt_surf=[]
    txt_rect=[]
    spacing=10
    if not isinstance(texts, list):
        texts = [texts]
    nbButtons = len(texts)
    maxBtnWidth = (WINDOWWIDTH - (nbButtons+1)*spacing)/nbButtons
    btnWidth=int(min(100, maxBtnWidth))
    delta = (btnWidth+spacing)/2
    for i in range(nbButtons):
        btn_rect.append( pygame.Rect(200, 250, btnWidth, btnHeight) )
        btn_surf.append( pygame.transform.scale(btn_img, (btnWidth, btnHeight)) )
        btnVertPos = int(WINDOWHEIGHT - 2*interspace - btnHeight/2)
        btn_rect[i].center=(WINDOWWIDTH/2 - (nbButtons-1-2*i)*delta, btnVertPos)
        DISPLAYSURF.blit(btn_surf[i], btn_rect[i])
        # Write the text in the button
        txt_surf.append( base_font.render(texts[i], True, (255, 255, 255)) )
        text_rect = txt_surf[i].get_rect()
        # render at position stated in arguments
        DISPLAYSURF.blit(txt_surf[i], (btn_rect[i].centerx - text_rect.centerx, btn_rect[i].centery - text_rect.centery))
        pygame.display.flip()

    done = False
    btnId=-1
    mousex = mousey = 0
    while not done:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                # print(mousex, mousey)
                for i in range(nbButtons):
                    minx=btn_rect[i].x
                    miny=btn_rect[i].y
                    maxx=btn_rect[i].x+btn_rect[i].w
                    maxy=btn_rect[i].y+btn_rect[i].h
                    if mousex>minx and mousex<maxx and mousey>miny and mousey<maxy:
                        btnId=i
                        done = True
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos

        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        FPSCLOCK.tick(FPS)
    return btnId

def getInput(message):
    DISPLAYSURF.fill((0,0,0))
    # basic font for user typed
    base_font = pygame.font.SysFont('chilanka', 32)
    user_text = ''
    # create rectangle
    mess_rect = pygame.Rect(200, 100, 140, 32)
    text_surface = base_font.render(message, True, (255, 0, 255))
    DISPLAYSURF.blit(text_surface, (mess_rect.x + 5, mess_rect.y + 5))
    text_width = text_surface.get_width() + 10
    mess_rect.w = max(100, text_width)
    pygame.display.flip()

    input_rect = pygame.Rect(200, 200, 140, 32)
    notDone = True
    while notDone:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                # Unicode standard is used for string
                # formation
                else:
                    if event.key == pygame.K_RETURN:
                        notDone = False
                    else:
                        user_text += event.unicode
                        # print(user_text)
        pygame.draw.rect(DISPLAYSURF, pygame.Color('lightskyblue3'), input_rect)
        text_surface = base_font.render(user_text, True, (255, 255, 255))

        # render at position stated in arguments
        DISPLAYSURF.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = mess_rect.w

        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()

        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        FPSCLOCK.tick(FPS)
    # print("user_text should be returned:"+user_text)
    return user_text


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2 # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half =    int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, - REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True


if __name__ == '__main__':
    main()
