import pygame
import time
from slider import Slider

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((540, 600))
pygame.display.set_caption('bezier curves')
FPS = 20
def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)

WHITE = (215, 215, 215)
GREAY = (70, 70, 70)
BLACK = (0, 0, 0)
BLUE = (10, 40, 100)
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


def quadratic(
    a,  # first point 
    b,  # second point
    c,  # third point 
    t   # parameter or step
    ):
    return lerp(lerp(a,b,t),lerp(b,c,t),t)

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
        start_pos , end_pos = (lerp1_x,lerp1_y),(lerp2_x,lerp2_y)
        pygame.draw.line(WIN,GREEN,start_pos,end_pos)
        t += step

    pygame.draw.circle(WIN,(0,0,225), (x1,y1),(3))
    pygame.draw.circle(WIN,(0,0,225), (x2,y2),(3),(3))
    pygame.draw.circle(WIN,(0,0,225), (x_3,y_3),(3),(3))
    # pygame.draw.circle(WIN,(0,0,225), (x_3,y_3),(3),(3))

    pygame.display.update()

class Canvas():
    def __init__(self,x=0,y=0,width = 500,height = 500,WIN = None) -> None:
        self.x , self.y = x, y
        self.width , self.height = width,height
        self.surface = pygame.Surface((self.width,self.height))
        self.surface.fill(WHITE)
        self.WIN = WIN
        self.step = 0.001
        self.points = []

        self.draw()

    def draw(self):
        self.WIN.blit(self.surface,(self.x,self.y))
        for point in self.points:
            point.draw()
        pygame.display.update()

    def in_limits(self,pos):
        x,y = pos
        return  (x < self.x or x > self.width+self.x) or (y < self.y or y > self.height+self.y)

    def bezier(self,step) :
        if len(self.points) >3:
            cubic_bezier(self.points,1/step)

    def right_click(self):
        if len(self.points) > 3:
            cubic_bezier(self.points)

            return
        x,y = pygame.mouse.get_pos()
        if self.in_limits((x,y)):
            return
        self.points.append(Point(x,y,self.WIN))
        self.draw()


class Point():
    def __init__(self,x,y,WIN) -> None:
        self.x,self.y = x,y
        self.WIN = WIN
        self.clicked = False
        self.draw()
    
    def draw(self):
        pygame.draw.circle(WIN,BLACK, (self.x,self.y),(3))
        pygame.draw.circle(WIN,BLACK, (self.x,self.y),(10),2)
    
    def is_hovering(self):
        threshold = 15
        return (
            pygame.mouse.get_pos()[0] > self.x   -threshold     and 
            pygame.mouse.get_pos()[0] < self.x   +threshold     and
            pygame.mouse.get_pos()[1] > self.y  -threshold      and 
            pygame.mouse.get_pos()[1] < self.y  +threshold      )

def main():
    widgets = []
    run = True
    canvas = Canvas(WIN = WIN)
    slider = Slider(520,200,WIN,start=1,end=1000,step=1)
    slider.set_val(5)
    widgets.append(slider)
    sliderval = 0

    while run:
        clock.tick(FPS)

        if pygame.mouse.get_pressed()[0]:
            for point in canvas.points:
                if point.clicked or  point.is_hovering():
                    point.clicked = True
                    if canvas.in_limits(pygame.mouse.get_pos()):
                        break
                    point.x,point.y = pygame.mouse.get_pos()
                    break
            
            if len(canvas.points) < 4:
                canvas.right_click()
                time.sleep(0.1)
                if len(canvas.points) == 4:
                    canvas.draw()
                    canvas.bezier(slider.slideVal)
            else:
                canvas.draw()
                canvas.bezier(slider.slideVal)

        else:
            for point in canvas.points :
                point.clicked = False
                

        if sliderval != slider.slideVal:
            sliderval = slider.slideVal
            canvas.draw()
            canvas.bezier(slider.slideVal)

                
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for widget in widgets:
            widget.update()
    pygame.quit()

if __name__ == "__main__":
    main()