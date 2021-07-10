import pygame
pygame.init()

# Setting up drawing window
screen = pygame.display.set_mode([500, 500])

# Run until user asks to quit
running = True
while running:
    # Did user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fills screen w/ white
    screen.fill((255, 255, 255))
    
    # Draws a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flips display
    pygame.display.flip()

# Quits
print('Quit game.')
pygame.quit()