import pygame
import random
import math
import copy
import time #this is pretty, not functional. don't use this, instead use 'midpoint.py'
from collections import namedtuple

Point = namedtuple("Point",['x','y'])
Line = namedtuple("Line",['p1','p2'])
pygame.init()

def midpoint(line):
    return Point(average(line.p1.x,line.p2.x),average(line.p1.y,line.p2.y))

def rand(intensity):
    return (random.random()-0.5)*intensity

def join(p1,p2):
    return Line(p1,p2)

def jitter(point,intensity):
    return Point(point.x,point.y+rand(intensity))

def average(*args):
    return sum(args)/len(args)

def split(ln,intensity):
    mid = midpoint(ln)
    mid = jitter(mid,intensity)
    return (Line(ln.p1,mid),Line(mid,ln.p2))

def midpointDisplacement(iterations,disp=False):
    lines = [ Line(Point(0,0.5),Point(1,0.5)) ]
    newLines = []
    strength = 1
    if(disp):
        display = pygame.display.set_mode( (500,500) )
        display.fill((255,255,255))
        pygame.display.update()
    for r in range(iterations):
        for ln in lines:
            for nln in split(ln,strength):
                newLines.append(nln)
        lines = copy.deepcopy(newLines)
        newLines = []
        strength /= 2
        if(disp):
            display.fill((255,255,255))
            for ln in lines:
                pygame.draw.line(display,(0,0,0),scale(ln.p1),scale(ln.p2))
            pygame.display.update()
            time.sleep(0.5)
    return(lines)

def scale(point):
    return Point(point.x*500,(point.y-0.5)*500 + 250)

if(__name__ == '__main__'):
    midpointDisplacement(12,True)
