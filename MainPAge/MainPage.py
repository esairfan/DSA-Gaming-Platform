import pygame
import sys

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
BUTTONTEXTCOLOR = (63, 226, 178)
# Define button class
class Button:
    def __init__(self, x, y, width, height, text, bg_color, text_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)  # You can use any font here
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, screen):
        # Create a transparent background for the button (fully transparent)
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        button_surface.fill(self.bg_color)  # Fill with transparent color

        # Draw the text on top of the transparent background
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Blit the button and text onto the screen
        screen.blit(button_surface, self.rect)
        screen.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
start_button = Button(40, 575, 265, 90, 'Start ', (0, 0, 0, 0), BUTTONTEXTCOLOR)  # Transparent
aboutUs_button = Button(377, 575, 265, 90, 'About Us', (0, 0, 0, 0), BUTTONTEXTCOLOR)  # Transparent
help_button = Button(730, 575, 265, 90, 'Help', (0, 0, 0, 0), BUTTONTEXTCOLOR)  # Transparent
exit_button = Button(1073, 575, 265, 90, 'Exit', (0, 0, 0, 0), BUTTONTEXTCOLOR)  # Transparent

def StartGame():
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Image Example")

    # Load and scale the image
    image_path = 'Assets/MainPage.png'  # Change this to the path of your image file
    image = pygame.image.load(image_path)

    # Scale the image if necessary (optional)
    image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Adjust the size as needed

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press Esc to quit the game
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button click
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.is_clicked(mouse_pos):
                        print("Start Game button clicked")
                    elif exit_button.is_clicked(mouse_pos):
                        print("Exit button clicked")
                        running = False# Exit the game
                    elif aboutUs_button.is_clicked(mouse_pos):
                        print("About Us button clicked")
                    elif help_button.is_clicked(mouse_pos):
                        print("Help button clicked")
                        running = False

        # Draw the image at the specified position
        screen.blit(image, (0, 0))

        # Draw the buttons
        start_button.draw(screen)
        aboutUs_button.draw(screen)
        help_button.draw(screen)
        exit_button.draw(screen)

        # Update the screen
        pygame.display.flip()

def Help():
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Image Example")
    
        # Main game loop
if __name__ == "__main__":
    StartGame()
    pygame.quit()
    sys.exit()
