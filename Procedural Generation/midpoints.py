import random
import math

def average(*args):
    return sum(args)/len(args)

def rand(strength):
    return (random.random()-0.5) * strength

def scale(n):
    return 2**n + 1

def FlatMidpoints(length,start=0.5,end=0.5,strength=1):
    middle = average(start,end) + rand(strength)
    #base cases
    if length == 1:
        return [end]
    elif length == 2:
        return [start,end]
    elif length == 3:
        return [start,middle,end]
    center = int(length/2)
    #recursion
    first = FlatMidpoints(center,start,middle,strength/2)
    second = FlatMidpoints(length-center + 1,middle,end,strength/2)
    return first + second[1::] #sliced to avoid center duplication

def _midpoints(array,start,size,strength):
    x,y = start
    middle = int(size/2)
    #we do the steps done every time
    if(not array[y][x+middle]):
        array[y][x+middle] = average(array[y][x],array[y][x+size]) + rand(strength)
    if(not array[y+middle][x]):
        array[y+middle][x] = average(array[y][x],array[y+size][x]) + rand(strength)
    if(not array[y+size][x+middle]):
        array[y+size][x+middle] = average(array[y+size][x],array[y+size][x+size]) + rand(strength)
    if(not array[y+middle][x+size]):
        array[y+middle][x+size] = average(array[y][x+size],array[y+size][x+size]) + rand(strength)
    array[y+middle][x+middle] = average(array[y+middle][x],array[y][x+middle],array[y+middle][x+size],array[y+size][x+middle]) + rand(strength)
    if size != 2:#a size of two is our base case
        #otherwise,we recurse
        _midpoints(array,start,middle,strength/2)
        _midpoints(array,(x+middle,y),middle,strength/2)
        _midpoints(array,(x,y+middle),middle,strength/2)
        _midpoints(array,(x+middle,y+middle),middle,strength/2)
    
def midpoints(size,jitter=0.25,variation = False):
    size = scale(size)
    array = [[0 for i in range(size)] for i in range(size)] #we make an array of 0s
    size -= 1 #this means we don't have to do indice arithmetic
    array[0][0] = rand(1) + 0.5 #we initalize the corners
    if(variation):
        array[0][size] = 1-array[0][0]
    else:
        array[0][size] = rand(1) + 0.5
    array[size][0] = rand(1) + 0.5
    if(variation):
        array[size][size] = 1-array[size][0]
    else:
        array[size][size] = rand(1) + 0.5 
    _midpoints(array,(0,0),size,jitter)
    return array

def render(pts,cFunc,window):
    for y in range(len(pts)):
        for x in range(len(pts)):
            pygame.draw.rect(window,cFunc(pts[y][x]),pygame.Rect(x,y,1,1))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if(event.type == KEYDOWN):
                if(event.key == K_ESCAPE):
                    quit()
                elif(event.key == K_d):
                    return False
                elif(event.key == K_s):
                    return True

def save(pts,cFunc,filename):
    img = Image.new('RGB',(len(pts[0]),len(pts)))
    img.putdata([tuple(cFunc(i)) for row in pts for i in row])
    img.save(filename)
    
if __name__ == '__main__':
    import gradients
    import pygame
    import time
    from pygame.locals import *
    from PIL import Image
    pygame.init()
    colorLambda1 = lambda color: (
        (0,0,100)       if 0.1 > color else
        (0,0,150)       if 0.2 > color else
        (0,0,255)       if 0.35 > color else
        (255,255,0)     if 0.4 > color else
        (0,200,0)       if 0.5 > color else
        (0,150,0)       if 0.6 > color else
        (0,100,0)       if 0.7 > color else
        (125,125,125)   if 0.8 > color else
        (150,150,150)   if 0.9 > color else
        (255,255,255) 
        )
    print("D to skip\nESC to stop\nS to save")
    window = pygame.display.set_mode((scale(10),scale(10)))
    while(True):
        pts = midpoints(10,0.5)
        if(render(pts,colorLambda1,window)):
            pygame.quit()
            save(pts,colorLambda1,input("Filename: "))
            quit()
