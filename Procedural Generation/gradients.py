def avg(*args):
    return sum(args)/len(args)

def averageLs(l1,l2):
    return [l1[i]+l2[i] for i in range(len(l1))]

def multiply(l,n):
    return [i*n for i in l]

def gradient(color0,color1,stage):
    return averageLs(multiply(color0,1-stage),multiply(color1,stage))

def map(stage,rng):
    offset,scale = rng
    stage -= offset
    scale -= offset
    return(stage/scale)

if __name__ == '__main__':
    import pygame
    import time
    pygame.init()
    disp = pygame.display.set_mode((500,500))
    up = True
    for r in range(10):
        stage = 0 if up else 1
        for i in range(101):
            disp.fill(gradient((255,0,0),(0,0,255),stage))
            pygame.display.update()
            stage += 0.01 * (1 if up else -1)
            time.sleep(0.01)
        up = not up
    pygame.quit()
