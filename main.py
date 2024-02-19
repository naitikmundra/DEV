import pygame
import sys
import pyautogui
import random
from pygame.locals import *
import math

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
RED_TRANSPARENT = (255, 0, 0, 128)  # Semi-transparent red color
#GLOBAL
sounds_folder = "library/sounds/"
images_folder = "library/visual/"
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
    def __init__(self, x, y, speed,radius, rocket=False):
        self.x = x
        self.y = y
        self.speed = speed
        self.rocket = rocket
        self.radius = radius
    def move(self):
     if not self.rocket:
        self.y -= self.speed
     else:
        self.y += self.speed

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
            star_radius = 2
            if random.random() < 0.1:
                star_radius = 10
            stars.append(Star(x, y, speed,star_radius))
        return stars

    def move_stars(self):
        for star in self.stars:
            star.move()
            if star.y < -10:  # If star moves out of screen, reset its position
                star.y = self.screen.get_height() + 10
                star.x = random.randint(0, self.screen.get_width())

    def draw_stars(self):
        for star in self.stars:

            pygame.draw.circle(self.screen, WHITE, (star.x, star.y), star.radius)


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
        
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA | pygame.HWSURFACE)  # Set SRCALPHA flag for per-pixel alpha
        self.color = (255, 255, 0, 255)  # Yellow color with some transparency
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = random.uniform(-0.1, 0.1)  # Random horizontal speed
        self.speed_y = random.uniform(1, 2)  # Adjusted initial upward speed
        self.gravity = 2  # Gravity to simulate downward acceleration
        self.max_speed_y = 10  # Maximum vertical speed
        self.sideways_drift = random.uniform(-0.09, 0.09)  # Initial sideways drift
        self.max_x_speed = 0.01  # Maximum speed on the x-axis
        self.sideways_drift_limit = 0.5  # Limit for sideways drift
        self.ax = ax
        self.ay = ay
    def update(self, screen):
        pygame.draw.circle(self.image, self.color, (2, 2), 20)
        if self.speed_y > 0:  # If moving upwards
            self.speed_y -= self.gravity  # Apply gravity
            self.speed_y = max(self.speed_y, 0)  # Stop upward motion at 0
            self.speed_x += self.sideways_drift  # Add sideways drift

        else:  # If moving downwards
            self.speed_y += self.gravity  # Apply gravity
            self.speed_y = min(self.speed_y, self.max_speed_y)  # Limit maximum vertical speed
            self.speed_x *= 0.99  # Apply air resistance to horizontal speed
        #despawn particles once it reaches far from rocket
        
        if self.rect.y > self.ay + 300:
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
        self.particles_hit_ground = 0  # Track the number of particles hitting the ground
        self.rocket_moving_up = False  # Flag to indicate if the rocket is moving upwards
        self.rocket_velocity = -2 # Initial velocity
        self.acceleration = 0.03  # Acceleration rate
        self.gravitic_accelaration = 0.1  # Acceleration rate
        self.power_on = pygame.mixer.Sound(sounds_folder +"power.mp3")
        self.power_on2 = pygame.mixer.Sound(sounds_folder +"switch.mp3")
        self.rocket_abovethreshold = False
        # GUI
        self.gui_image = pygame.image.load(images_folder+"gui.png").convert_alpha()  # Load GUI image
        self.gui_image2 = pygame.image.load(images_folder+"gui2.png").convert_alpha()  # Load GUI image

        self.gui_image = pygame.transform.scale(self.gui_image, (screen.get_width(), screen.get_height()))  # Resize GUI image to match screen dimensions
        self.gui_rect = self.gui_image.get_rect()  # Position GUI image
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)
        # Horizontal movement variables
        self.rocket_horizontal_velocity = 0
        self.rocket_horizontal_acceleration = 0.1
        self.max_horizontal_speed = 5
        self.rocket_rotation_angle = 0  # Initial tilt angle
        self.rocket_rotation_speed = 2  # Rotation speed in degrees per frame
        self.max_rotation_angle = 40  # Maximum rotation angle in degrees
        self.speedometer_color = YELLOW  # Color of the speedometer rectangle
        self.speedometer_width = 10  # Width of the speedometer rectangle
        self.speedometer_length = 100  # Length of the speedometer rectangle
        self.speedometer_x = 20  # X-coordinate of the speedometer rectangle
        self.speedometer_y = screen.get_height() - self.speedometer_length - 20  # Y-coordinate of the speedometer rectangle
        self.max_velocity = 20  # Maximum velocity of the rocket
        # Define variables for adjusting the position of the speedometer
        self.speedometer_x = screen.get_width()/1.105  # X-coordinate of the speedometer
        self.speedometer_y = screen.get_height()/1.25  # Y-coordinate of the speedometer
        self.groundremover = 50 #SLOWLY erase ground
        # Inside the GameScene's __init__ method, add the following attributes
        self.alert_duration = 500  # Duration of each state in milliseconds
        self.alert_timer = 0  # Timer to track the duration of each state
        self.alert_state = False  # Flag to track the current state of the alert effect
        self.rocket_exhaust_sound = pygame.mixer.Sound(sounds_folder +"rocket_exhaust.wav")  # Load the rocket exhaust sound file
        self.rocket_sound_playing = False  # Flag to track whether the rocket exhaust sound is playing
        self.alert_sound = pygame.mixer.Sound(sounds_folder +"alert.wav")  # Load the alert sound file
        self.alert_sound.set_volume(0.9)  # Adjust the volume of the alert sound
        self.rocket_image = pygame.image.load(images_folder+"rocket.png").convert_alpha()
        self.rocket_image = pygame.transform.scale(self.rocket_image, (self.rocket_width, self.rocket_height))

        # Adjust the volume of the rocket exhaust sound
        self.rocket_exhaust_sound.set_volume(0.5)
        self.distance_travelled= 0
        # Fuel wheel valve parameters
        self.circle_radius = 150
        self.circle_center = (screen.get_width() /1.2, screen.get_height()/1.25)

        # Plus symbol parameters
        self.plus_length = self.circle_radius * 2
        self.plus_width = 10
        self.plus_color = WHITE

        # Angle for rotation
        self.angle = 0
        self.scroll_value = 0

        # Stiffness factor
        self.stiffness = 0.02
        self.scroll_sound = pygame.mixer.Sound(sounds_folder+"valve.mp3")

    def draw_fuelwheel(self):
        # Calculate the positions of the ends of the plus symbol
        plus_end1 = (self.circle_center[0] + self.plus_length/2 * math.cos(self.angle), self.circle_center[1] + self.plus_length/2 * math.sin(self.angle))
        plus_end2 = (self.circle_center[0] + self.plus_length/2 * math.cos(self.angle + math.pi), self.circle_center[1] + self.plus_length/2 * math.sin(self.angle + math.pi))
        plus_end3 = (self.circle_center[0] + self.plus_length/2 * math.cos(self.angle + math.pi/2), self.circle_center[1] + self.plus_length/2 * math.sin(self.angle + math.pi/2))
        plus_end4 = (self.circle_center[0] + self.plus_length/2 * math.cos(self.angle - math.pi/2), self.circle_center[1] + self.plus_length/2 * math.sin(self.angle - math.pi/2))

        # Draw the plus symbol
        pygame.draw.line(self.screen, self.plus_color, plus_end1, plus_end2, self.plus_width)
        pygame.draw.line(self.screen, self.plus_color, plus_end3, plus_end4, self.plus_width)

        # Draw circle
        pygame.draw.circle(self.screen, WHITE, self.circle_center, self.circle_radius, 2)

    def draw_speedometer(self):
        # Calculate the angle of rotation based on the rocket's velocity
        angle = self.rocket_velocity / self.max_velocity * 90  # Convert velocity to angle (assuming 0 to 90 degrees)

        # Define the dimensions of the speedometer
        speedometer_width = 20
        speedometer_length = 100

        # Calculate the position of the fixed bottom part of the speedometer (circle)
        bottom_part_center = (self.speedometer_x + speedometer_width / 2, self.speedometer_y + speedometer_length)

        # Draw the fixed bottom part of the speedometer (circle)
        pygame.draw.circle(self.screen, self.speedometer_color, bottom_part_center, speedometer_width // 2)

        # Calculate the position of the moving part of the speedometer (rectangle/needle)
        needle_length = 50  # Length of the needle
        needle_width = 5  # Width of the needle
        needle_center = bottom_part_center  # Position the needle center at the bottom part center

        # Calculate the end point of the needle based on the angle of rotation
        needle_end_x = needle_center[0] + needle_length * math.cos(math.radians(angle))
        needle_end_y = needle_center[1] - needle_length * math.sin(math.radians(angle))

        # Draw the needle
        pygame.draw.line(self.screen, self.speedometer_color, needle_center, (needle_end_x, needle_end_y), needle_width)

    def alert(self):

        # Inside the GameScene's run method, after updating the rocket position
        self.alert_timer += self.clock.get_time()  # Increment the alert timer

        # Check if it's time to change the alert state
        if self.alert_timer >= self.alert_duration:
            self.alert_state = not self.alert_state  # Toggle the alert state
            self.alert_timer = 0  # Reset the timer
        if not self.rocket_moving_up and self.alert_state:
         if self.rocket_abovethreshold and self.rocket_velocity < 0:
            self.alert_sound.play()  
            # Create a semi-transparent red surface
            overlay_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            overlay_surface.fill((255, 0, 0, 50))  # Fill with semi-transparent red color (R, G, B, Alpha)

            # Blit the overlay surface onto the screen
            self.screen.blit(overlay_surface, (0, 0))
        else:
            self.alert_sound.stop() 

    def fps_counter(self):
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps , 1, pygame.Color("RED"))
        self.screen.blit(fps_t,(0,0))
        score = self.font.render(str(int(self.distance_travelled)) , 1, pygame.Color("YELLOW"))
        self.screen.blit(score,(0,20))
    def draw_gui(self):
        if self.rocket_on:
            self.screen.blit(self.gui_image, self.gui_rect)
        else:
            self.screen.blit(self.gui_image2, self.gui_rect)
    def create_stars(self, num_stars, min_speed, max_speed):
        stars = []
        for _ in range(num_stars):
            x = random.randint(0, self.screen.get_width())
            y = random.randint(0, self.screen.get_height())
            speed = random.randint(min_speed, max_speed)
            star_radius = 2
            if random.random() < 0.3:
                star_radius = 10
            stars.append(Star(x, y, speed,star_radius))
        return stars
    # Define a function to check collision between rocket and star
    def check_collision(self,rocket_x, rocket_y, rocket_radius, star_x, star_y, star_radius):
        # Calculate the closest point on the rectangle to the center of the circle
        closest_x = max(rocket_x, min(star_x, rocket_x + self.rocket_width))
        closest_y = max(rocket_y, min(star_y, rocket_y + self.rocket_height))
        distance = math.sqrt((closest_x - star_x) ** 2 + (closest_y - star_y) ** 2)
        # Check if the distance is less than or equal to the circle's radius
        if distance <= star_radius and self.rocket_abovethreshold:
            return True
        # Check if any of the rectangle's edges intersect with the circle
        
        return False
    def move_stars(self):
        for star in self.stars:
            star.move()
            # Check collision between rocket and star
            if self.check_collision(self.rocket_x, self.rocket_y, self.rocket_width / 2, star.x, star.y, 2):
                if star.radius==10:
                    pygame.quit()
            if self.rocket_moving_up: #change star movement to create miraj
                star.rocket = True
                star.speed = self.rocket_velocity
                    
                    
            
            else:
                
                if self.rocket_velocity < 0:
                    star.rocket = False
                    star.speed = -self.rocket_velocity
                    
                else:
                    
                        star.speed = self.rocket_velocity
            if self.rocket_velocity < 0:
                
                self.distance_travelled +=self.rocket_velocity
            else:
                self.distance_travelled +=self.rocket_velocity
   
            if self.rocket_y < self.screen.get_height() - 350:
                
                self.rocket_abovethreshold = True
                self.groundremover -= 1
            if star.y < -10:  # If star moves out of screen, reset its position
                star.y = self.screen.get_height() + 10
                star.x = random.randint(0, self.screen.get_width())
            
            if star.y > self.screen.get_height() + 10:  # If star moves out of screen, reset its position
                star.y = -10
                star.x = random.randint(0, self.screen.get_width())
            if self.rocket_horizontal_velocity < 0:
                if self.rocket_velocity > 0: 
                    star.x -= star.speed
            elif self.rocket_horizontal_velocity > 0:
                if self.rocket_velocity > 0:
                    star.x += star.speed

            if star.x < -10:
                star.x = self.screen.get_width() + 10
                star.y = random.randint(0, self.screen.get_height())
            elif star.x > self.screen.get_width() + 10:
                star.x = -10
                star.y = random.randint(0, self.screen.get_height())

    def draw_stars(self):
        for star in self.stars:
            pygame.draw.circle(self.screen, WHITE, (star.x, star.y), star.radius)
            self.screen.blit(self.circle_surf(8, (20,20,60)),(star.x -5,star.y-5), special_flags=BLEND_RGB_ADD)#adding glow to stars
    def circle_surf(self,radius, color):
        surf = pygame.Surface((radius * 2 , radius * 2))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf
    def draw_ground(self):
        pygame.draw.rect(self.screen, self.ground_color, (0, self.screen.get_height() - self.groundremover, self.screen.get_width(), 50))

    def draw_rocket(self):
        # Load the rocket image

        # Scale the rocket image to match the width and height

        # Rotate the rocket image
        rotated_rocket = pygame.transform.rotate(self.rocket_image, self.rocket_rotation_angle)

        # Get the rect of the rotated surface
        rotated_rect = rotated_rocket.get_rect(center=(self.rocket_x + self.rocket_width / 2, self.rocket_y + self.rocket_height / 2))

        # Update the rotation angle
        self.rocket_rotation_angle += self.rocket_horizontal_velocity * self.rocket_rotation_speed
        self.rocket_rotation_angle = max(-self.max_rotation_angle, min(self.max_rotation_angle, self.rocket_rotation_angle))  # Limit rotation angle

        # Draw the rotated rocket
        self.screen.blit(rotated_rocket, rotated_rect)
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
                    self.power_on2.play()
                    if self.rocket_on:
                        if self.rocket_velocity != 0:
                             self.rocket_moving_up = False
                    else:
                        self.power_on.play()
                    self.rocket_on = not self.rocket_on  # Toggle the rocket on/off
                    
                elif event.key == pygame.K_w and self.rocket_on:
                    self.particle_emit = True
                    self.rocket_moving_up = True  # Start moving the rocket upwards when "W" is pressed
                    # Play the rocket exhaust sound if it's not already playing
                    if not self.rocket_sound_playing:
                        self.rocket_exhaust_sound.play(-1)
                        self.rocket_sound_playing = True 
                elif event.key == pygame.K_w and not self.rocket_on:
                    self.rocket_moving_up = False
                elif event.key == pygame.K_a and self.rocket_on:
                    # Move rocket left
                    self.rocket_horizontal_velocity = self.max_horizontal_speed

                elif event.key == pygame.K_d and self.rocket_on:
                    # Move rocket right
                    self.rocket_horizontal_velocity = -self.max_horizontal_speed
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.particle_emit = False
                    self.rocket_moving_up = False  # Stop moving the rocket
                    # Stop playing the rocket exhaust sound
                    self.rocket_exhaust_sound.stop()
                    self.rocket_sound_playing = False  # Reset the flag
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    # Stop horizontal movement
                    self.rocket_horizontal_velocity = 0
                    self.rocket_rotation_angle = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
             if self.rocket_on:
                mouse_pos = pygame.mouse.get_pos()
                distance = math.sqrt((mouse_pos[0] - self.circle_center[0])**2 + (mouse_pos[1] - self.circle_center[1])**2)
                if distance <= self.circle_radius:
                    if event.button == 4:  # Scroll Up
                        if self.scroll_value > 0:
                            self.scroll_sound.play()
                            self.angle -= math.pi / 18 * self.stiffness * self.scroll_value  # Rotate clockwise with stiffness
                            self.scroll_value -= 1
                    elif event.button == 5:  # Scroll Down
                        if self.scroll_value < 100:
                            self.scroll_sound.play()
                            self.angle += math.pi / 18 * self.stiffness * self.scroll_value  # Rotate anti-clockwise with stiffness
                            self.scroll_value += 1
    def update(self):
            self.rocket_velocity = max(-self.max_velocity, min(self.max_velocity, self.rocket_velocity))

            # Move the rocket upwards continuously while "W" is held down and the rocket is turned on
            if self.rocket_moving_up and self.rocket_on:
              
                self.rocket_velocity += self.acceleration 

                # Move the rocket based on its velocity
                if not self.rocket_abovethreshold: #only move rocket to certain limit on screen
                    self.rocket_y -= self.rocket_velocity
                    
                
                # Stop moving the rocket upwards if it reaches the top
                if self.rocket_y <= 0:
                    self.rocket_moving_up = False

            # Apply gravity when the rocket is not moving upwards
            if not self.rocket_moving_up:
                # Apply gravity to the rocket
                self.rocket_velocity -= self.gravitic_accelaration  # Decrease velocity due to gravity
                if self.rocket_velocity < -20:
                    pygame.quit()
                # Move the rocket based on its velocity
                if not self.rocket_abovethreshold:
                    self.rocket_y -= self.rocket_velocity

                # Ensure that the rocket stays within the screen boundaries
            if self.rocket_y >= self.screen.get_height() - self.rocket_height - 50:
                    self.rocket_y = self.screen.get_height() - self.rocket_height - 50
                    self.rocket_velocity = 0  # Stop the rocket when it reaches the ground

            
    def emit_particles(self):
        now = pygame.time.get_ticks()
        if self.particle_emit and self.rocket_on:
            for _ in range(20):  # Emit 20 particles at once
                # Calculate the offset from the rocket's position based on its rotation angle
                offset_distance = random.uniform(0, 20)  # Example offset distance
                offset_angle = random.uniform(-10, 10)  # Example offset angle
                
                # Convert offset angle to radians
                offset_angle_radians = math.radians(self.rocket_rotation_angle + offset_angle)

                # Calculate the offset components using trigonometry
                offset_x = offset_distance * math.sin(offset_angle_radians)
                offset_y = offset_distance * math.cos(offset_angle_radians)
                if self.rocket_rotation_angle > 0:
                    offset_x += self.rocket_rotation_angle - 10
                    offset_y -= self.rocket_rotation_angle - 30
                if self.rocket_rotation_angle < 0:
                    offset_x -= -self.rocket_rotation_angle - 10
                    offset_y += self.rocket_rotation_angle + 30

                # Adjust the x-coordinate to emit particles from the entire base of the rocket
                particle_x = random.uniform(self.rocket_x, self.rocket_x + self.rocket_width)

                # Spawn the particle at the calculated position relative to the rocket's base
                particle = Particle(particle_x + offset_x, self.rocket_y + self.rocket_height + offset_y, self.rocket_x, self.rocket_y)
                self.particles.add(particle)
            self.emit_timer = now  # Reset emit timer

        

                
    def run(self):
        while True:
            self.handle_events()
            self.update()

            # Fill the screen with black
            self.screen.fill(BLACK)

            # Move and draw stars
            self.move_stars()
            self.draw_stars()

            # Draw ground and rocket
            if self.groundremover > 0:
                self.draw_ground()
            self.draw_rocket()

            # Draw rocket on indicator
            self.draw_rocket_on_indicator()

            # Emit particles if necessary
            self.emit_particles()
            # Update and draw particles
            self.particles.update(self.screen)
            self.particles.draw(self.screen)
            # Draw GUI
            self.draw_gui()
            self.draw_speedometer()
            self.fps_counter()
            self.alert()
            self.draw_fuelwheel()
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
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.DOUBLEBUF)

    # Loading scene
    #loading_scene = LoadingScene(screen, "screenshot.png")
    #loading_scene.run()

    # Menu scene
    menu_scene = MenuScene(screen)
    menu_scene.run()

if __name__ == "__main__":
    main()
