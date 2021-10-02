import pygame
import tkinter
from tkinter.filedialog import askopenfilename

def convert_matrix_to_img(img_matrix):
    dimension_x,dimension_y = len(img_matrix),len(img_matrix[0])
    new_img = pygame.Surface((dimension_x,dimension_y))
    for i in range(dimension_x):
        for j in range(dimension_y):
            new_img.set_at((i,j),(img_matrix[i][j]))
    return new_img

def convert_img_to_matrix(imgs:list[pygame.Surface]):
    '''
        converts pygame surface image objects to a colour matrix and saves into a text file
    '''
    all_imgs = ''
    for i in imgs:
        img = []
        no_i,no_j=i.get_width(),i.get_height()

        for x in range(no_i):
            helper = []
            for y in range(no_j):
                helper_2 = i.get_at((x,y))
                if helper_2[3] == 0:
                    helper.append((255,255,255))
                    continue
                # helper.append(i.get_at((x,y)))
                helper.append(i.get_at((x,y))[0:3])
            img.append(helper)
        all_imgs += str(img)
        all_imgs += '\n\n\n'

    with open('image.txt', 'w') as f:
        f.write(all_imgs)
    if len(imgs) == 1:
        return img


def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)

class Button():
    def __init__(self, color = (255,255,255), x:int = 0,y:int = 0,width:int = 0,height:int = 0, text='',win= None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        if self.text == '':
            self.text = 'Button'
        self.win = win
        self.val = ''
        self.clicked = False
        self.being_pressed_down = False
        
        self.draw()

    def draw(self,outline=None):
        if outline or self.clicked:
            pygame.draw.rect(self.win, (0,0,0), (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(self.win, self.color, (self.x,self.y,self.width,self.height),3)
        self.win.blit(self.text, (self.x, self.y ))

    def is_hovering(self) -> bool:
        #Pos is the mouse position or a tuple of (x,y) coordinates
        pos = pygame.mouse.get_pos()
        return (
            pos[0] > self.x
            and pos[0] < self.x + self.width
            and pos[1] > self.y
            and pos[1] < self.y + self.height
        )
    def update(self):
        if self.is_hovering():
            if pygame.mouse.get_pressed()[0]:
                # self.clicked = not self.clicked
                if not self.being_pressed_down:
                    if self.clicked:
                        self.clicked = False
                    else:
                        self.clicked = True
                self.being_pressed_down = True
                
            else:
                self.being_pressed_down = False
            self.draw(self.clicked)
        else:
            self.draw()

def main():
    pygame.init()
    WIN = pygame.display.set_mode((540, 600))
    pygame.display.update()
    buttons = []

    window = tkinter.Tk()
    window.withdraw()
    path =  askopenfilename(title="Open File to convert to matrix", filetypes=[("All files", "*.*"),("Portable Network Graphics", "*.png"), ("JPEG", "*.jpg"), ("GIF", "*.gif")])
    if path == '' or path is None:
        path = 'assets/load.jpg'
    saveImage = pygame.transform.scale(pygame.image.load(path), (25,25))

    fillImage = convert_img_to_matrix([saveImage])
    fillImage = convert_matrix_to_img(fillImage)
    buttons.append(Button(color = (255,255,255), x = 100, y = 100, width = 100, height = 50, text = fillImage,win = WIN))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for button in buttons:
            button.update()
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()

