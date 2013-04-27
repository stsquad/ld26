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
    global screen, clock, maze, shipPoly, player, speed, trailsBitmap, trailsX, trailsY
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
    speed = 4
    trailsX = 0
    trailsY = 0

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
    

def processKeys():
    keys = pygame.key.get_pressed()
    if(keys[K_LEFT]): player.rot -= 0.05
    if(keys[K_RIGHT]): player.rot += 0.05

def getMaze(x,y):
    if(x<0 or x>= GSX or y<0 or y>=GSY): return 1
    return maze[x][y]

def loop():
    global trailsX
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
        pygame.draw.polygon(screen, (255,0,0), shipTransPoly)
        pygame.draw.circle(trailsBitmap, (255,255,255), (320,240), 8)
        pygame.display.flip()
        if(dead): 
            playerReset()

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
        processKeys()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    exit(0)

init()
loop()
