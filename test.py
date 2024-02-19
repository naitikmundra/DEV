import pygame
import random

# Define colors
WHITE = (255, 255, 255)

class Star:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = 300

    def move(self, dt):
        self.y += self.speed * dt

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.stars = [Star(random.randint(0, self.screen_width), random.randint(0, self.screen_height), random.randint(1, 3), random.uniform(0.1, 1.0)) for _ in range(100)]

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0  # Convert milliseconds to seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.move_stars(dt)
            self.draw_stars()

            pygame.display.flip()

        pygame.quit()

    def move_stars(self, dt):
        for star in self.stars:
            star.move(dt)
            if star.y > self.screen_height:  # If star moves out of screen, reset its position
                star.y = 0
                star.x = random.randint(0, self.screen_width)

    def draw_stars(self):
        self.screen.fill((0, 0, 0))  # Clear the screen
        for star in self.stars:
            pygame.draw.circle(self.screen, WHITE, (int(star.x), int(star.y)), star.radius)

if __name__ == "__main__":
    game = Game()
    game.run()
