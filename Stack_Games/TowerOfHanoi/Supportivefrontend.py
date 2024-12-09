import pygame
import sys
import os
from subprocess import Popen
import time

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Select Difficulty Level")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

FONT = pygame.font.Font(None, 36)

BUTTON_WIDTH, BUTTON_HEIGHT = 150, 40
BUTTON_SPACING = 20

button_texts = ["Easy", "Medium", "Hard"]

button_positions = []
start_y = (SCREEN_HEIGHT - (BUTTON_HEIGHT * len(button_texts) + BUTTON_SPACING * (len(button_texts) - 1))) // 2
for i in range(len(button_texts)):
    button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
    button_y = start_y + i * (BUTTON_HEIGHT + BUTTON_SPACING)
    button_positions.append((button_x, button_y))


def draw_buttons(screen, positions, texts, selected=None):
    for idx, (x, y) in enumerate(positions):
        color = GRAY if idx == selected else WHITE
        pygame.draw.rect(screen, color, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, BLACK, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)

        text_surface = FONT.render(texts[idx], True, BLACK)
        text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2))
        screen.blit(text_surface, text_rect)


def display_loading_screen():
    loading_text = FONT.render("Loading, please wait...", True, BLACK)
    loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill(WHITE)
    screen.blit(loading_text, loading_rect)
    pygame.display.flip()  # Update the screen to show the loading message
    time.sleep(5)  # Wait for 1 second to simulate loading (this can be adjusted)


def main():
    running = True
    selected_button = None

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for idx, (x, y) in enumerate(button_positions):
                    if x < mouse_x < x + BUTTON_WIDTH and y < mouse_y < y + BUTTON_HEIGHT:
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

        label_surface = FONT.render("Select Difficulty Level:", True, BLACK)
        label_rect = label_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(label_surface, label_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
