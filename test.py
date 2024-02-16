import pygame
import sys
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(self.image, 2, 2, 2, YELLOW)  # Draw anti-aliased circle
        pygame.gfxdraw.filled_circle(self.image, 2, 2, 2, YELLOW)  # Fill circle
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = random.uniform(-0.1, 0.1)
        self.speed_y = random.uniform(1, 2)
        self.gravity = 0.1

    def update(self, screen):
        if self.speed_y > 0:
            self.speed_y -= self.gravity
            self.speed_y = max(self.speed_y, 0)
        else:
            self.speed_y += self.gravity
            self.speed_y = min(self.speed_y, 10)
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y
        if self.rect.y > screen.get_height():
            self.kill()

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    particles = pygame.sprite.Group()
    for _ in range(100):
        particle = Particle(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
        particles.add(particle)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        particles.update(screen)

        screen.fill(BLACK)
        particles.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
