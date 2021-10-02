import time
import pygame 

from components.colors import *
from components.point import Point
from components.canvas import Canvas
from components.slider import Slider
from components.buttons import Button
from components.color_button import ColourButton
from components.buttons import convert_matrix_to_img, Button
from components.matrix_buttons import grid_matrix, up_matrix, down_matrix

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((600, 500))
pygame.display.set_caption('')
FPS = 60

points_color = (0,0,225)
line_color = (128,0,255)
tangent_color = (GREEN)

def lerp(a,b,t):
    return a + (b-a) * t

def quadratic_bezier(arr,step = 0.001,draw_tangents = False):
    x1,y1,x2,y2,x_3,y_3 = arr[0].x,arr[0].y,arr[1].x,arr[1].y,arr[2].x,arr[2].y
    t = 0 
    while t < 1.0001:
        lerp1_x = lerp(x1,x_3,t)
        lerp2_x = lerp(x_3,x2,t)
        lerp1_y = lerp(y1,y_3,t)
        lerp2_y = lerp(y_3,y2,t)
        x = lerp(lerp1_x,lerp2_x,t)
        y = lerp(lerp1_y,lerp2_y,t)
        pygame.draw.circle(WIN,line_color, (x,y),(3))
        if draw_tangents :
            start_pos , end_pos = (lerp1_x,lerp1_y),(lerp2_x,lerp2_y)
            stroke = 1
            pygame.draw.line(WIN,tangent_color,start_pos,end_pos,stroke)
        t += step

    pygame.draw.circle(WIN, points_color, (x1,y1),(3))
    pygame.draw.circle(WIN, points_color, (x2,y2),(3),(3))
    pygame.draw.circle(WIN, points_color, (x_3,y_3),(3),(3))
    # pygame.draw.circle(WIN,(0,0,225), (x_3,y_3),(3),(3))


points = []
collection_points = []
widgets = []

canvas = Canvas(0,0,WIN.get_width()-100,WIN.get_height(),WIN = WIN)
slider = Slider(posX  = 530 , posY  = 305,
                win = WIN,
                start = 1,end = 1000 , step = 1 ,
                slider_width  = 10, slider_height  = 30,
                color = (210,210,210),fontSize=25)
widgets.append(slider)
grid_button = Button(
    x = 535,y= 120,
    width = 25,height=25,
    text= convert_matrix_to_img(grid_matrix),
    win = WIN
)
widgets.append(grid_button)
up_button = Button(
    x = 565,y= 255,
    width = 25,height=25,
    text= convert_matrix_to_img(up_matrix),
    win = WIN
)
widgets.append(up_button)
down_button = Button(
    x = 565,y= 350,
    width = 25,height=25,
    text= convert_matrix_to_img(down_matrix),
    win = WIN
)
widgets.append(down_button)

slider_step = 1
line_color_btn = ColourButton(colour=line_color,x = 540,y = 40,win = WIN)
points_color_btn = ColourButton(colour=points_color,x = 510,y = 40,win = WIN)
tangent_color_btn = ColourButton(colour=tangent_color,x = 570,y = 40,win = WIN)
widgets.append(points_color_btn)
widgets.append(line_color_btn)
widgets.append(tangent_color_btn)

run = True
while run:
    WIN.fill(WHITE)
    canvas.draw()

    if pygame.mouse.get_pressed()[0]:
        x,y = pygame.mouse.get_pos()

        # moving the point mechanism
        for point in canvas.points:
            # this variable is required to stop clicking other points than the ones we had clicked
            # ex if we already clicked index 1 and bring it close to 0 it snaps to 0 so this is needed
            # to check this comment this and take two points together

            proceed = False
            if canvas.clicked_point is None:
                proceed = True
            elif canvas.clicked_point == point:
                proceed = True

            if point.clicked or (proceed and point.is_hovering()):
                if not canvas.in_limits((x,y)):
                    break
                point.clicked = True
                canvas.clicked_point = point
                point.x,point.y = x,y
                break
        else:
            canvas.clicked_point = None

        # placing the points
        if canvas.in_limits((x,y)):
            if canvas.start is None and canvas.clicked_point is None:
                canvas.start = Point(x,y,WIN)
                canvas.points.append(canvas.start)
                points.append(canvas.start)
                time.sleep(0.2)

            elif canvas.end is None and canvas.clicked_point is None:
                canvas.end = Point(x,y,WIN)
                canvas.end.clicked = True
                canvas.end_cord = x,y
                canvas.points.append(canvas.end)
                points.append(canvas.end)
                time.sleep(0.1)

            elif canvas.clicked_point == canvas.end:
                if canvas.pnt is None:
                    canvas.pnt = Point(canvas.end.x,canvas.end.y,WIN)
                    canvas.points.append(canvas.pnt)
                    points.append(canvas.pnt)
                else:
                    # if not (canvas.end_cord[0] - canvas.end.x) == 0 or (canvas.end_cord[1] - canvas.end.y) == 0:
                    if canvas.in_limits((canvas.end_cord[0] + (canvas.end_cord[0] - canvas.end.x) ,  canvas.end_cord[1] + (canvas.end_cord[1]- canvas.end.y))):
                            canvas.pnt.x,canvas.pnt.y = canvas.end_cord[0] + (canvas.end_cord[0] - canvas.end.x) ,  canvas.end_cord[1] + (canvas.end_cord[1]- canvas.end.y)

    # if mouse press is released
    else:
        # resetting things
        up_button.clicked,down_button.clicked = False,False 
        for point in canvas.points :
            point.clicked = False
        canvas.clicked_point = None

        # appending points to an array to draw
        if not (canvas.start is None or canvas.end is None or canvas.pnt is None):
            collection_points.append([canvas.start,canvas.end,canvas.pnt])
            canvas.start = canvas.end
            canvas.end = None
            canvas.end_cord = None
            canvas.pnt = None

    # drawing the current bezier curve
    if not (canvas.start is None or canvas.end is None or canvas.pnt is None) :
        quadratic_bezier([canvas.start , canvas.end , canvas.pnt], 1/slider.slideVal, draw_tangents= grid_button.clicked)
    # drawing all the bezier curves
    if len(collection_points) :
        for points in collection_points:
            quadratic_bezier(points,1/slider.slideVal,grid_button.clicked)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if up_button.clicked:
            slider.set_val(slider.slideVal-slider_step)
        if down_button.clicked:
            slider.set_val(slider.slideVal+slider_step)

    for point in points:
        point.draw()
    for widget in widgets:
        widget.update()

    line_color = line_color_btn.colour
    points_color = points_color_btn.colour
    tangent_color = tangent_color_btn.colour

    slider.draw() 
    pygame.display.update()
pygame.quit()