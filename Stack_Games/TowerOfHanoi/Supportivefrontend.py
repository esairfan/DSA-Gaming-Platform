import pygame
import sys
import os
from subprocess import Popen
import time

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Trek")
WHITE = (250, 240, 230)  # Warm off-white (Antique White)
pygame.mixer.init()

# Load sound effect for card flip
button_click = pygame.mixer.Sound("Stack_Games/TowerOfHanoi/Assets/button_click.mp3")

BLACK = (0, 0, 0)
GRAY = (0, 0, 128)
SE = (217, 71, 57)
BG = (250, 236, 204)


FONT = pygame.font.Font("Stack_Games/TowerOfHanoi/Assets/static/EduAUVICWANTPre-Bold.ttf", 36)
FONT1 = pygame.font.Font("Stack_Games/TowerOfHanoi/Assets/static/EduAUVICWANTPre-Bold.ttf", 50)  # Increased font size
FONT1.set_bold(True)  # Set the font to bold

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 70
BUTTON_SPACING = 40

button_texts = ["Easy", "Medium", "Hard"]

button_positions = []
start_x = (SCREEN_WIDTH - (BUTTON_WIDTH * len(button_texts) + BUTTON_SPACING * (len(button_texts) - 1))) // 2
start_y = ((SCREEN_HEIGHT - BUTTON_HEIGHT)+40) // 2  # Keep the y-position in the center

for i in range(len(button_texts)):
    button_x = start_x + i * (BUTTON_WIDTH + BUTTON_SPACING)  # Calculate the x position
    button_y = start_y  # Keep the y position constant
    button_positions.append((button_x, button_y))

def draw_buttons(screen, positions, texts, selected=None):
    for idx, (x, y) in enumerate(positions):
        color = (255, 102, 102) if idx == selected else (217, 71, 57)  # Lighter red for selected, red for default
        pygame.draw.rect(screen, color, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)
        pygame.draw.rect(screen, WHITE, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), 2, border_radius=10)

        text_surface = FONT.render(texts[idx], True, WHITE)  # White text for contrast
        text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2))
        screen.blit(text_surface, text_rect)


def display_loading_screen():
    loading_text = FONT.render("Loading, please wait...", True, SE)  # Use BLACK for text color
    loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill(BG)  # Set background to WHITE
    screen.blit(loading_text, loading_rect)
    pygame.display.flip()  # Update the screen to show the loading message
    time.sleep(2)  # Wait for 2 seconds to simulate loading


def main():
    # Load and scale the background image
    background_image = pygame.image.load("Stack_Games/TowerOfHanoi/Assets/MainBG.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    running = True
    selected_button = None

    while running:
        screen.blit(background_image, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for idx, (x, y) in enumerate(button_positions):
                    if x < mouse_x < x + BUTTON_WIDTH and y < mouse_y < y + BUTTON_HEIGHT:
                        button_click.play()  # Play the sound effect
                        print(f"{button_texts[idx]} selected!")
                        selected_button = idx
                        # Set the number of tiles based on the selected difficulty
                        if button_texts[idx] == "Easy":
                            os.environ["TILE_COUNT"] = "4"  # Set for Easy
                        elif button_texts[idx] == "Medium":
                            os.environ["TILE_COUNT"] = "6"  # Set for Medium
                        elif button_texts[idx] == "Hard":
                            os.environ["TILE_COUNT"] = "8"  # Set for Hard
                        
                        # Display the loading screen before launching the game
                        display_loading_screen()

                        # Launch the main game
                        Popen(['python', 'Stack_Games/TowerOfHanoi/Mainfrontend.py'])
                        pygame.quit()  # Close the difficulty menu window
                        return  # Exit the difficulty menu

        draw_buttons(screen, button_positions, button_texts, selected=selected_button)

        label_surface = FONT1.render("Select Difficulty Level:", True, SE)
        label_rect = label_surface.get_rect(center=(SCREEN_WIDTH // 2, 220))
        screen.blit(label_surface, label_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
