import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the width and height of the screen (you can adjust as needed)
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Expanding Circle")

# Define colors
ORANGE = (255, 165, 0)
WHITE =  (0,0,0)
# Specify the coordinates for the center of the circle
start_x, start_y = 400, 300

# Initial radius of the circle
radius = 1

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with orange color
    screen.fill(WHITE)
    
    # Draw the circle
    pygame.draw.circle(screen, (0, 0, 0), (start_x, start_y), radius, 1)  # Black outline
    pygame.draw.circle(screen, ORANGE, (start_x, start_y), radius - 1)  # Orange circle
    
    # Update the display
    pygame.display.flip()
    
    # Increase the radius
    radius += 0.1
    
    # If the circle expands beyond the screen size, exit the loop
    if radius >= 100:
        pygame.quit()

# Wait for a moment before closing the window
pygame.time.wait(5000)

# Quit Pygame
pygame.quit()
sys.exit()
