import pygame
import sys
import pyautogui
import random
# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

class Button:
    def __init__(self, text, font, x, y, width, height, default_color, hover_color):
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.default_color = default_color
        self.hover_color = hover_color
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.default_color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            print(f"Button '{self.text}' clicked!")

class LoadingScene:
    def __init__(self, screen, image_path, scale_factor_decrement=0.002):
        self.screen = screen
        self.image = pygame.image.load(image_path)
        self.image_width, self.image_height = self.image.get_size()
        self.initial_scale_factor = 1.0
        self.min_scale_factor = 0.01
        self.scale_factor_decrement = scale_factor_decrement
        self.clock = pygame.time.Clock()
        self.loading_sound = pygame.mixer.Sound("loading_sound.wav")  # Load the sound file
        self.start_time = pygame.time.get_ticks()  # Get the current time
        self.sound_volume = 0.0  # Initial volume level

    def run(self):
        # Display the image for 2 seconds
        while pygame.time.get_ticks() - self.start_time < 1000:  # Wait for 1000 milliseconds (1 second)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Fill the screen with black
            self.screen.fill(BLACK)

            # Draw the image on the screen
            self.screen.blit(self.image, (0, 0))

            # Update the display
            pygame.display.flip()

        # Start pixelation after 1 second
        self.loading_sound.play()  # Play the sound effect
        # Fade in effect
        while self.sound_volume < 1.0:
            self.sound_volume += 0.01  # Adjust the increment for the fading effect
            self.loading_sound.set_volume(self.sound_volume)  # Set the volume
            pygame.time.delay(10)  # Adjust the delay for smoother fading

        while self.initial_scale_factor >= self.min_scale_factor:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Fill the screen with black
            self.screen.fill(BLACK)

            # Scale the image
            scaled_image = pygame.transform.scale(self.image, (int(self.image_width * self.initial_scale_factor), int(self.image_height * self.initial_scale_factor)))
            scaled_image = pygame.transform.scale(scaled_image, (self.image_width, self.image_height))  # Scale back to original size

            # Draw the pixelated image on the screen
            self.screen.blit(scaled_image, (0, 0))

            # Decrement the scale factor
            self.initial_scale_factor -= self.scale_factor_decrement

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(30)  # Adjust the frame rate here

        self.loading_sound.stop()  # Stop the sound effect when pixelation is done

        # Switch to the menu scene
        menu_scene = MenuScene(self.screen)
        menu_scene.run()





class Star:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.y -= self.speed

class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.buttons = [
            Button("Play", self.font, 0, 0, 200, 50, GRAY, LIGHT_GRAY),
            Button("Options", self.font, 0, 0, 200, 50, GRAY, LIGHT_GRAY),
            Button("Quit", self.font, 0, 0, 200, 50, GRAY, LIGHT_GRAY)
        ]
        self.num_stars = 50
        self.star_speed_min = 1
        self.star_speed_max = 5
        self.stars = self.create_stars(self.num_stars, self.star_speed_min, self.star_speed_max)
        self.arrange_buttons()

    def create_stars(self, num_stars, min_speed, max_speed):
        stars = []
        for _ in range(num_stars):
            x = random.randint(0, self.screen.get_width())
            y = random.randint(0, self.screen.get_height())
            speed = random.randint(min_speed, max_speed)
            stars.append(Star(x, y, speed))
        return stars

    def move_stars(self):
        for star in self.stars:
            star.move()
            if star.y < -10:  # If star moves out of screen, reset its position
                star.y = self.screen.get_height() + 10
                star.x = random.randint(0, self.screen.get_width())

    def draw_stars(self):
        for star in self.stars:
            pygame.draw.circle(self.screen, WHITE, (star.x, star.y), 2)


    def arrange_buttons(self):
        total_button_height = sum(button.height for button in self.buttons) + (len(self.buttons) - 1) * 20
        y_offset = (self.screen.get_height() - total_button_height) / 1.1 # Shifted buttons lower by 50 pixels
        for button in self.buttons:
            button.x = (self.screen.get_width() - button.width) / 2
            button.y = y_offset
            y_offset += button.height + 20
            button.rect = pygame.Rect(button.x, button.y, button.width, button.height)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in self.buttons:
                    button.update(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos) and button.text == "Play":
                            game_scene = GameScene(self.screen)
                            game_scene.run()

            # Move and draw stars
            self.move_stars()
            self.screen.fill(BLACK)
            self.draw_stars()

            # Draw buttons
            for button in self.buttons:
                button.draw(self.screen)

            # Update the display
            pygame.display.flip()
            clock.tick(30)

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y,ax,ay):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = random.uniform(-0.1, 0.1)  # Random horizontal speed
        self.speed_y = random.uniform(1, 2)  # Adjusted initial upward speed
        self.gravity = 2  # Gravity to simulate downward acceleration
        self.max_speed_y = 10  # Maximum vertical speed
        self.sideways_drift = random.uniform(-0.07, 0.07)  # Initial sideways drift
        self.max_x_speed = 0.01  # Maximum speed on the x-axis
        self.sideways_drift_limit = 0.5  # Limit for sideways drift
        self.ax = ax
        self.ay = ay
    def update(self, screen):
        if self.speed_y > 0:  # If moving upwards
            self.speed_y -= self.gravity  # Apply gravity
            self.speed_y = max(self.speed_y, 0)  # Stop upward motion at 0
            self.speed_x += self.sideways_drift  # Add sideways drift

        else:  # If moving downwards
            self.speed_y += self.gravity  # Apply gravity
            self.speed_y = min(self.speed_y, self.max_speed_y)  # Limit maximum vertical speed
            self.speed_x *= 0.99  # Apply air resistance to horizontal speed
        #despawn particles once it reaches far from rocket
        if self.rect.y > self.ay + 400:
            self.kill()
        if self.rect.x > self.ax + 200 or self.rect.x < self.ax - 150:
            self.kill()
        #setting limit on how much particles can travel on x-axis 
        if self.rect.x > self.ax+ random.uniform(50,150):
            self.sideways_drift =0
            if self.speed_x >0:
                self.speed_x -=0.05
        if self.rect.x < self.ax- random.uniform(10,100):
            self.sideways_drift =0
            if self.speed_x <0:
                self.speed_x +=0.05
        
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Check if particle hits the sides of the screen and reverse its direction
        if self.rect.left <= 0 or self.rect.right >= screen.get_width():
            self.speed_x *= -1

        if self.rect.bottom >= screen.get_height() - 50:
            self.kill()
'''
            self.speed_y = -0.2
            if self.speed_x >0:
                self.speed_x += 0.13
            if self.speed_x <0:
                self.speed_x -= 0.13
            self.gravity = -0.01
'''

'''
        # Check collision with ground
        if self.rect.bottom >= screen.get_height() - 50:
            self.speed_x *= 0.95  # Reduce horizontal speed on collision
            self.speed_x += random.uniform(-0.1, 0.1)  # Add randomness to horizontal speed
            self.speed_y = -self.speed_y * 0.5  # Reverse and reduce vertical speed
            self.rect.bottom = screen.get_height() - 50  # Adjust position to ground level
  # Adjust position to ground'''
class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.ground_color = WHITE
        self.rocket_color = (50, 50, 50)  # Dark gray color
        self.rocket_width = 50
        self.rocket_height = 100
        self.rocket_x = (screen.get_width() - self.rocket_width) / 2
        self.rocket_y = screen.get_height() - self.rocket_height - 100  # Place rocket above ground level

        self.rocket_on = False  # Flag to indicate if the rocket is turned on
        self.rocket_on_indicator_radius = 5  # Radius of the indicator circle
        self.rocket_on_indicator_color = (255, 0, 0)  # Red color
        self.rocket_on_indicator_pos = (20, 20)  # Position of the indicator circle

        self.particles = pygame.sprite.Group()  # Group to store particles
        self.particle_emit = False
         # 5 seconds in milliseconds

        self.num_stars = 50
        self.star_speed_min = 1
        self.star_speed_max = 5
        self.stars = self.create_stars(self.num_stars, self.star_speed_min, self.star_speed_max)
        self.emit_timer = 0
        self.emit_interval = 20  # Emit particles every 20 milliseconds
    def create_stars(self, num_stars, min_speed, max_speed):
        stars = []
        for _ in range(num_stars):
            x = random.randint(0, self.screen.get_width())
            y = random.randint(0, self.screen.get_height())
            speed = random.randint(min_speed, max_speed)
            stars.append(Star(x, y, speed))
        return stars

    def move_stars(self):
        for star in self.stars:
            star.move()
            if star.y < -10:  # If star moves out of screen, reset its position
                star.y = self.screen.get_height() + 10
                star.x = random.randint(0, self.screen.get_width())

    def draw_stars(self):
        for star in self.stars:
            pygame.draw.circle(self.screen, WHITE, (star.x, star.y), 2)

    def draw_ground(self):
        pygame.draw.rect(self.screen, self.ground_color, (0, self.screen.get_height() - 50, self.screen.get_width(), 50))

    def draw_rocket(self):
        pygame.draw.rect(self.screen, self.rocket_color, (self.rocket_x, self.rocket_y, self.rocket_width, self.rocket_height))

    def draw_rocket_on_indicator(self):
        if self.rocket_on:
            pygame.draw.circle(self.screen, self.rocket_on_indicator_color, self.rocket_on_indicator_pos, self.rocket_on_indicator_radius)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.rocket_on = not self.rocket_on  # Toggle the rocket on/off
                    if self.rocket_on:
                        self.emit_timer = pygame.time.get_ticks()  # Start emit timer
                elif event.key == pygame.K_w:
                    self.particle_emit = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.particle_emit = False

    def emit_particles(self):
        now = pygame.time.get_ticks()
        if self.particle_emit and self.rocket_on and now - self.emit_timer >= self.emit_interval:
            for _ in range(10):  # Emit 20 particles at once
                particle = Particle(random.uniform(self.rocket_x, self.rocket_x + self.rocket_width),
                                    self.rocket_y + self.rocket_height, self.rocket_x, self.rocket_y)
                self.particles.add(particle)
            self.emit_timer = now  # Reset emit timer

    def run(self):
        while True:
            self.handle_events()

            # Fill the screen with black
            self.screen.fill(BLACK)

            # Move and draw stars
            self.move_stars()
            self.draw_stars()

            # Draw ground and rocket
            self.draw_ground()
            self.draw_rocket()

            # Draw rocket on indicator
            self.draw_rocket_on_indicator()

            # Emit particles if necessary
            self.emit_particles()

            # Update and draw particles
            self.particles.update(self.screen)
            self.particles.draw(self.screen)

            # Update the display
            pygame.display.flip()
            self.clock.tick(30)

            
def main():
    # Take a screenshot and save it to a file
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")

    # Initialize Pygame
    pygame.init()

    # Get screen info
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    # Create a fullscreen display
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    # Loading scene
    #loading_scene = LoadingScene(screen, "screenshot.png")
    #loading_scene.run()

    # Menu scene
    menu_scene = MenuScene(screen)
    menu_scene.run()

if __name__ == "__main__":
    main()
