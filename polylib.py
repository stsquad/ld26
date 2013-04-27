from globs import *
import copy
import math

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


def linesIntersect(s1,e1,s2,e2):
    A1 = e1[1]-s1[1]
    B1 = s1[0]-e1[0]
    C1 = A1*s1[0]+B1*s1[1]
    A2 = e2[1]-s2[1]
    B2 = s2[0]-e2[0]
    C2 = A2*s2[0]+B2*s2[1]

    determinant = A1*B2-A2*B1
    if(determinant == 0): return False

    #Determine start pos                                                                                                                     
    x = (B2*C1-B1*C2)/determinant
    y = (A1*C2-A2*C1)/determinant

    intersect = (x,y)

    box1x1 = min(s1[0],e1[0])
    box1x2 = max(s1[0],e1[0])
    box1y1 = min(s1[1],e1[1])
    box1y2 = max(s1[1],e1[1])

    box2x1 = min(s2[0],e2[0])
    box2x2 = max(s2[0],e2[0])
    box2y1 = min(s2[1],e2[1])
    box2y2 = max(s2[1],e2[1])

    # Check bounding boxes actually overlap                                                                                                  
    if(box1x2 < box2x1 or box1x1 > box2x2): return False
    if(box1y2 < box2y1 or box1y1 > box2y2): return False
    box3x1 = max(box1x1, box2x1)
    box3x2 = min(box1x2, box2x2)
    box3y1 = max(box1y1, box2y1)
    box3y2 = min(box1y2, box2y2)

    if(x>=box3x1 and y>=box3y1 and x<=box3x2 and y<=box3y2):
        return True
    return False

def polyIntersectsBlock(poly2, blockX,blockY):
    poly1 = [ (0,0), (BS,0), (BS,BS), (0,BS), (0,0) ]
    poly1 = polyTranslate(poly1,blockX,blockY)

    for i in range(0,len(poly1)-1):
        for j in range(0,len(poly2)-1):
            if(linesIntersect(poly1[i],poly1[i+1],poly2[j],poly2[j+1])):
                return True
    return False
