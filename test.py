import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rotating Wheel")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Constants
wheel_radius = 100
wheel_center = (screen_width // 2, screen_height // 2)
patch_size = 20

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

    # Draw the wheel
    wheel = pygame.Surface((wheel_radius * 2, wheel_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(wheel, BLACK, (wheel_radius, wheel_radius), wheel_radius, 2)

    # Rotate the wheel
    rotated_wheel = pygame.transform.rotate(wheel, math.degrees(circumference / (2 * math.pi * wheel_radius)))
    rotated_rect = rotated_wheel.get_rect(center=wheel_center)
    screen.blit(rotated_wheel, rotated_rect)

    # Draw the patch
    if dragging:
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - wheel_center[0], my - wheel_center[1]
        angle = math.atan2(dy, dx)
        delta_angle = angle - circumference
        circumference += delta_angle  # Update circumference with the change in angle
        patch_center = (wheel_center[0] + int(wheel_radius * math.cos(circumference)),
                        wheel_center[1] + int(wheel_radius * math.sin(circumference)))

    pygame.draw.circle(screen, BLUE, patch_center, patch_size)

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

pygame.quit()
