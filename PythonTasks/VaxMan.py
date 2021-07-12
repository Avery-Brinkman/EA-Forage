# 'tiles' GRID TAKEN FROM GRANT JENKS FREE PYTHON GAMES
# https://github.com/grantjenks/free-python-games/blob/master/freegames/pacman.py

import pygame
from pygame import surface
from pygame.constants import *
from numpy import array

pygame.init()

# fmt: off
tiles = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
# fmt: on

# Scale = 420x420 (Grid size 20)
DISP_W = 420
DISP_H = 420
GRID_SIZE = 20

# Colors
RED =       (255, 0,   0)
GREEN =     (0,   255, 0)
BLUE =      (0,   0,   255)
YELLOW =    (255, 255, 0)
WHITE =     (255, 255, 255)
BLACK =     (0,   0,   0)
BACKGROUND_COLOR = BLUE

# Creating Screen
screen = pygame.display.set_mode((DISP_W, DISP_H))
pygame.display.update()
pygame.display.set_caption('VaxMan')

# Pygame clock
clock = pygame.time.Clock()

maze = pygame.sprite.Group()
bricks = pygame.sprite.Group()
pills = pygame.sprite.Group()

# Maze drawing
def createMaze():
    mY = 0
    for row in tiles:
        mX = 0
        for square in row:
            if square == 0:
                Brick(mX, mY, GRID_SIZE, GRID_SIZE)
            mX += GRID_SIZE
        mY += GRID_SIZE    

# Brick class
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, surf = screen, color = BLACK):
        pygame.sprite.Sprite.__init__(self, bricks)
        
        self.surf = surf 
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = (self.x, self.y, self.w, self.h)
        self.pos = (x, y)

    def draw(self):
        pygame.draw.rect(self.surf, self.color, self.rect)

# Movement shortcuts 
SPEED = 1
UP = array([0, -1])
DOWN = array([0, 1])
LEFT = array([-1, 0])
RIGHT = array([1, 0])
STOPPED = array([0, 0])

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.pos = array([x, y])
        self.dir = STOPPED
        self.intPos = (x, y)
        self.r = GRID_SIZE / 2

        self.rect = pygame.draw.circle(screen, YELLOW, self.pos, self.r)

    def getDir(self, key):
        if key == K_UP:
            return UP * SPEED
        elif key == K_DOWN:
            return DOWN * SPEED
        elif key == K_LEFT:
            return LEFT * SPEED
        elif key == K_RIGHT:
            return RIGHT * SPEED
        else:
            return self.dir        

    def input(self, key):
        self.dir = self.getDir(key)
        
    def collision(self, dir):
        origCenter = self.pos
        tstCenter = origCenter + dir
        tstPnt = tstCenter + (dir * self.r)
        
        for b in bricks:
            if (tstPnt[0] in range(b.x, b.x + b.w)) and (tstPnt[1] in range(b.y, b.y + b.h)):
                return True
        return False

    def move(self):       
        self.pos += self.dir
        # self.dir = array([0, 0])
        self.rect = pygame.draw.circle(screen, YELLOW, self.pos, self.r)

player = Player(50, 30)
createMaze()

# print(f'{bricks.sprites()}')
playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                playing = False
            print(pygame.key.name(event.key))
            if not player.collision(player.getDir(event.key)):
                player.input(event.key)

    if player.collision(player.dir):
        player.dir = STOPPED
    screen.fill(BACKGROUND_COLOR)
    for b in bricks:
        b.draw()
    player.move()
    pygame.display.update()

    clock.tick(30)

pygame.quit()
quit()