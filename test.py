import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lever in Pygame")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Lever properties
lever_width = 100
lever_height = 20
lever_color = BLACK
lever_x = (screen_width - lever_width) // 2
lever_y = (screen_height - lever_height) // 2

# Circle properties
circle_radius = 20
circle_color = BLACK
circle_x = lever_x + lever_width // 2
circle_y = lever_y - circle_radius

# Variables to handle lever movement
lever_angle = 0  # Initial angle
lever_length = 100  # Length of lever arm
is_pressed = False  # Flag to track mouse button state

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_pressed = False

    # If left mouse button is pressed, update lever angle
    if is_pressed:
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate angle between mouse and lever origin
        dx = mouse_x - circle_x
        dy = mouse_y - circle_y
        lever_angle = math.degrees(math.atan2(dy, dx))

        # Limit lever angle
        if lever_angle > 90:
            lever_angle = 90
        elif lever_angle < -90:
            lever_angle = -90

    # Draw lever
    pygame.draw.rect(screen, lever_color, (lever_x, lever_y, lever_width, lever_height))

    # Calculate circle position based on lever angle
    circle_x = lever_x + lever_width // 2 + int(lever_length * math.sin(math.radians(lever_angle)))
    circle_y = lever_y + int(lever_length * (1 - math.cos(math.radians(lever_angle))))

    # Draw circle
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)

    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
