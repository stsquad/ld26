import pygame
from pygame.locals import *
import random
import math

# Constants
BS = 128 # Block size in pixels
GSX = 64 # Maze grid size
GSY = 64
class Player:
    def __init__(self):
        self.x = 32*4
        self.y = 32*4
        self.rot = 0

def init():
    global screen, clock, maze, shipPoly, player, speed
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
    speed = 4

def createMaze(maze):
    for x in range(0,64):
        for y in range(0,64):
            if(x>2 and y>2):
                maze[x][y] = random.choice([0,1])

def polyScale(poly,scale):
    newPoly = []
    for p in poly:
        newPoly.append((p[0]*scale, p[1]*scale))
    return newPoly

def polyTranslate(poly,x,y):
    newPoly = []
    for p in poly:
        newPoly.append((p[0]+x, p[1]+y))
    return newPoly

def polyRotate(poly,rads):
    newPoly = []
    for p in poly:
        newPoly.append((p[0]*math.cos(rads)-p[1]*math.sin(rads),
                        p[0]*math.sin(rads)+p[1]*math.cos(rads)))
    return newPoly

def processKeys():
    keys = pygame.key.get_pressed()
    if(keys[K_LEFT]): player.rot -= 0.05
    if(keys[K_RIGHT]): player.rot += 0.05

def getMaze(x,y):
    if(x<0 or x>= GSX or y<0 or y>=GSY): return 1
    return maze[x][y]

def loop():
    while 1:
        clock.tick(50)
        screen.fill((0,0,0))
        for x in range(int(player.x/BS)-1,int(player.x/BS)+6):
            for y in range(int(player.y/BS)-1,int(player.y/BS)+5):
                if(getMaze(x,y) == 1):
                    pygame.draw.rect(screen, (255,255,255), (x*BS-player.x,y*BS-player.y,BS,BS))
        shipRotPoly = polyRotate(shipPoly,player.rot)
        shipTransPoly = polyTranslate(shipRotPoly,320,256)
        
        pygame.draw.polygon(screen, (255,0,0), shipTransPoly)
        pygame.display.flip()
        player.x += speed*math.cos(player.rot)
        player.y += speed*math.sin(player.rot)
        processKeys()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    exit(0)

init()
loop()
