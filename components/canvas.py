import pygame
from components.point import Point

class Canvas():
    def __init__(self,x=0,y=0,width = 500,height = 500,WIN = None) -> None:

        self.x , self.y = x, y
        self.width , self.height = width,height
        self.WIN = WIN
        self.step = 0.001

        self.points = []
        self.start = None
        self.end = None
        self.end_cord = None
        self.pnt = None
        self.clicked_point = None

        self.draw()

    def draw(self):
        # drawing the border lines
        BLACK = pygame.Color('#3c3c3c')

        pygame.draw.line(self.WIN,BLACK,(self.x+self.width,self.y),(self.x+self.width,self.y+self.height))
        pygame.draw.line(self.WIN,BLACK,(self.x+self.width,self.y+self.height),(0,self.y+self.height))

    def in_limits(self,pos):
        x,y = pos
        return not ((x < self.x or x > self.width+self.x) or (y < self.y or y > self.height+self.y))

    def click(self):
        x,y = pygame.mouse.get_pos()
        if self.in_limits((x,y)):
            return
        self.points.append(Point(x,y,self.WIN))
        self.draw()
        return self.points[-1]

