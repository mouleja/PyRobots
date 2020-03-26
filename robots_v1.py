import pygame, sys, random
from pygame.locals import *

WINDOWWIDTH = 1000
WINDOWHEIGHT = 800
xSpaces = 40
ySpaces = 30
xSize = 20
ySize = 20
xBorder = int(WINDOWWIDTH - xSpaces * xSize)/2
yBorder = int(WINDOWHEIGHT - ySpaces * ySize)/2
FPS = 30
gridColor = (0, 0, 0)
bgColor = (255,255,255)
initRobots = 20
perLevelAdd = 10
ROBOT_IMG = pygame.image.load('Robot1.png')
CRASH_IMG = pygame.image.load('Crash.png')
PLAYER_IMG = pygame.image.load('Player.png')
ROBOT_IMG = pygame.transform.scale(ROBOT_IMG, (xSize-2, ySize-2))
CRASH_IMG = pygame.transform.scale(CRASH_IMG, (xSize-2, ySize-2))
PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (xSize-2, ySize-2))

def main():
    global DISPLAYSURF

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Robots')

    startScreen()

    level = 0
    score = 0
    showGrid = False
    currentState = drawLevel(populateLevel(level),showGrid)
    drawScore(score,level)
    
    while True: # main game loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit(0)

            elif event.type == KEYUP:
                if event.key == K_q:
                    currentState,score = movePlayer(currentState,-1,-1,score)
                elif event.key == K_w:
                    currentState,score = movePlayer(currentState,0,-1,score)
                elif event.key == K_e:
                    currentState,score = movePlayer(currentState,1,-1,score)
                elif event.key == K_a:
                    currentState,score = movePlayer(currentState,-1,0,score)
                elif event.key == K_s:
                    currentState,score = movePlayer(currentState,0,0,score)
                elif event.key == K_d:
                    currentState,score = movePlayer(currentState,1,0,score)
                elif event.key == K_z:
                    currentState,score = movePlayer(currentState,-1,1,score)
                elif event.key == K_x:
                    currentState,score = movePlayer(currentState,0,1,score)
                elif event.key == K_c:
                    currentState,score = movePlayer(currentState,1,1,score)
                elif event.key == K_t:
                    currentState,score = teleport(currentState,score)
                elif event.key == K_g:
                    showGrid = not showGrid

                drawLevel(currentState,showGrid)
                drawScore(score,level)
                
                if checkLevel(currentState):
                    level += 1
                    currentState = drawLevel(populateLevel(level),showGrid)
                    drawScore(score,level)

def startScreen():
    startScreen = pygame.image.load('Start.png')
    startScreen = pygame.transform.scale(startScreen, (WINDOWWIDTH, WINDOWHEIGHT))
    startScreenRect = startScreen.get_rect()
    DISPLAYSURF.blit(startScreen,startScreenRect)
    pygame.display.update()
    while True: # check to start
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit(0)

            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    return

def drawScore(score,level):
    FONT = pygame.font.Font('freesansbold.ttf', 12)
    scoreSurf = FONT.render("Level: " + str(level) + "  Score: " + str(score),True, gridColor)
    scoreSurfRect = scoreSurf.get_rect()
    scoreSurfRect.topleft = (xBorder, 2)
    DISPLAYSURF.blit(scoreSurf,scoreSurfRect)
    pygame.display.update()

def teleport(currentState,score):
    px, py = getPlayerPos(currentState)
    empty = False
    while empty == False:
        newX = random.randint(0, xSpaces - 1)
        newY = random.randint(0, ySpaces - 1)
        if currentState[newX][newY] == '0': # space blank, okay to teleport
            currentState[px][py] = '0'
            currentState[newX][newY] = 'p'
            return currentState, score - 5
        
def checkLevel(currentState): # check if any robots remaining
    for i in range(xSpaces):
        for j in range(ySpaces):
            if currentState[i][j] == 'r':
                return False
    return True

def movePlayer(currentState,x,y,score):
    px,py = getPlayerPos(currentState) # player's position before move
    newX = px + x
    newY = py + y
    if newX < 0 or newX > xSpaces - 1 or newY < 0 or newY > ySpaces - 1: # attempted move beyond borders
        return currentState, score
    if currentState[newX][newY] in ('r','c'): # player crashes into robot or crashsite
        gameOver()

    newState = [] # create new playfield for robots to move & check collisions
    for i in range(xSpaces):
        newState.append(['0'] * ySpaces)
    newState[newX][newY] = 'p' # place player in the new playfield
    
    for i in range(xSpaces): # check currentState for crash sites
        for j in range(ySpaces):
            if currentState[i][j] == 'c': # transfer crash sites
                newState[i][j] = 'c'
                
    for i in range(xSpaces): # check currentState for robots
        for j in range(ySpaces):
            if currentState[i][j] == 'r': # move robot toward player
                moveX = 0
                moveY = 0
                if newX > i:
                    moveX = 1
                elif newX < i:
                    moveX = -1
                
                if newY > j:
                    moveY = 1
                elif newY < j:
                    moveY = -1

                dest = newState[i + moveX][j + moveY] # what is in robot's destination square
                if dest == 'p':
                    gameOver()
                elif dest == 'c': # robot crashes into crash site (and is eliminated)
                    score = score + 1
                elif dest == 'r': # robot crashes into another robot and creates new crash site
                    score = score + 1
                    newState[i + moveX][j + moveY] = 'c'
                elif dest == '0': # destination clear, robot moves there
                    newState[i + moveX][j + moveY] = 'r'
                    
    return newState,score # which is now the currentState

    
def gameOver():
    FONT = pygame.font.Font('freesansbold.ttf', 12)
    endText = FONT.render("Game Over! Press <Space> to play again, or <Esc> to end.", True, gridColor)
    endTextRect = endText.get_rect()
    endTextRect.topleft = (xBorder, 20)
    DISPLAYSURF.blit(endText, endTextRect)
    pygame.display.update()
    while True: # check end game loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit(0)
                sys.exit()

            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    main()

def getPlayerPos(currentState):
    for i in range(xSpaces):
        for j in range(ySpaces):
            if currentState[i][j] == 'p':
                px = i
                py = j
    return px, py

def populateLevel(level):
    currentState = []
    for i in range(xSpaces):
        currentState.append(['0'] * ySpaces)

    population = initRobots + perLevelAdd * level
    for p in range(population):
        empty = False
        while empty == False:
            x = random.randint(0,xSpaces-1)
            y = random.randint(0,ySpaces-1)
            if currentState[x][y] == '0':
                currentState[x][y] = 'r'
                empty = True
    empty = False
    while empty == False:
        x = random.randint(0,xSpaces-1)
        y = random.randint(0,ySpaces-1)
        if currentState[x][y] == '0':
            currentState[x][y] = 'p'
            empty = True
    return currentState

def drawLevel(currentState,showGrid):
    DISPLAYSURF.fill(bgColor)
    pygame.draw.rect(DISPLAYSURF, gridColor, (xBorder,yBorder,xSpaces*xSize,ySpaces*ySize),1)
    if showGrid:
        drawSquares()
    for i in range(xSpaces):
        currentX = xBorder + i * xSize
        for j in range(ySpaces):
            currentY = yBorder + j * ySize
            if currentState[i][j] == 'r': # draw the robots
                DISPLAYSURF.blit(ROBOT_IMG,pygame.Rect(currentX+1,currentY+1, xSize-2, ySize-2))
            if currentState[i][j] == 'p': # draw the player
                DISPLAYSURF.blit(PLAYER_IMG,pygame.Rect(currentX+1,currentY+1, xSize-2, ySize-2))
            if currentState[i][j] == 'c': # draw the crashes
                DISPLAYSURF.blit(CRASH_IMG,pygame.Rect(currentX+1,currentY+1, xSize-2, ySize-2))
            if currentState[i][j] == '0': # draw the blanks (for moved robots)
                DISPLAYSURF.fill(bgColor,(currentX+1,currentY+1, xSize-2, ySize-2))
    pygame.display.update()
    return currentState

def drawSquares():
    DISPLAYSURF.fill(bgColor)
    # print ("drawSquares called") # testing only
    for i in range(xSpaces):
        currentX = xBorder + i * xSize
        for j in range(ySpaces):
            currentY = yBorder + j * ySize
            pygame.draw.rect(DISPLAYSURF, gridColor, (currentX, currentY, xSize, ySize),1)
    pygame.display.update()
            #pygame.time.Clock().tick(10)

if __name__ == '__main__':
    main()
