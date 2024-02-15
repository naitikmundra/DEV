import pygame
import sys
import pyautogui
import random
import math
# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)

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



class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.buttons = [
            Button("New Game", self.font, 0, 0, 200, 50, GRAY, LIGHT_GRAY),
            Button("Options", self.font, 0, 0, 200, 50, GRAY, LIGHT_GRAY),
            Button("Quit", self.font, 0, 0, 200, 50, GRAY, LIGHT_GRAY)
        ]
        self.arrange_buttons()
        self.blur_amount = 10  # Adjust the blur amount as needed
        self.shutter_height = 100
        self.shutter_speed = 25
        self.shutter_pos = -self.shutter_height 

        # Create a smaller surface for rendering the effects
        self.xyz_surface = pygame.Surface((600, 400))  # Adjust the size as needed
        self.xyz_surface.fill(BLACK)

        # Chain parameters
        self.chain_length = 200  # Length of the chain
        self.chain_color = (150, 150, 150)  # Color of the chain
        self.chain_thickness = 3  # Thickness of the chain
        self.chain_angle = 33  # Initial angle of the swinging chain
        self.chain_rotation_speed = 0.005  # Speed of rotation
        self.chain_origin_x = self.screen.get_width() // 2  # X coordinate of the chain's attachment point (middle of the screen)
        self.chain_origin_y = 0  # Y coordinate of the chain's attachment point
        self.chain_amplitude = 300  # Amplitude of the swinging motion
        self.chain_swing_speed = 0.001  # Speed of swinging
        self.xyz_pos = (self.chain_origin_x - self.xyz_surface.get_width() // 2, self.chain_origin_y - self.xyz_surface.get_height())  # Position of the XYZ monitor

    def arrange_buttons(self):
        total_button_height = sum(button.height for button in self.buttons) + (len(self.buttons) - 1) * 20
        y_offset = (self.screen.get_height() - total_button_height) / 2
        for button in self.buttons:
            button.x = (self.screen.get_width() - button.width) / 2
            button.y = y_offset
            y_offset += button.height + 20
            button.rect = pygame.Rect(button.x, button.y, button.width, button.height)

    def draw_tv_static(self):
        # Draw TV static effect with reduced brightness
        for y in range(0, self.xyz_surface.get_height(), 5):
            for x in range(0, self.xyz_surface.get_width(), 5):
                if random.random() < 0.1:  # Adjust the density of static
                    color = BLACK if random.random() < 0.5 else LIGHT_GRAY
                    pygame.draw.rect(self.xyz_surface, color, (x, y, 5, 5))
        
        # Draw broken screen-like lines (vertical)
        for _ in range(10):  # Adjust the number of lines as needed
            color = random.choice([(255, 0, 0), (0, 255, 255), (255, 0, 255)])  # Choose from different colors
            start_x = random.randint(self.xyz_surface.get_width() * 9 // 10, self.xyz_surface.get_width() - 50)
            end_x = start_x  # Ensure the line is straight by keeping the x-coordinate the same
            start_y = 0
            end_y = self.xyz_surface.get_height()
            start_x += random.randint(-20, 20)  # Randomly move the line to the left or right
            end_x += random.randint(-20, 20)    # Randomly move the line to the left or right
            pygame.draw.line(self.xyz_surface, color, (start_x, start_y), (end_x, end_y), random.randint(1, 3))  # Adjust line thickness
        
        # Draw rolling shutter effect
        self.shutter_pos += self.shutter_speed
        if self.shutter_pos >= self.xyz_surface.get_height():
            self.shutter_pos = -self.shutter_height
        pygame.draw.rect(self.xyz_surface, WHITE, (0, self.shutter_pos, self.xyz_surface.get_width(), self.shutter_height))

        # Draw blinking error message
        error_font = pygame.font.Font(None, 40)
        error_text = error_font.render("Error: System malfunction", True, (255, 0, 0))
        error_rect = error_text.get_rect()
        error_rect.topleft = (50, 50)
        if pygame.time.get_ticks() % 1000 < 500:  # Make the text blink every 500 milliseconds
            self.xyz_surface.blit(error_text, error_rect)

    def draw_swinging_chain(self):
        # Update chain angle
        self.chain_angle += self.chain_rotation_speed

        # Calculate swinging motion
        offset = self.chain_amplitude * math.sin(self.chain_swing_speed * pygame.time.get_ticks())
        swing_x = self.chain_origin_x + offset
        swing_y = self.chain_origin_y + self.chain_length

        # Draw chain
        pygame.draw.line(self.screen, self.chain_color, (swing_x, swing_y), (swing_x, swing_y - self.chain_length), self.chain_thickness)

        # Update XYZ monitor position
        self.xyz_pos = (swing_x - self.xyz_surface.get_width() // 2, swing_y)  # Adjusted to align with the chain

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in self.buttons:
                    button.update(event)

            # Draw black background
            self.screen.fill(BLACK)



            # Draw XYZ rectangle with effects
            self.draw_tv_static()
            self.screen.blit(self.xyz_surface, self.xyz_pos)
            # Draw swinging chain
            self.draw_swinging_chain()
            # Draw buttons
            for button in self.buttons:
                button.draw(self.screen)

            # Update the display
            pygame.display.flip()


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
