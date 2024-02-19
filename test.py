import pygame
import math

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Plus Symbol")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Circle parameters
circle_radius = 150
circle_center = (WIDTH // 2, HEIGHT // 2)

# Plus symbol parameters
plus_length = 300
plus_width = 10
plus_color = BLACK

# Angle for rotation
angle = 0
scroll_value = 0

# Stiffness factor
stiffness = 0.005

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            distance = math.sqrt((mouse_pos[0] - circle_center[0])**2 + (mouse_pos[1] - circle_center[1])**2)
            if distance <= circle_radius:
                if event.button == 4:  # Scroll Up
                    if scroll_value > 0:
                        angle -= math.pi / 18 * stiffness * scroll_value  # Rotate clockwise with stiffness
                        scroll_value -= 1
                elif event.button == 5:  # Scroll Down
                    if scroll_value < 100:
                        angle += math.pi / 18 * stiffness * scroll_value  # Rotate anti-clockwise with stiffness
                        scroll_value += 1
                print("Scroll Value:", scroll_value)
        
    # Calculate the positions of the ends of the plus symbol
    plus_end1 = (circle_center[0] + plus_length/2 * math.cos(angle), circle_center[1] + plus_length/2 * math.sin(angle))
    plus_end2 = (circle_center[0] + plus_length/2 * math.cos(angle + math.pi), circle_center[1] + plus_length/2 * math.sin(angle + math.pi))
    plus_end3 = (circle_center[0] + plus_length/2 * math.cos(angle + math.pi/2), circle_center[1] + plus_length/2 * math.sin(angle + math.pi/2))
    plus_end4 = (circle_center[0] + plus_length/2 * math.cos(angle - math.pi/2), circle_center[1] + plus_length/2 * math.sin(angle - math.pi/2))

    # Draw the plus symbol
    pygame.draw.line(screen, plus_color, plus_end1, plus_end2, plus_width)
    pygame.draw.line(screen, plus_color, plus_end3, plus_end4, plus_width)

    # Draw circle
    pygame.draw.circle(screen, BLACK, circle_center, circle_radius, 2)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
