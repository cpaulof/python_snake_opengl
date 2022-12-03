import random

from OpenGL.GL import *
from OpenGL.GLU import *


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "<Block x:{}, y:{}>".format(self.x, self.y)

class Snake:
    def __init__(self, width, height, initial_position=None, window_minx=50, window_miny=50, window_step=10):
        if initial_position is None:
            initial_position = (width//2, height//2)
        assert len(initial_position) == 2

        self.wminx = window_minx
        self.wminy = window_miny
        self.wmaxx = window_minx + window_step * width 
        self.wmaxy = window_miny + window_step * height 
        self.wstep = window_step

        

        self.width = width
        self.height = height

        self.direction = 1 # 0-top | 1-right | 2-bottom | 3-left
        self.size = 1
        self.blocks = [Block(*initial_position)]
        self.blocks_to_grow = []
        self.next_block_position = None
        self.alive = True

        self.gen_food()
    
    def grow(self):
        self.blocks_to_grow.append(len(self.blocks)-1)
    
    def update_grow_blocks(self):
        self.check_grow_blocks()
        for i in range(len(self.blocks_to_grow)):
            self.blocks_to_grow[i]-=1
        
    def check_alive(self):
        block = (self.blocks[0].x, self.blocks[0].y)
        current_blocks = [(i.x, i.y) for i in self.blocks[1:]]

        if block[0] < 0 or block[1] < 0 or block[0] >= self.width or block[1] >= self.height:
            self.alive = False
        if block in current_blocks:
            self.alive = False
    
    def check_grow_blocks(self):
        #print(self.blocks_to_grow)
        if len(self.blocks_to_grow) == 0: return
        if self.blocks_to_grow[0] == 0:
            #print("updating blocks to grow")
            self.next_block_position = (self.blocks[-1].x, self.blocks[-1].y)
        if self.blocks_to_grow[0] == -1:
            self.blocks_to_grow.pop(0)
            #print("adding new blopck")
            assert self.next_block_position is not None
            self.blocks.append(Block(*self.next_block_position))
    
    def change_direction(self, new_direction):
        assert 0 <= new_direction <= 3
        if (self.direction in (0, 2) and new_direction in (0, 2)) or (self.direction in (1, 3) and new_direction in (1, 3)):
            return
        self.direction = new_direction
    
    def move(self):
        moves = {
            0: [0, 1], 
            1: [1, 0], 
            2: [0, -1],
            3: [-1, 0]
        }

        new_x, new_y = 0, 0

        if len(self.blocks) > 1:
            new_x = self.blocks[0].x
            new_y = self.blocks[0].y

        for idx in range(1, len(self.blocks[1:])+1):
            old_x = self.blocks[idx].x
            old_y = self.blocks[idx].y
            self.blocks[idx].x = new_x
            self.blocks[idx].y = new_y
            new_x = old_x
            new_y = old_y
            
        
        move = moves[self.direction]
        self.blocks[0].x += move[0]
        self.blocks[0].y += move[1]

        
        self.update_grow_blocks()
        #self.grow()
        self.check_alive()
        self.check_food_collision()
    
    def check_food_collision(self):
        head_pos = (self.blocks[0].x, self.blocks[0].y)
        if head_pos == self.food:
            self.grow()
            self.gen_food()

    def transform(self, x, y):
        #  xp = (x - w.xmin)/(w.xmax - w.xmin)*self.width
        # p = (1 - (y- w.ymin)/(w.ymax - w.ymin))*self.height
        xw = x /self.width*(self.wmaxx - self.wminx) + self.wminx
        yw = (1 - y/self.height)*(self.wmaxy - self.wminy) + self.wminy

        
        s = self.wstep // 2
        x1 = xw - s
        x2 = xw + s
        y1 = yw - s
        y2 = yw + s
        return x1, x2, y1, y2

    def render(self):
        #print(len(self.blocks))
        head = True
        for block in self.blocks:
            #print(block)
            x1, x2, y1, y2 = self.transform(block.x, block.y)

            glColor3f(0.7, 0.9, 0.2)

            if head:
                glColor3f(0.9, 0.2, 0.2)
                head = False

            glBegin(GL_LINE_LOOP)
            glVertex2f(x1, y1)
            glVertex2f(x2, y1)
            glVertex2f(x2, y2)
            glVertex2f(x1, y2)
            glEnd()
        
        glColor3f(0.0, 0.9, 0.8)
        x1, x2, y1, y2 = self.transform(self.food[0], self.food[1])
        glBegin(GL_LINE_LOOP)
        glVertex2f(x1, y1)
        glVertex2f(x2, y1)
        glVertex2f(x2, y2)
        glVertex2f(x1, y2)
        glEnd()

    def __repr__(self):
        s = "<Snake \n\t"
        for b in self.blocks[::-1]:
            s+=repr(b)+"\n\t"
        s+=">"
        return s
    
    def get_possible_food_locations(self):
        locs = []
        block_positions = [(i.x, i.y) for i in self.blocks]
        for x in range(self.width):
            for y in range(self.height):
                if not (x, y) in block_positions:
                    locs.append((x,y))
        return locs

    def gen_food(self):
        self.food = random.choice(self.get_possible_food_locations())
        



    
