import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 400
screen_height = 300
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lever in Pygame")
pygame.display.set_caption("Rotating Wheel")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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
# Constants
wheel_radius = 100
wheel_center = (screen_width // 2, screen_height // 2)
patch_size = 20

# Variables to handle lever movement
lever_angle = 0  # Initial angle
lever_length = 100  # Length of lever arm
is_pressed = False  # Flag to track mouse button state
# Variables
circumference = 0
total_circumference = 0
dragging = False
offset = (0, 0)
patch_center = (wheel_center[0] + wheel_radius, wheel_center[1])

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
    # Draw the wheel
    wheel = pygame.Surface((wheel_radius * 2, wheel_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(wheel, BLACK, (wheel_radius, wheel_radius), wheel_radius, 2)

        # Limit lever angle
        if lever_angle > 90:
            lever_angle = 90
        elif lever_angle < -90:
            lever_angle = -90
    # Rotate the wheel
    rotated_wheel = pygame.transform.rotate(wheel, math.degrees(circumference / (2 * math.pi * wheel_radius)))
    rotated_rect = rotated_wheel.get_rect(center=wheel_center)
    screen.blit(rotated_wheel, rotated_rect)

    # Draw lever
    pygame.draw.rect(screen, lever_color, (lever_x, lever_y, lever_width, lever_height))
    # Draw the patch
    if dragging:
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - wheel_center[0], my - wheel_center[1]
        angle = math.atan2(dy, dx)
        delta_angle = angle - circumference
        circumference += delta_angle  # Update circumference with the change in angle
        patch_center = (wheel_center[0] + int(wheel_radius * math.cos(circumference)),
                        wheel_center[1] + int(wheel_radius * math.sin(circumference)))

    # Calculate circle position based on lever angle
    circle_x = lever_x + lever_width // 2 + int(lever_length * math.sin(math.radians(lever_angle)))
    circle_y = lever_y + int(lever_length * (1 - math.cos(math.radians(lever_angle))))
    pygame.draw.circle(screen, BLUE, patch_center, patch_size)

    # Draw circle
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dx, dy = event.pos[0] - patch_center[0], event.pos[1] - patch_center[1]
                dist = math.hypot(dx, dy)
                if dist <= patch_size:
                    dragging = True
                    offset = (event.pos[0] - patch_center[0], event.pos[1] - patch_center[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                # Update total circumference only if dragging occurred
                if circumference != 0:
                    total_circumference += circumference
                    print("Total circumference rotated:", total_circumference)
                    circumference = 0  # Reset circumference for next drag

    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
