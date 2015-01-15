#2048 (python replica)
#By Banji Afolabi
#VERSION 1.3

#hbb: Header Button or Border
#MTT: Merged This Turn
# * : Remove All Of These Comments To View Board Log As You Play

import pygame, sys, random
from pygame.locals import *

#CONSTANTS
WINDOWHEIGHT = 625
WINDOWWIDTH = 500
HEADERHEIGHT = 125
TILESIZE = 100
GAPSIZE = 20
BOARDHEIGHT = BOARDWIDTH = 4
HBBHEIGHT = 42
HBBWIDTH = 165


#COLORS      R    G    B
FUCHSIA  = (255,   0, 255) #2
RED      = (255,   0,   0) #4
GREEN    = (  0, 128,   0) #8
BLUE     = (  0,   0, 255) #16
PURPLE   = (128,   0, 128) #32
OLIVE    = (128, 128,   0) #64
NAVYBLUE = (  0,   0, 128) #128
LIME     = (  0, 255,   0) #256
TEAL     = (  0, 128, 128) #512
ORANGE   = (252, 128,   0) #1024
YELLOW   = (255, 255,   0) #2048
BLACK    = (  0,   0,   0) #text
WHITE    = (255, 255, 255) #event text
SILVER   = (192, 192, 192) #empty tile space color

BGCOLOR  = (164, 152, 128)
EMPTYTILECOLOR = SILVER 

#DIRECTIONS
UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'


#TILES              VALUE   COLOR   MTT
TWO              = [   2, FUCHSIA, False]
FOUR             = [   4,     RED, False]
EIGHT            = [   8,   GREEN, False]
SIXTEEN          = [  16,    BLUE, False]
THIRTYTWO        = [  32,  PURPLE, False]
SIXTYFOUR        = [  64,   OLIVE, False]
ONETWOEIGHT      = [ 128,NAVYBLUE, False]
TWOFIVESIX       = [ 256,    LIME, False]
FIVEONETWO       = [ 512,    TEAL, False]
TENTWENTYFOUR    = [1024,  ORANGE, False]
TWENTYFORTYEIGHT = [2048,  YELLOW, False]

ALLTILES = (TWO, FOUR, EIGHT, SIXTEEN, THIRTYTWO, SIXTYFOUR, ONETWOEIGHT, TWOFIVESIX, FIVEONETWO, TENTWENTYFOUR, TWENTYFORTYEIGHT)


def main(highscore):
    global DISPLAYSURF, tilefont, tilefont2, hbbfont, eventfont, eventfont2
    pygame.init()
    
    #Prepare Font
    tilefont = pygame.font.Font('freesansbold.ttf', 69)
    tilefont2 = pygame.font.Font('freesansbold.ttf', 42)
    hbbfont = pygame.font.Font('freesansbold.ttf', 20)
    eventfont = pygame.font.Font('freesansbold.ttf', 60)
    eventfont2 = pygame.font.Font('freesansbold.ttf', 19)
    #Prepare Window
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('2048')
    #Prepare Board Structure
    header, mainBoard = getStartBoard()
    #Set HighScore
    header[2] = highscore
      
    #Main Game Loop
    while True:
       DISPLAYSURF.fill(BGCOLOR)
       drawHeader(header)
       drawBoard(mainBoard)
       
       #Event Handler
       for event in pygame.event.get():
           
           if (event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE)):
               pygame.quit()
               sys.exit()
               
           elif event.type == MOUSEBUTTONUP:
               
                   mouse_pos = pygame.mouse.get_pos()
                   if (header[0].collidepoint(mouse_pos)): #New Game
                       main(header[2])
                    
           elif event.type == KEYUP and event.key == K_UP:
               move(header, mainBoard, UP)
           elif event.type == KEYUP and event.key == K_DOWN:
               move(header, mainBoard, DOWN)
           elif event.type == KEYUP and event.key == K_RIGHT:
               move(header, mainBoard, RIGHT)
           elif event.type == KEYUP and event.key == K_LEFT:
               move(header, mainBoard, LEFT)
           
       pygame.display.update()


def getStartBoard():
   #Header         # New Game         # Score    # Best Score           
    header = [pygame.Rect(0, 0, 0, 0),      0,              0]
                 

    #Board Tiles
    tiles = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(None)
        tiles.append(column)
       
    #Generate Start Tiles
    r1 = random.randrange(4)
    r2 = random.randrange(4)  
    tiles[r1][r2] = ALLTILES[random.randrange(2)][:]

    r3 = random.randrange(4)
    r4 = random.randrange(4)
    while r3 == r1 and r4 == r2: #Prevents Start Tiles From Being Placed In The Same Location
        r3 = random.randrange(4)
        r4 = random.randrange(4)
    tiles[r3][r4] = ALLTILES[random.randrange(2)][:]
    

    random.shuffle(tiles)
    return (header, tiles)


def getLeftTopCoords(x, y): # Converts List Coords To Pixel Coords
    left = x * (TILESIZE + GAPSIZE) + GAPSIZE
    top  = y * (TILESIZE + GAPSIZE) + GAPSIZE + HEADERHEIGHT

    return (left, top)
    
    
def drawHeader(header):
    
    # Draw "New Game" Button 
    textSurf = hbbfont.render("New Game", True, BLACK)
    header[0] = textSurf.get_rect() 
    header[0].topleft = (0, GAPSIZE)
    header[0].center = (HBBWIDTH/2, HEADERHEIGHT/3+(HBBHEIGHT/2)) 
    DISPLAYSURF.blit(textSurf, header[0])

    #Draw Score Counter
    textSurf = hbbfont.render("Score: " + str(header[1]), True, BLACK) 
    textSurfRect = textSurf.get_rect()
    textSurfRect.topleft = (HBBWIDTH, HEADERHEIGHT/3)
    textSurfRect.center = (HBBWIDTH+(HBBWIDTH/2), HEADERHEIGHT/3+(HBBHEIGHT/2)) 
    DISPLAYSURF.blit(textSurf, textSurfRect)

    #Draw Best Score Counter
    textSurf = hbbfont.render("Best Score: " + str(header[2]), True, BLACK) 
    textSurfRect = textSurf.get_rect()
    textSurfRect.topleft = ((HBBWIDTH*2), HEADERHEIGHT/3)
    textSurfRect.center = ((HBBWIDTH*2)+(HBBWIDTH/2), HEADERHEIGHT/3+(HBBHEIGHT/2)) 
    DISPLAYSURF.blit(textSurf, textSurfRect)

    
def drawBoard(board):
    
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            left, top = getLeftTopCoords(tilex, tiley)
            if board[tilex][tiley] == None: #Tile Is Empty. Draw Empty Tile Space.
                pygame.draw.rect(DISPLAYSURF, EMPTYTILECOLOR, (left, top, TILESIZE, TILESIZE))
            else: # Draw The Tile
                pygame.draw.rect(DISPLAYSURF, board[tilex][tiley][1], (left, top, TILESIZE, TILESIZE)) #The Color Of Each Tile Is In Location 1 
                if board[tilex][tiley][0] <= 64:
                 textSurf = tilefont.render(str(board[tilex][tiley][0]), True, BLACK) # The Value Of Each Tile Is In Location 0 
                else:
                 textSurf = tilefont2.render(str(board[tilex][tiley][0]), True, BLACK)   
                textSurfRect = textSurf.get_rect()
                textSurfRect.topleft = (left, top)
                textSurfRect.center = (left+(TILESIZE/2), top+(TILESIZE/2)) 
                DISPLAYSURF.blit(textSurf, textSurfRect)


def gameOverCheck(header,board,direction):
    m=False
    for x in range(BOARDWIDTH): 
            for y in range(BOARDHEIGHT): 
                if board[x][y]!=None:
                            board[x][y][2]=False                
    if direction == UP: 
        
        for x in range(BOARDWIDTH): #0 , 1 , 2 , 3 
            for y in range(1, BOARDHEIGHT): # 1, 2, 3
                
                if y == 1:
                   if board[x][y] != None: #There Is A Tile In The Space
                       if board[x][0] == None:
                           board[x][0] = board[x][y]
                           board[x][y] = None
                           m = True
                       elif board[x][y][0] == board[x][0][0] and board[x][0][2] == False: #If The Tiles Have The Same Value And The End Tile Was Not Merged This Turn
                           header, board, board[x][y], board[x][0] = merge(header, board, board[x][y], board[x][0])
                           
                           if board[x][0] == TWENTYFORTYEIGHT:
                               youWin(header, board)
                           m = True
                     
                           
                elif y == 2:
                   if board[x][y] != None: 
                       if board[x][1] == None:
                           if board[x][0] == None:
                            board[x][0] = board[x][y]
                            board[x][y] = None
                            m = True
                            
                           elif board[x][y][0] == board[x][0][0] and board[x][0][2] == False:
                               header, board, board[x][y], board[x][0] = merge(header, board, board[x][y], board[x][0])
                               if board[x][0] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True                              
                               
                           else:
                               board[x][1] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[x][1][0] and (board[x][1][2] == False): 
                               header, board, board[x][y], board[x][1] = merge(header, board, board[x][y], board[x][1])
                               if board[x][1] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True
                       
                elif y == 3:
                   if board[x][y] != None: 
                       if board[x][2] == None:
                           if board[x][1] == None:
                               if board[x][0] == None:
                                   board[x][0] = board[x][y]
                                   board[x][y] = None
                                   m = True
                               elif board[x][y][0] == board[x][0][0] and (board[x][0][2] == False):
                                   header, board, board[x][y], board[x][0] = merge(header, board, board[x][y], board[x][0])
                                   if board[x][0] == TWENTYFORTYEIGHT:
                                     youWin(header, board)
                                   m = True 
                               else:
                                   board[x][1] = board[x][y]
                                   board[x][y] = None
                                   m = True
                           elif board[x][y][0] == board[x][1][0] and (board[x][1][2] == False):
                               header, board, board[x][y], board[x][1] = merge(header, board, board[x][y], board[x][1])
                               if board[x][1] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                           else:
                               board[x][2] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[x][2][0] and (board[x][2][2] == False):
                               header, board, board[x][y], board[x][2] = merge(header, board, board[x][y], board[x][2])
                               if board[x][2] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 

    if direction == DOWN:
        
        for x in range(BOARDWIDTH): #0 , 1 , 2 , 3 
            for y in range(BOARDHEIGHT-2, -1, -1): #2, 1, 0
              
                if y == 2:
                   if board[x][y] != None: 
                       if board[x][3] == None:
                           board[x][3] = board[x][y]
                           board[x][y] = None
                           m = True
                       elif board[x][y][0] == board[x][3][0] and (board[x][3][2] == False): 
                           header, board, board[x][y], board[x][3] = merge(header, board, board[x][y], board[x][3])
                           if board[x][3] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                           m = True
                elif y == 1:
                   if board[x][y] != None: 
                       if board[x][2] == None:
                           if board[x][3] == None:
                            board[x][3] = board[x][y]
                            board[x][y] = None
                            m = True
                           elif board[x][y][0] == board[x][3][0] and (board[x][3][2] == False):
                               header, board, board[x][y], board[x][3] = merge(header, board, board[x][y], board[x][3])
                               if board[x][3] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                           else:
                               board[x][2] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[x][2][0] and (board[x][2][2] == False): 
                               header, board, board[x][y], board[x][2] = merge(header, board, board[x][y], board[x][2])
                               if board[x][2] == TWENTYFORTYEIGHT:
                                 youWin(header ,board)
                               m = True 
                       
                elif y == 0:
                   if board[x][y] != None: 
                       if board[x][1] == None:
                           if board[x][2] == None:
                               if board[x][3] == None:
                                   board[x][3] = board[x][y]
                                   board[x][y] = None
                                   m = True
                               elif board[x][y][0] == board[x][3][0] and (board[x][3][2] == False):
                                   header, board, board[x][y], board[x][3] = merge(header, board, board[x][y], board[x][3])
                                   if board[x][3] == TWENTYFORTYEIGHT:
                                     youWin(header, board)
                                   m = True 
                               else:
                                   board[x][2] = board[x][y]
                                   board[x][y] = None
                                   m = True
                           elif board[x][y][0] == board[x][2][0] and (board[x][2][2] == False):
                               header, board, board[x][y], board[x][2] = merge(header, board, board[x][y], board[x][2])
                               if board[x][2] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                           else:
                               board[x][1] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[x][1][0] and (board[x][1][2] == False):
                               header, board, board[x][y], board[x][1] = merge(header, board, board[x][y], board[x][1])
                               if board[x][1] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                               
    if direction == RIGHT: 
        
        for y in range(BOARDHEIGHT): #0 , 1 , 2 , 3 
            for x in range(BOARDWIDTH-2, -1, -1): #2, 1, 0
               
                if x == 2:
                   if board[x][y] != None:
                       if board[3][y] == None:
                           board[3][y] = board[x][y]
                           board[x][y] = None
                           m = True
                       elif board[x][y][0] == board[3][y][0] and (board[3][y][2] == False):
                           header, board, board[x][y], board[3][y] = merge(header, board, board[x][y], board[3][y])
                           if board[3][y] == TWENTYFORTYEIGHT:
                               youWin(header, board)
                           m = True
                elif x == 1:
                   if board[x][y] != None: 
                       if board[2][y] == None:
                           if board[3][y] == None:
                            board[3][y] = board[x][y]
                            board[x][y] = None
                            m = True
                           elif board[x][y][0] == board[3][y][0] and (board[3][y][2] == False):
                               header, board, board[x][y], board[3][y] = merge(header, board, board[x][y], board[3][y])
                               if board[3][y] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                           else:
                               board[2][y] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[2][y][0] and (board[2][y][2] == False): 
                               header, board, board[x][y], board[2][y] = merge(header, board, board[x][y], board[2][y])
                               if board[2][y] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                       
                elif x == 0:
                   if board[x][y] != None: 
                       if board[1][y] == None:
                           if board[2][y] == None:
                               if board[3][y] == None:
                                   board[3][y] = board[x][y]
                                   board[x][y] = None
                                   m = True
                               elif board[x][y][0] == board[3][y][0] and (board[3][y][2] == False):
                                   header, board, board[x][y], board[3][y] = merge(header, board, board[x][y], board[3][y])
                                   if board[3][y] == TWENTYFORTYEIGHT:
                                      youWin(header, board)
                                   m = True 
                               else:
                                   board[2][y] = board[x][y]
                                   board[x][y] = None
                                   m = True
                           elif board[x][y][0] == board[2][y][0] and (board[2][y][2] == False):
                               header, board, board[x][y], board[2][y] = merge(header, board, board[x][y], board[2][y])
                               if board[2][y] == TWENTYFORTYEIGHT:
                                  youWin(header, board)
                               m = True 
                           else:
                               board[1][y] = board[x][y]
                               board[x][y] = None
                               m=True
                       elif board[x][y][0] == board[1][y][0] and (board[1][y][2] == False):
                               header, board, board[x][y], board[1][y] = merge(header, board, board[x][y], board[1][y])
                               if board[1][y] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                                
    if direction == LEFT: 
        
        for y in range(BOARDHEIGHT): #0 , 1 , 2 , 3 
            for x in range(1, BOARDWIDTH):#1 , 2 , 3
               
                if x == 1:
                   if board[x][y] != None: 
                       if board[0][y] == None:
                           board[0][y] = board[x][y]
                           board[x][y] = None
                           m = True
                       elif board[x][y][0] == board[0][y][0] and (board[0][y][2] == False): 
                           header, board, board[x][y], board[0][y] = merge(header,board,board[x][y],board[0][y])
                           if board[0][y] == TWENTYFORTYEIGHT:
                               youWin(header,board)
                           m = True 
                elif x == 2:
                   if board[x][y] != None: 
                       if board[1][y] == None:
                           if board[0][y] == None:
                            board[0][y] = board[x][y]
                            board[x][y] = None
                            m = True
                           elif board[x][y][0] == board[0][y][0] and (board[0][y][2] == False):
                               header, board, board[x][y], board[0][y] = merge(header, board, board[x][y], board[0][y])
                               if board[0][y]==TWENTYFORTYEIGHT:
                                  youWin(header, board)
                               m = True 
                           else:
                               board[1][y] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[1][y][0] and (board[1][y][2] == False): 
                               header, board, board[x][y], board[1][y] = merge(header, board, board[x][y], board[1][y])
                               if board[1][y] == TWENTYFORTYEIGHT:
                                  youWin(header, board)
                               m = True 
                       
                elif x == 3:
                   if board[x][y] != None: 
                       if board[2][y] == None:
                           if board[1][y] == None:
                               if board[0][y] == None:
                                   board[0][y] = board[x][y]
                                   board[x][y] = None
                                   m = True
                               elif board[x][y][0] == board[0][y][0] and (board[0][y][2] == False):
                                   header, board, board[x][y], board[0][y] = merge(header, board, board[x][y], board[0][y])
                                   if board[0][y] == TWENTYFORTYEIGHT:
                                     youWin(header, board)
                                   m = True 
                               else:
                                   board[1][y] = board[x][y]
                                   board[x][y] = None
                                   m = True
                           elif board[x][y][0] == board[1][y][0] and (board[1][y][2] == False):
                               header, board, board[x][y], board[1][y] = merge(header, board, board[x][y], board[1][y])
                               if board[1][y] == TWENTYFORTYEIGHT:
                                  youWin(header, board)
                               m = True 
                           else:
                               board[2][y] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[2][y][0] and (board[2][y][2] == False):
                               header, board, board[x][y], board[2][y] = merge(header, board, board[x][y], board[2][y])
                               if board[2][y] == TWENTYFORTYEIGHT:
                                  youWin(header, board)
                               m = True
 
    return m                            



def move(header, board, direction):
    #*n = 0
    m = False
    for x in range(BOARDWIDTH): 
            for y in range(BOARDHEIGHT): 
                if board[x][y] != None:
                            board[x][y][2] = False
    #*print("")
    #*for x in range(BOARDWIDTH): 
    #*  for y in range(BOARDHEIGHT): 
    #*      if board[x][y] != None:
    #*          print("board[" + str(x) + "][" + str(y) + "] = " + str(board[x][y][2]))
                    
                            
    if direction == UP: 
        
        for x in range(BOARDWIDTH): #0 , 1 , 2 , 3 
            for y in range(1, BOARDHEIGHT): # 1, 2, 3
                
                if y == 1:
                   if board[x][y] != None: #There Is A Tile In The Space
                       if board[x][0] == None:
                           board[x][0] = board[x][y]
                           board[x][y] = None
                           m = True
                       elif board[x][y][0] == board[x][0][0] and board[x][0][2] == False: #If The Tiles Have The Same Value And The End Tile Was Not Merged This Turn
                           header, board, board[x][y], board[x][0] = merge(header, board, board[x][y], board[x][0])
                           #*n+=1
                           #*print("\n"+"merged",n," = ",board[x][0][0])
                           
                           if board[x][0] == TWENTYFORTYEIGHT:
                               youWin(header, board)
                           m = True
                     
                           
                elif y == 2:
                   if board[x][y] != None: 
                       if board[x][1] == None:
                           if board[x][0] == None:
                            board[x][0] = board[x][y]
                            board[x][y] = None
                            m = True
                            
                           elif board[x][y][0] == board[x][0][0] and board[x][0][2] == False:
                               header, board, board[x][y], board[x][0] = merge(header, board, board[x][y], board[x][0])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[x][0][0])
                               if board[x][0] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True                              
                               
                           else:
                               board[x][1] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[x][1][0] and (board[x][1][2] == False): 
                               header, board, board[x][y], board[x][1] = merge(header, board, board[x][y], board[x][1])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[x][1][0])
                               if board[x][1] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True
                       
                elif y == 3:
                   if board[x][y] != None: 
                       if board[x][2] == None:
                           if board[x][1] == None:
                               if board[x][0] == None:
                                   board[x][0] = board[x][y]
                                   board[x][y] = None
                                   m = True
                               elif board[x][y][0] == board[x][0][0] and (board[x][0][2] == False):
                                   header, board, board[x][y], board[x][0] = merge(header, board, board[x][y], board[x][0])
                                   #*n+=1
                                   #*print("\n"+"merged",n," = ",board[x][0][0])
                                   if board[x][0] == TWENTYFORTYEIGHT:
                                     youWin(header, board)
                                   m = True 
                               else:
                                   board[x][1] = board[x][y]
                                   board[x][y] = None
                                   m = True
                           elif board[x][y][0] == board[x][1][0] and (board[x][1][2] == False):
                               header, board, board[x][y], board[x][1] = merge(header, board, board[x][y], board[x][1])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[x][1][0])
                               if board[x][1] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                           else:
                               board[x][2] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[x][2][0] and (board[x][2][2] == False):
                               header, board, board[x][y], board[x][2] = merge(header, board, board[x][y], board[x][2])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[x][2][0])
                               if board[x][2] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 

    if direction == DOWN:
        
        for x in range(BOARDWIDTH): #0 , 1 , 2 , 3 
            for y in range(BOARDHEIGHT-2, -1, -1): #2, 1, 0
              
                if y == 2:
                   if board[x][y] != None: 
                       if board[x][3] == None:
                           board[x][3] = board[x][y]
                           board[x][y] = None
                           m = True
                       elif board[x][y][0] == board[x][3][0] and (board[x][3][2] == False): 
                           header, board, board[x][y], board[x][3] = merge(header, board, board[x][y], board[x][3])
                           #*n+=1
                           #*print("\n"+"merged",n," = ",board[x][3][0])
                           if board[x][3] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                           m = True
                elif y == 1:
                   if board[x][y] != None: 
                       if board[x][2] == None:
                           if board[x][3] == None:
                            board[x][3] = board[x][y]
                            board[x][y] = None
                            m = True
                           elif board[x][y][0] == board[x][3][0] and (board[x][3][2] == False):
                               header, board, board[x][y], board[x][3] = merge(header, board, board[x][y], board[x][3])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[x][3][0])
                               if board[x][3] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                           else:
                               board[x][2] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[x][2][0] and (board[x][2][2] == False): 
                               header, board, board[x][y], board[x][2] = merge(header, board, board[x][y], board[x][2])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[x][2][0])
                               if board[x][2] == TWENTYFORTYEIGHT:
                                 youWin(header ,board)
                               m = True 
                       
                elif y == 0:
                   if board[x][y] != None: 
                       if board[x][1] == None:
                           if board[x][2] == None:
                               if board[x][3] == None:
                                   board[x][3] = board[x][y]
                                   board[x][y] = None
                                   m = True
                               elif board[x][y][0] == board[x][3][0] and (board[x][3][2] == False):
                                   header, board, board[x][y], board[x][3] = merge(header, board, board[x][y], board[x][3])
                                   #*n+=1
                                   #*print("\n"+"merged",n," = ",board[x][3][0])
                                   if board[x][3] == TWENTYFORTYEIGHT:
                                     youWin(header, board)
                                   m = True 
                               else:
                                   board[x][2] = board[x][y]
                                   board[x][y] = None
                                   m = True
                           elif board[x][y][0] == board[x][2][0] and (board[x][2][2] == False):
                               header, board, board[x][y], board[x][2] = merge(header, board, board[x][y], board[x][2])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[x][2][0])
                               if board[x][2] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                           else:
                               board[x][1] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[x][1][0] and (board[x][1][2] == False):
                               header, board, board[x][y], board[x][1] = merge(header, board, board[x][y], board[x][1])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[x][1][0])
                               if board[x][1] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                               
    if direction == RIGHT: 
        
        for y in range(BOARDHEIGHT): #0 , 1 , 2 , 3 
            for x in range(BOARDWIDTH-2, -1, -1): #2, 1, 0
               
                if x == 2:
                   if board[x][y] != None:
                       if board[3][y] == None:
                           board[3][y] = board[x][y]
                           board[x][y] = None
                           m = True
                       elif board[x][y][0] == board[3][y][0] and (board[3][y][2] == False):
                           header, board, board[x][y], board[3][y] = merge(header, board, board[x][y], board[3][y])
                           #*n+=1
                           #*print("\n"+"merged",n," = ",board[3][y][0])
                           if board[3][y] == TWENTYFORTYEIGHT:
                               youWin(header, board)
                           m = True
                elif x == 1:
                   if board[x][y] != None: 
                       if board[2][y] == None:
                           if board[3][y] == None:
                            board[3][y] = board[x][y]
                            board[x][y] = None
                            m = True
                           elif board[x][y][0] == board[3][y][0] and (board[3][y][2] == False):
                               header, board, board[x][y], board[3][y] = merge(header, board, board[x][y], board[3][y])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[3][y][0])
                               if board[3][y] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                           else:
                               board[2][y] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[2][y][0] and (board[2][y][2] == False): 
                               header, board, board[x][y], board[2][y] = merge(header, board, board[x][y], board[2][y])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[2][y][0])
                               if board[2][y] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                       
                elif x == 0:
                   if board[x][y] != None: 
                       if board[1][y] == None:
                           if board[2][y] == None:
                               if board[3][y] == None:
                                   board[3][y] = board[x][y]
                                   board[x][y] = None
                                   m = True
                               elif board[x][y][0] == board[3][y][0] and (board[3][y][2] == False):
                                   header, board, board[x][y], board[3][y] = merge(header, board, board[x][y], board[3][y])
                                   #*n+=1
                                   #*print("\n"+"merged",n," = ",board[3][y][0])
                                   if board[3][y] == TWENTYFORTYEIGHT:
                                      youWin(header, board)
                                   m = True 
                               else:
                                   board[2][y] = board[x][y]
                                   board[x][y] = None
                                   m = True
                           elif board[x][y][0] == board[2][y][0] and (board[2][y][2] == False):
                               header, board, board[x][y], board[2][y] = merge(header, board, board[x][y], board[2][y])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[2][y][0])
                               if board[2][y] == TWENTYFORTYEIGHT:
                                  youWin(header, board)
                               m = True 
                           else:
                               board[1][y] = board[x][y]
                               board[x][y] = None
                               m=True
                       elif board[x][y][0] == board[1][y][0] and (board[1][y][2] == False):
                               header, board, board[x][y], board[1][y] = merge(header, board, board[x][y], board[1][y])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[1][y][0])
                               if board[1][y] == TWENTYFORTYEIGHT:
                                 youWin(header, board)
                               m = True 
                                
    if direction == LEFT: 
        
        for y in range(BOARDHEIGHT): #0 , 1 , 2 , 3 
            for x in range(1, BOARDWIDTH):#1 , 2 , 3
               
                if x == 1:
                   if board[x][y] != None: 
                       if board[0][y] == None:
                           board[0][y] = board[x][y]
                           board[x][y] = None
                           m = True
                       elif board[x][y][0] == board[0][y][0] and (board[0][y][2] == False): 
                           header, board, board[x][y], board[0][y] = merge(header,board,board[x][y],board[0][y])
                           #*n+=1
                           #*print("\n"+"merged",n," = ",board[0][y][0])
                           if board[0][y] == TWENTYFORTYEIGHT:
                               youWin(header,board)
                           m = True 
                elif x == 2:
                   if board[x][y] != None: 
                       if board[1][y] == None:
                           if board[0][y] == None:
                            board[0][y] = board[x][y]
                            board[x][y] = None
                            m = True
                           elif board[x][y][0] == board[0][y][0] and (board[0][y][2] == False):
                               header, board, board[x][y], board[0][y] = merge(header, board, board[x][y], board[0][y])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[0][y][0])
                               if board[0][y]==TWENTYFORTYEIGHT:
                                  youWin(header, board)
                               m = True 
                           else:
                               board[1][y] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[1][y][0] and (board[1][y][2] == False): 
                               header, board, board[x][y], board[1][y] = merge(header, board, board[x][y], board[1][y])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[1][y][0])
                               if board[1][y] == TWENTYFORTYEIGHT:
                                  youWin(header, board)
                               m = True 
                       
                elif x == 3:
                   if board[x][y] != None: 
                       if board[2][y] == None:
                           if board[1][y] == None:
                               if board[0][y] == None:
                                   board[0][y] = board[x][y]
                                   board[x][y] = None
                                   m = True
                               elif board[x][y][0] == board[0][y][0] and (board[0][y][2] == False):
                                   header, board, board[x][y], board[0][y] = merge(header, board, board[x][y], board[0][y])
                                   #*n+=1
                                   #*print("\n"+"merged",n," = ",board[0][y][0])
                                   if board[0][y] == TWENTYFORTYEIGHT:
                                     youWin(header, board)
                                   m = True 
                               else:
                                   board[1][y] = board[x][y]
                                   board[x][y] = None
                                   m = True
                           elif board[x][y][0] == board[1][y][0] and (board[1][y][2] == False):
                               header, board, board[x][y], board[1][y] = merge(header, board, board[x][y], board[1][y])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[1][y][0])
                               if board[1][y] == TWENTYFORTYEIGHT:
                                  youWin(header, board)
                               m = True 
                           else:
                               board[2][y] = board[x][y]
                               board[x][y] = None
                               m = True
                       elif board[x][y][0] == board[2][y][0] and (board[2][y][2] == False):
                               header, board, board[x][y], board[2][y] = merge(header, board, board[x][y], board[2][y])
                               #*n+=1
                               #*print("\n"+"merged",n," = ",board[2][y][0])
                               if board[2][y] == TWENTYFORTYEIGHT:
                                  youWin(header, board)
                               m = True
    #*print("")
    #*for x in range(BOARDWIDTH): 
    #*        for y in range(BOARDHEIGHT): 
    #*            if board[x][y] != None:
    #*                print("board[" + str(x) + "][" + str(y) + "] = " + str(board[x][y][2]))
    #*print("--------------------")
    if m == True:
        newTile(board)
    none = 0 # For Counting Empty Spaces Left On The Board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == None:
                none+=1 # Increments For Each Empty Tile Space Left
    if none == 0: #If No Empty Tile Space, Check For Game Over
        h_sub = header[:]
        b_sub = board[:]
        if gameOverCheck(h_sub, b_sub, UP) == gameOverCheck(h_sub, b_sub, DOWN) == gameOverCheck(h_sub, b_sub, RIGHT) == gameOverCheck(h_sub, b_sub, LEFT) == False:
            gameOver(header, board)
            
                

                
def merge(header, board, sourcetile, endtile):
    if sourcetile[0] == 2:
        
        endtile = FOUR[:]
        sourcetile = None
        
        header[1]+=endtile[0] 
    
        if header[1] > header[2]: 
           header[2] = header[1]  
           
        endtile[2] = True #Was Merged This Turn
        
    elif sourcetile[0] == 4:
        
        endtile = EIGHT[:]
        sourcetile = None
        
        header[1]+=endtile[0] 
    
        if header[1] > header[2]: 
           header[2] = header[1]  
           
        endtile[2] = True 
        
    elif sourcetile[0] == 8:
        
        endtile = SIXTEEN[:]
        sourcetile = None
        
        header[1]+=endtile[0] 
    
        if header[1] > header[2]: 
           header[2] = header[1]  
           
        endtile[2] = True 
       
    elif sourcetile[0] == 16:

        endtile = THIRTYTWO[:]
        sourcetile = None

        header[1]+=endtile[0] 
    
        if header[1] > header[2]: 
           header[2] = header[1]  
           
        endtile[2] = True 

    elif sourcetile[0] == 32:

        endtile = SIXTYFOUR[:]
        sourcetile = None
        
        header[1]+=endtile[0] 
    
        if header[1] > header[2]: 
           header[2] = header[1]  
           
        endtile[2] = True 

    elif sourcetile[0] == 64:

        endtile = ONETWOEIGHT[:]
        sourcetile = None

        header[1]+=endtile[0] 
    
        if header[1] > header[2]: 
           header[2] = header[1]  
           
        endtile[2] = True 


    elif sourcetile[0] == 128:

        endtile = TWOFIVESIX[:]
        sourcetile = None

        header[1]+=endtile[0] 
    
        if header[1] > header[2]: 
           header[2] = header[1]  
           
        endtile[2] = True 


    elif sourcetile[0] == 256:

        endtile = FIVEONETWO[:]
        sourcetile = None

        header[1]+=endtile[0] 
    
        if header[1] > header[2]: 
           header[2] = header[1]  
           
        endtile[2] = True 


    elif sourcetile[0] == 512:

        endtile = TENTWENTYFOUR[:]
        sourcetile = None

        header[1]+=endtile[0] 
    
        if header[1] > header[2]: 
           header[2] = header[1]  
           
        endtile[2] = True 


    elif sourcetile[0] == 1024:

        endtile = TWENTYFORTYEIGHT[:]
        sourcetile = None

        header[1]+=endtile[0] 
    
        if header[1] > header[2]: 
           header[2] = header[1]  
           
        endtile[2] = True 

           
    return (header, board, sourcetile, endtile)  


def youWin(header, board):
    
    DISPLAYSURF.fill(BGCOLOR)
    drawHeader(header)
    drawBoard(board)
    
    textSurf = eventfont.render("YOU WIN!", True, WHITE)
    textSurfRect = textSurf.get_rect()
    textSurfRect.topleft = (WINDOWWIDTH, WINDOWHEIGHT/2)
    textSurfRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/3) 
    DISPLAYSURF.blit(textSurf, textSurfRect)
    
    textSurf = eventfont2.render("YOU SIR/MA ARE HIGHLY FAVOURED AMONG MEN!", True, WHITE) 
    textSurfRect = textSurf.get_rect()
    textSurfRect.topleft = (WINDOWWIDTH, WINDOWHEIGHT)
    textSurfRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2) 
    DISPLAYSURF.blit(textSurf, textSurfRect)
    pygame.display.update()
    
    sys.exit()

def gameOver(header, mainBoard):
    
    
    while True: #Main Game-Over Loop
       
      
       DISPLAYSURF.fill(BGCOLOR)
       drawHeader(header)
       drawBoard(mainBoard)
       
       textSurf = eventfont.render("GAME OVER!", True, WHITE)
       textSurfRect = textSurf.get_rect()
       textSurfRect.topleft = (WINDOWWIDTH, WINDOWHEIGHT/2)
       textSurfRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/3) 
       DISPLAYSURF.blit(textSurf, textSurfRect)
       
       #Event Handler
       for event in pygame.event.get():
           
           if (event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE)):
               pygame.quit()
               sys.exit()
               
           elif event.type == MOUSEBUTTONUP:
               
                   mouse_pos = pygame.mouse.get_pos()
                   if (header[0].collidepoint(mouse_pos)): #New Game
                       main(header[2])
                    
           elif event.type == KEYUP and event.key == K_UP:
               move(header, mainBoard, UP)
           elif event.type == KEYUP and event.key == K_DOWN:
               move(header, mainBoard, DOWN)
           elif event.type == KEYUP and event.key == K_RIGHT:
               move(header, mainBoard, RIGHT)
           elif event.type == KEYUP and event.key == K_LEFT:
               move(header, mainBoard, LEFT)
           
       pygame.display.update()


def newTile(board):
    i = 0
    while i != 1:
            r1 = random.randrange(4)
            r2 = random.randrange(4)
            if (board[r1][r2] == None) and (i != 1):
               board[r1][r2] = ALLTILES[random.randrange(2)][:]
               i = 1
    
    
                
if __name__ == '__main__':
    main(0)

