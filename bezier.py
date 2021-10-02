import pygame

from components.colors import *

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((540, 600))
pygame.display.set_caption('')
FPS = 60

def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)

def lerp(a,b,t):
    return a + (b-a) * t

x1,y1 = (50,200)
x2,y2 = (500,200)
x3,y3 = (200,200)
x4,y4 = (300,300)

def quadratic(
    a,  # first point 
    b,  # second point
    c,  # third point 
    t   # parameter or step
    ):
    return lerp(lerp(a,b,t),lerp(b,c,t),t)

def cubic_bezier(x_3,y_3,x_4,y_4):
    t = 0 
    step = 0.001
    while t< 1.00001:
        x = lerp(quadratic(x1,x_3,x_4,t),quadratic(x_3,x_4,x2,t),t)
        y = lerp(quadratic(y1,y_3,y_4,t),quadratic(y_3,y_4,y2,t),t)
        pygame.draw.circle(WIN,(0,120,40), (x,y),(2))
        t += step

    pygame.draw.circle(WIN,WHITE, (x1,y1),(3))
    pygame.draw.circle(WIN,PINK, (x1,y1),(10),2)
    pygame.draw.circle(WIN,WHITE, (x2,y2),(3))
    pygame.draw.circle(WIN,PINK, (x2,y2),(10),2)

    pygame.draw.circle(WIN,(0,0,200), (x_3,y_3),(3),(3))
    pygame.draw.circle(WIN,(0,0,200), (x_4,y_4),(3),(3))

    pygame.display.update()

def quadratic_bezier(x_3,y_3):
    t = 0
    step = 0.2
    while t < 1.0001:
        lerp1_x = lerp(x1,x_3,t)
        lerp2_x = lerp(x_3,x2,t)
        lerp1_y = lerp(y1,y_3,t)
        lerp2_y = lerp(y_3,y2,t)
        x = lerp(lerp1_x,lerp2_x,t)
        y = lerp(lerp1_y,lerp2_y,t)
        pygame.draw.circle(WIN,(255,0,0), (x,y),(3))
        start_pos , end_pos = (lerp1_x,lerp1_y),(lerp2_x,lerp2_y)
        pygame.draw.line(WIN,GREEN,start_pos,end_pos)
        t += step

    pygame.draw.circle(WIN,(0,0,225), (50,200),(3))
    pygame.draw.circle(WIN,(0,0,225), (x2,y2),(3),(3))
    pygame.draw.circle(WIN,(0,0,225), (x_3,y_3),(3),(3))
    pygame.draw.circle(WIN,(0,0,225), (x_3,y_3),(3),(3))

    pygame.display.update()

cubic_bezier(x3,y3,x4,y4)


run = True
while run:
    clock.tick(FPS)
    if pygame.mouse.get_pressed()[0]:
        WIN.fill(absBlack)
        _x,_y = pygame.mouse.get_pos()
        dis_3 = (_x-x3)**2 + (_y-y3)**2
        dis_4 = (_x-x4)**2 + (_y-y4)**2

        if dis_3 < dis_4:
            x3,y3 = _x,_y
        else:
            x4,y4 = _x,_y
        cubic_bezier(x3,y3,x4,y4)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()