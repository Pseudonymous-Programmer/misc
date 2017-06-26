import pygame
from pygame.locals import *
import math
import time
pygame.init()

X,Y,Z = 0,1,2

WINDOW_SIZE = 1000
REDUCTION_SCALE = 1/200
def project(point):
    if(point[Z] <= 0):
        return None #behind/on camera
    else:
        scale = 1/(REDUCTION_SCALE*point[Z])
        result =  (int(point[X]*scale + WINDOW_SIZE/2),int(point[Y]*scale + WINDOW_SIZE/2))
        if((0 <= result[X] < WINDOW_SIZE) and (0 <= result[Y] < WINDOW_SIZE)):
            return result
        return None

window = pygame.display.set_mode((WINDOW_SIZE,WINDOW_SIZE))

def rotate_around_y(degree,point):  
    x = point[X]
    z = point[Z]
    angle = math.radians(degree)
    return (math.cos(angle)*x-math.sin(angle)*z,point[Y],math.sin(angle)*x+math.cos(angle)*z)

def rotate_around_z(degree,point):
    x,y = point[X],point[Y]
    angle = math.radians(degree)
    return (x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle),point[Z])

def rotate_around_x(degree,point):
    z,y = point[Z],point[Y]
    angle = math.radians(degree)
    return (point[X],z*math.sin(angle)+y*math.cos(angle),z*math.cos(angle)-y*math.sin(angle))
    
def project_with_camera(point,camera):
    point = list(point)
    #transform point relative to camera
    for axe in [X,Y,Z]:
        point[axe] -= camera.location[axe]
    return project(rotate_around_x(camera.xrot,rotate_around_y(camera.yrot,point)))
    
points = [(1,1,1),(1,1,0),(1,0,1),(0,1,1),(1,0,0),(0,1,0),(0,0,1),(0,0,0)]
edges = [((1,1,1),(1,0,1)),((1,1,1),(0,1,1)),((0,1,1),(0,0,1)),((1,0,1),(0,0,1)),
         ((1,1,0),(1,0,0)),((1,1,0),(0,1,0)),((0,1,0),(0,0,0)),((1,0,0),(0,0,0)),
         ((1,1,0),(1,1,1)),((1,0,0),(1,0,1)),((0,1,0),(0,1,1)),((0,0,0),(0,0,1))]

class Camera:
    def __init__(self,points):
        self.xrot = 0
        self.yrot = 0
        self.location = (0,0,0)
        self.points = points
    def draw(self):
        window.fill((255,255,255))
        draws = [project_with_camera(i,self) for i in self.points]
        for i in draws:
            if(i):
                pygame.draw.circle(window,(0,0,0),i,3)
        for i in edges:
            begin = project_with_camera(i[0],self)
            end = project_with_camera(i[1],self)
            if(begin and end):
                pygame.draw.line(window,(255,0,0),begin,end)
        pygame.display.update()
    def update(self):
        for event in pygame.event.get():
            if(event.type == QUIT):
                quit()
            elif(event.type == KEYDOWN):
                if(event.key == K_ESCAPE): pygame.quit();quit()
                dz,dx = 0.1*math.cos(math.radians(self.yrot)),0.1*math.sin(math.radians(self.yrot))
                #print(dx,dy)
                if(event.key == K_RIGHT):
                    self.yrot += 1
                elif(event.key == K_LEFT):
                    self.yrot -= 1
                elif(event.key == K_UP):
                    self.xrot += 1
                elif(event.key == K_DOWN):
                    self.xrot -= 1
                elif(event.key == K_SPACE):
                    self.location = (self.location[X],self.location[Y]+0.1,self.location[Z])
                elif(event.key == K_z):
                    self.location = (self.location[X],self.location[Y]-0.1,self.location[Z])
                elif(event.key == K_w):
                    self.location = (self.location[X]+dx,self.location[Y],self.location[Z]+dz)
                elif(event.key == K_a):
                    self.location = (self.location[X]-dz,self.location[Y],self.location[Z]+dx)
                elif(event.key == K_d):
                    self.location = (self.location[X]+dz,self.location[Y],self.location[Z]-dx)
                elif(event.key == K_s):
                    self.location = (self.location[X]-dx,self.location[Y],self.location[Z]-dz)
            elif(event.type == MOUSEMOTION):
                self.xrot -= event.rel[1]/10
                self.yrot -= event.rel[0]/10
                
pygame.key.set_repeat(500,30); pygame.mouse.get_rel(); pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
camera = Camera(points)
camera.draw()
try:
    while(1):
        camera.update()
        camera.draw()
        time.sleep(0.01)
except Exception as e:
    print(e)
    pygame.quit()
