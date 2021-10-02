import pygame
pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((540, 600))
pygame.display.set_caption('')
import time
FPS = 20

WHITE = pygame.Color('#d7d7d7')
GREAY = pygame.Color('#464646')
BLACK = pygame.Color('#3c3c3c')
GREEN = pygame.Color('#1eb464')
TURTLEGREEN = pygame.Color('#50c85a')
VIOLET = pygame.Color('#9632dc')
ORANGE = pygame.Color('#dc7832')
CYAN = pygame.Color('#64d2b4')
absBlack = pygame.Color('#000000')
BLUE = pygame.Color('#0a2864')
PINK = pygame.Color('#faa0a0')
YELLOW = pygame.Color('#ffeb00')
AMBER = pygame.Color('#dc0032')
MAROON = pygame.Color('#800000')
OLIVE = pygame.Color('#808000')
TEAL = pygame.Color('#008080')
TRANSPARENT = (0, 0, 0, 0)

def lerp(a,b,t):
    return a + (b-a) * t

def cubic_bezier(arr,step = 0.001):
    x1,y1,x2,y2,x_3,y_3 = arr[0].x,arr[0].y,arr[1].x,arr[1].y,arr[2].x,arr[2].y
    t = 0 
    while t < 1.0001:
        lerp1_x = lerp(x1,x_3,t)
        lerp2_x = lerp(x_3,x2,t)
        lerp1_y = lerp(y1,y_3,t)
        lerp2_y = lerp(y_3,y2,t)
        x = lerp(lerp1_x,lerp2_x,t)
        y = lerp(lerp1_y,lerp2_y,t)
        pygame.draw.circle(WIN,(255,0,0), (x,y),(3))
        # start_pos , end_pos = (lerp1_x,lerp1_y),(lerp2_x,lerp2_y)
        # pygame.draw.line(WIN,GREEN,start_pos,end_pos)
        t += step

    pygame.draw.circle(WIN,(0,0,225), (x1,y1),(3))
    pygame.draw.circle(WIN,(0,0,225), (x2,y2),(3),(3))
    pygame.draw.circle(WIN,(0,0,225), (x_3,y_3),(3),(3))
    # pygame.draw.circle(WIN,(0,0,225), (x_3,y_3),(3),(3))

class Point():
    def __init__(self,x,y,WIN) -> None:
        self.x,self.y = x,y
        self.WIN = WIN
        self.clicked = False
        self.draw()
    
    def draw(self):
        global BLACK
        pygame.draw.circle(WIN,BLACK, (self.x,self.y),(3))
        pygame.draw.circle(WIN,BLACK, (self.x,self.y),(10),2)
        
    
    def is_hovering(self):
        threshold = 15
        return (
            pygame.mouse.get_pos()[0] > self.x   -threshold     and 
            pygame.mouse.get_pos()[0] < self.x   +threshold     and
            pygame.mouse.get_pos()[1] > self.y  -threshold      and 
            pygame.mouse.get_pos()[1] < self.y  +threshold      )

start = None
end = None
end_cord = None
pnt = None
points = []
collection_points = []
clicked_point = None
all_points = []

run = True
while run:
    WIN.fill(WHITE)
    if pygame.mouse.get_pressed()[0]:
        x,y = pygame.mouse.get_pos()
        for point in all_points:
            # this variable is required to stop clicking other points than the ones we had clicked
            # ex if we already clicked index 1 and bring it close to 0 it snaps to 0 so this is needed
            # to check this comment this and take two points together

            proceed = False
            if clicked_point is None:
                proceed = True
            elif clicked_point == point:
                proceed = True

            if point.clicked or (proceed and point.is_hovering()):
                point.clicked = True
                clicked_point = point
                point.x,point.y = x,y
                break
        else:
            clicked_point = None
        if start is None and clicked_point is None:
            start = Point(x,y,WIN)
            all_points.append(start)
            points.append(start)
            time.sleep(0.2)
        elif end is None and clicked_point is None:
            end = Point(x,y,WIN)
            end.clicked = True
            end_cord = x,y
            all_points.append(end)
            points.append(end)
            time.sleep(0.1)
        elif clicked_point == end:
            if pnt is None:
                pnt = Point(end.x,end.y,WIN)
                all_points.append(pnt)
                points.append(pnt)
            else:
                if not (end_cord[0] - end.x) == 0 or (end_cord[1] - end.y) == 0:
                    pnt.x,pnt.y = end_cord[0] + (end_cord[0] - end.x) ,  end_cord[1] + (end_cord[1]- end.y)
                    print(pnt.x,pnt.y)
    else:
        for point in all_points :
            point.clicked = False
        clicked_point = None
        if not (start is None or end is None or pnt is None):
            collection_points.append([start,end,pnt])
            start = end
            end = None
            end_cord = None
            pnt = None

    if not (start is None or end is None or pnt is None) :
        cubic_bezier([start , end , pnt],0.02)
    if len(collection_points) :
        for points in collection_points:
            cubic_bezier(points,0.002)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for point in points:
        point.draw()
    pygame.display.update()
pygame.quit()