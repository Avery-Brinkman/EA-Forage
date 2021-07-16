# 'tiles' GRID TAKEN FROM GRANT JENKS FREE PYTHON GAMES
# https://github.com/grantjenks/free-python-games/blob/master/freegames/pacman.py

import pygame
from random import seed, choice, randint
from pygame.constants import *
from numpy import array

# Initializes random
seed()

pygame.init()
pygame.font.init()
scoreText = pygame.font.SysFont('Comic Sans MS', 12)
endScreen = pygame.font.SysFont('Comic Sans MS', 30)

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
pygame.display.set_caption('VaxMan')

# Pygame clock
clock = pygame.time.Clock()

# Sprite groups
bricks = pygame.sprite.Group()
dots = pygame.sprite.Group()
ghosts = pygame.sprite.Group()

# Maze drawing
def createMaze():
    currY = 0
    foundStart = False
    for row in tiles:
        # Init for current row
        currX = 0
        foundStart = False
        bWidth = 0 
        rowLen = len(row) - 1

        for index, square in enumerate(row):
            if square == 0:
                # Starts brick
                if not foundStart:
                    foundStart = True
                    bStartX = currX
                    bStartY = currY
                
                # Brick longer
                bWidth += GRID_SIZE
                   
                # Checks to end last element
                if index == rowLen:
                    Brick(bStartX, bStartY, bWidth, GRID_SIZE)
                    foundStart = False

            else:
                # Ends brick
                if foundStart:
                    Brick(bStartX, bStartY, bWidth, GRID_SIZE)
                    foundStart = False
                    bWidth = 0
                Dot(currX + GRID_SIZE / 2, currY + GRID_SIZE / 2)
            currX += GRID_SIZE
        currY += GRID_SIZE


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
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

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

    def input(self, key):
        if key == K_UP:
            self.dir = UP * SPEED
        elif key == K_DOWN:
            self.dir = DOWN * SPEED
        elif key == K_LEFT:
            self.dir = LEFT * SPEED
        elif key == K_RIGHT:
            self.dir = RIGHT * SPEED
        else:
            self.dir = self.dir
        
    def collision(self):
        # Testing position (movement + radius)
        nextPos = array(self.dir + (self.dir / SPEED) * self.r)
        leftSide = array([-nextPos[1], nextPos[0]])
        rightSide = array(-leftSide).copy()
                
        # Checks for collsion
        for b in bricks:
            if b.rect.collidepoint(self.pos + nextPos):
                self.dir = STOPPED
            if b.rect.collidepoint(self.pos + rightSide) or b.rect.collidepoint(self.pos + rightSide - 1):
                self.pos -= rightSide / self.r
            if b.rect.collidepoint(self.pos + leftSide) or b.rect.collidepoint(self.pos + leftSide - 1):
                self.pos -= leftSide / self.r
            
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
        
    def collision(self):
        # Testing position (center + movement + radius)
        nextPos = array(self.dir + (self.dir / SPEED) * self.r).copy()
        # Creates a list of all possible directions except current direction (which caused the initial collision)
        options = [possibleMove * SPEED for possibleMove in MOVESET if (self.dir != possibleMove * SPEED).all()]
        # Checks for collsion
        for b in bricks:
            if b.rect.collidepoint(self.pos + nextPos):
                self.dir = choice(options)
                self.pos = roundNear(self.pos)
            
    def move(self):      
        if randint(1, 100) > 99:
            options = [possibleMove * SPEED for possibleMove in MOVESET if (self.dir != -1 * possibleMove * SPEED).all()]
            self.dir = choice(options)
            self.pos = roundNear(self.pos)
        self.pos += self.dir
        self.rect = pygame.draw.circle(screen, self.color, self.pos, self.r)

# Adding initial ghosts
ghosts.add(Ghost(30, 30))
ghosts.add(Ghost(310, 30))
ghosts.add(Ghost(30, 350))
ghosts.add(Ghost(310, 350))
GameOver = len(ghosts) * 32

player = Player(DISP_W / 2, DISP_H / 2)
createMaze()

# Multiplication event on timer
MultiplicationEvent = USEREVENT + 1
pygame.time.set_timer(MultiplicationEvent, 10000)

status = 'PLAYING'
showEndScreen = False
while status == 'PLAYING':
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            status = 'QUIT'
        # KB input
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                status = 'QUIT'
            # Movement
            else:
                player.input(event.key)
        # Multiplication
        elif event.type == MultiplicationEvent:
            # List to store new ghosts
            newGhosts = []
            for g in ghosts:
                newGhosts.append(Ghost(int(g.pos[0]), int(g.pos[1])))
            # Adding new ghosts
            for g in newGhosts:
                ghosts.add(g)
    # Stops player when they run into a wall
    player.collision()  

    # Dot collection
    for i in pygame.sprite.spritecollide(player, dots, True):
        Score += 10

    # Vaccination handler
    for i in pygame.sprite.spritecollide(player, ghosts, True):
        Score += 50

    # Drawing Screen
    screen.fill(BACKGROUND_COLOR)
    if showEndScreen:
        if win:
            screen.blit(endScreen.render('WINNER!', True, WHITE), (0, DISP_W))
        else:
            screen.blit(endScreen.render('GAME OVER!', True, WHITE), (0, DISP_W))
    else:
        for b in bricks:
            b.draw()
        for d in dots:
            d.draw()
        for g in ghosts:
            g.collision()
            g.move()
        player.move()

        # Drawing Text 
        screen.blit(scoreText.render(str(Score) + '     Ghosts: ' + str(len(ghosts)) + '/' + str(GameOver), True, WHITE), (0, 0))
    # Update screen
    pygame.display.update()
    

    # Endgame checking
    if not dots:
        showEndScreen = True
        win = True
    if len(ghosts) >= GameOver:
        showEndScreen = True
        win = False

    clock.tick(60)
pygame.quit()
quit()