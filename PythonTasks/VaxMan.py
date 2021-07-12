# 'tiles' GRID TAKEN FROM GRANT JENKS FREE PYTHON GAMES
# https://github.com/grantjenks/free-python-games/blob/master/freegames/pacman.py

import pygame
from random import choice
from pygame.constants import *
from numpy import array

pygame.init()

# Score tracking
Score = 0

# fmt: off
tiles = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
# fmt: on

# Scale = 420x420 (Grid size 20)
DISP_W = 340
DISP_H = 380
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

# Sprite groups
bricks = pygame.sprite.Group()
dots = pygame.sprite.Group()
ghosts = pygame.sprite.Group()

# Maze drawing
def createMaze():
    mY = 0
    for row in tiles:
        mX = 0
        for square in row:
            if square == 0:
                Brick(mX, mY, GRID_SIZE, GRID_SIZE)
            elif square == 1:
                Dot(mX + GRID_SIZE / 2, mY + GRID_SIZE / 2)
            mX += GRID_SIZE
        mY += GRID_SIZE    

# Round to nearest multiple (https://stackoverflow.com/a/2272174)
def roundNear(pos, base = 10):
    xVal = int(base * round(int(pos[0]) / base))
    yVal = int(base * round(int(pos[1]) / base))
    return array([xVal, yVal])

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y, surf = screen, color = WHITE):
        pygame.sprite.Sprite.__init__(self, dots)

        self.r = 2

        self.surf = surf
        self.color = color
        self.x = x
        self.y = y
        self.rect = pygame.draw.circle(self.surf, self.color, (self.x, self.y), self.r)

    def draw(self):
        pygame.draw.circle(self.surf, self.color, (self.x, self.y), self.r)

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

    def draw(self):
        pygame.draw.rect(self.surf, self.color, self.rect)

# Movement shortcuts 
SPEED = 1
UP = array([0, -1])
DOWN = array([0, 1])
LEFT = array([-1, 0])
RIGHT = array([1, 0])
STOPPED = array([0, 0])
MOVESET = [UP, DOWN, LEFT, RIGHT]

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color = YELLOW):
        pygame.sprite.Sprite.__init__(self)
        
        self.color = color
        self.pos = array([x, y])
        self.dir = STOPPED
        self.r = GRID_SIZE / 2
        self.rect = pygame.draw.circle(screen, self.color, self.pos, self.r)

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
        if ((self.dir != self.getDir(key)).all() and (self.dir != -1 * self.getDir(key)).all()): 
            self.pos = roundNear(self.pos)
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
        self.rect = pygame.draw.circle(screen, self.color, self.pos, self.r)

# Ghost class
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color = RED):
        pygame.sprite.Sprite.__init__(self)
        
        self.color = color
        self.pos = array([x, y])
        self.dir = choice(MOVESET)
        self.r = GRID_SIZE / 2
        self.rect = pygame.draw.circle(screen, self.color, self.pos, self.r)
   
    def changeDir(self):
        newDir = choice(MOVESET)
        while (self.dir == newDir).all() or (self.dir == -1 * newDir).all() or self.collision(newDir):
            newDir = choice(MOVESET)
        self.dir = newDir
        
    def collision(self, dir):
        origCenter = self.pos
        tstCenter = origCenter + dir
        tstPnt = tstCenter + (dir * self.r)
        
        for b in bricks:
            if (tstPnt[0] in range(b.x, b.x + b.w)) and (tstPnt[1] in range(b.y, b.y + b.h)):
                return True
        return False

    def move(self):       
        self.pos += self.dir * SPEED
        self.rect = pygame.draw.circle(screen, self.color, self.pos, self.r)

# Adding initial ghosts
ghosts.add(Ghost(30, 30))
ghosts.add(Ghost(310, 30))
ghosts.add(Ghost(30, 350))
ghosts.add(Ghost(310, 350))

player = Player(DISP_W / 2, DISP_H / 2)
createMaze()

# Multiplication timer
MultiplicationEvent = USEREVENT + 1
pygame.time.set_timer(MultiplicationEvent, 10000)

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
        elif event.type == MultiplicationEvent:
            newGhosts = []
            for g in ghosts:
                newGhosts.append(Ghost(int(g.pos[0]), int(g.pos[1])))
            for g in newGhosts:
                ghosts.add(g)

    if player.collision(player.dir):
        player.dir = STOPPED

    # Dot collection
    for i in pygame.sprite.spritecollide(player, dots, True):
        Score += 10
        print(Score)

    # Vaccination handler
    for i in pygame.sprite.spritecollide(player, ghosts, True):
        Score += 50
        print(Score)

    screen.fill(BACKGROUND_COLOR)
    for b in bricks:
        b.draw()
    for d in dots:
        d.draw()
    for g in ghosts:
        if g.collision(g.dir):
            g.changeDir()
        g.move()
    player.move()
    pygame.display.update()

    clock.tick(60)

pygame.quit()
quit()