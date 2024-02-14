import pygame
import sys
import pyautogui
import random
import time

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)

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

        # Initialize graph line parameters
        self.graph_line_color = RED
        self.graph_line_thickness = 2
        self.graph_line_length = 0
        self.graph_line_max_length = self.screen.get_width()  # Maximum length of the graph line
        self.graph_line_y = 0  # Initial y-coordinate of the graph line
        self.graph_line_speed = 3
        self.graph_line_points = [(0, self.graph_line_y)] 
    def arrange_buttons(self):
        total_button_height = sum(button.height for button in self.buttons) + (len(self.buttons) - 1) * 20
        y_offset = (self.screen.get_height() - total_button_height) / 2
        for button in self.buttons:
            button.x = (self.screen.get_width() - button.width) / 2
            button.y = y_offset
            y_offset += button.height + 20
            button.rect = pygame.Rect(button.x, button.y, button.width, button.height)

    def update_graph_line(self):
        # Update graph line parameters for animation
        self.graph_line_length += self.graph_line_speed
        # Check if the end of the x-axis is reached
        if self.graph_line_length >= self.graph_line_max_length:
            # Reset the graph line
            self.graph_line_length = 0
            self.graph_line_y = 0  # Reset y-coordinate to the middle of the screen
            self.graph_line_points = [(0, self.graph_line_y)]
        # Calculate the next x-coordinate based on the current length
        next_x = self.graph_line_length
        print(self.graph_line_y)
        # Calculate the next y-coordinate for falling only
        next_y = self.graph_line_y + random.randint(1, 3)  # Random downward movement
        self.graph_line_y += next_y - self.graph_line_y
        # Ensure the y-coordinate stays within the screen boundaries
        next_y = min(max(next_y, 0), self.screen.get_height() - 1)
        # If the end of the x-axis is reached, make the line fall to the bottom of the screen
        if next_x >= self.graph_line_max_length:
            next_x = self.graph_line_max_length - 1  # Ensure the line reaches the end of x-axis
            next_y = self.screen.get_height() - 1  # Make the line fall to the bottom of the screen

        # Add the new point to the graph line
        self.graph_line_points.append((next_x, next_y))
    def draw_graph_line(self):
       
        pygame.draw.lines(self.screen, self.graph_line_color, False, self.graph_line_points, self.graph_line_thickness)

    def run(self):
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in self.buttons:
                    button.update(event)

            # Update graph line
            self.update_graph_line()

            # Fill the screen with black
            self.screen.fill(BLACK)

            # Draw the animated graph line
            self.draw_graph_line()

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