import math
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from snake import Snake

pygame.init()

screen_width = 1000
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Pygame + OpenGL Example')

def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() #clear the system
    gluOrtho2D(0, 640, 0, 480)


def plot_triangle(obj):
    glBegin(GL_LINE_LOOP)
    for x,y in obj.points:
        glVertex2f(x, y)
    glEnd()


def plot_rectangle(obj):
    glBegin(GL_LINE_LOOP)
    for x,y in obj.points:
        glVertex2f(x, y)
    glEnd()




done = False
init_ortho()
glPointSize(3)

scene_x = 100
scene_y = 40
scene_step = 20

size = 20

snake = Snake(size, size, window_minx=scene_x, window_miny=scene_y, window_step=scene_step)
count = 0

speed = 30

def cenario():
    glColor3f(0.1, 0.7, 0.5)
    x1 = scene_x - scene_step//2-3
    y1 = scene_y - scene_step//2-3
    x2 = scene_x+scene_step*size + scene_step//2+3
    y2 = scene_y+scene_step*size + scene_step//2+3
    glBegin(GL_LINE_LOOP)

    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

initial_size = 5

while not done:
    p = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if pygame.key.get_pressed()[pygame.K_UP]:
            snake.change_direction(2)

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            snake.change_direction(0)

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            snake.change_direction(3)

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            snake.change_direction(1)
        
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            snake.grow()
            print(snake.blocks)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    
    count += 1
    
    if not snake.alive:
        done = True
    cenario()
    if count % (speed-len(snake.blocks)) == 0:
        if initial_size > 1:
            snake.grow()
            initial_size -= 1
        snake.move()
    snake.render() 
    pygame.display.flip()
    pygame.time.wait(5)
pygame.quit()