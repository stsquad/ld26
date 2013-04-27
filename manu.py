import pygame
from pygame.locals import *
import random
import math
from globs import *
from polylib import *
from mazegen import makeMaze

class Player:
    def __init__(self):
        self.x = 32*4
        self.y = 32*4
        self.rot = 0

def init():
    global screen, clock, maze, shipPoly, player, speed, trailsBitmap, trailsX, trailsY, miniMap
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Turning circle')
    clock = pygame.time.Clock()
    maze = [0]*64
    for i in range(0,64): maze[i] = [0]*64
    random.seed(2013)
    createMaze(maze)
    shipPoly = [ (0,2), (2,-2), (0,-1), (-2,-2), (0,2) ]
    shipPoly = polyScale(shipPoly, 8)
    shipPoly = polyRotate(shipPoly, -math.pi/2 ) # Adjust so it faces to 0 radians
    player = Player()
    trailsBitmap = pygame.Surface((640,480))
    trailsBitmap.fill((0,0,0))
    speed = 3
    trailsX = 0
    trailsY = 0
    miniMap = pygame.Surface((64,64))
    drawMiniMap(miniMap, maze)

def drawMiniMap(surface, maze):
    surface.fill((0,0,0))
    for x in range(0,64):
        for y in range(0,64):
            if(maze[x][y]==1): 
                surface.set_at((x,y),(127,127,0))
            elif(maze[x][y]==2): 
                surface.set_at((x,y),(255,0,255))

def playerReset():
    global player
    player = Player()

def createMaze(maze):
    for x in range(0,64):
        for y in range(0,64):
            maze[x][y] = 1

    makeMaze(maze, 1,1)
    for x in range(0,6):
        for y in range(0,4):
            maze[x][y] = 0
    saveSpots = 0
    tries = 0
    while(saveSpots < 100 and tries < 1000):
        x = random.randint(0,63)
        y = random.randint(0,63)
        if(maze[x][y] == 0):
            maze[x][y] = 2
            print "Save spot at %d,%d"%(x,y)
            saveSpots += 1
        tries += 1

def processKeys():
    keys = pygame.key.get_pressed()
    if(keys[K_LEFT]): player.rot -= 0.05
    if(keys[K_RIGHT]): player.rot += 0.05

def getMaze(x,y):
    if(x<0 or x>= GSX or y<0 or y>=GSY): return 1
    return maze[x][y]

def loop():
    global trailsX
    saveQueue = []
    saveDir = []
    while 1:
        clock.tick(50)
        screen.fill((127,127,127))
        offX = int(320-player.x) % 640
        w = 640-offX
        offY = int(-240+player.y) % 480
        h = 480-offY
        screen.blit(trailsBitmap,(0,0), (w, offY, offX, h))
        screen.blit(trailsBitmap,(offX,0),(0,offY,w,h))

        screen.blit(trailsBitmap,(0,h),(w,0,640,512))
        screen.blit(trailsBitmap,(offX, h), (0,0, 640,512))

        
        dead = False
        shipRotPoly = polyRotate(shipPoly,player.rot)
        shipTransPoly = polyTranslate(shipRotPoly,320,240)
        
        for x in range(int(player.x/BS)-1,int(player.x/BS)+6):
            for y in range(int(player.y/BS)-1,int(player.y/BS)+5):
                if(getMaze(x,y) == 1):
                    pygame.draw.rect(screen, (255,255,255), (x*BS-player.x,y*BS-player.y,BS,BS))
                    if polyIntersectsBlock(shipTransPoly, x*BS-player.x,y*BS-player.y):
                        dead = True
                elif(getMaze(x,y) == 2):
                    if (x,y) in saveQueue:
                        pygame.draw.rect(screen, (255,0,255), (x*BS-player.x,y*BS-player.y,BS,BS),4)
                    else:
                        pygame.draw.rect(screen, (0,255,255), (x*BS-player.x,y*BS-player.y,BS,BS),4)

        screen.blit(miniMap, (0,0))

        pygame.draw.polygon(screen, (255,0,0), shipTransPoly)
        pygame.draw.circle(trailsBitmap, (255,255,255), (320,240), 8)
        pygame.display.flip()
        if(dead):           
            playerReset()
            if(len(saveQueue)>0):
                (gridx,gridy) = saveQueue.pop()
                player.x = gridx*BS+BS/2-320
                player.y = gridy*BS+BS/2-240
                player.rot = saveDir.pop()

        dx = speed*math.cos(player.rot)
        dy = speed*math.sin(player.rot)
        pygame.draw.circle(trailsBitmap, (255,255,255), (int(player.x) % 640, int(player.y)%480), 2)
        pygame.draw.rect(trailsBitmap, (0,0,0), (int(player.x+320-8)%640, 0, 8,480))
        pygame.draw.rect(trailsBitmap, (0,0,0), (int(player.x-320)%640, 0, 8,480))
        pygame.draw.rect(trailsBitmap, (0,0,0), (0,int(player.y+240-8)%480, 640,8))
        pygame.draw.rect(trailsBitmap, (0,0,0), (0,int(player.y-240)%480, 640,8))
        if(player.x - (trailsX*256) > 256): trailsX+=1
        player.x += dx
        player.y += dy
        gridx = int((player.x+320) / BS)
        gridy = int((player.y+240) / BS)
        if(maze[gridx][gridy]==2):
            if((gridx,gridy) not in saveQueue):
                saveQueue.append((gridx,gridy))
                saveDir.append(player.rot)
                print "Savequeue is now: "
                print saveQueue
        processKeys()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    exit(0)

init()
loop()
