import pygame 

class Point():
    def __init__(self,x,y,WIN) -> None:
        self.x,self.y = x,y
        self.WIN = WIN
        self.clicked = False
        self.draw()
    
    def draw(self):
        GREAY = pygame.Color('#464646')

        pygame.draw.circle(self.WIN,GREAY, (self.x,self.y),(2))
        pygame.draw.circle(self.WIN,GREAY, (self.x,self.y),(8),2)
        
    
    def is_hovering(self):
        threshold = 15
        return (
            pygame.mouse.get_pos()[0] > self.x   -threshold     and 
            pygame.mouse.get_pos()[0] < self.x   +threshold     and
            pygame.mouse.get_pos()[1] > self.y  -threshold      and 
            pygame.mouse.get_pos()[1] < self.y  +threshold      )
