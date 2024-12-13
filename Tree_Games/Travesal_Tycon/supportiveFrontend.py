import pygame
import sys
import time
from subprocess import call
 
pygame.init()
 
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Traversal Tree")
 
WHITE = (250, 240, 230)  
BLACK = (0, 0, 0)
SE = (217, 71, 57) 
BG = (250, 236, 204)  # Background color
HOVER_COLOR = (255, 102, 102)  # Button hover color

# Fonts
FONT = pygame.font.Font(None, 36)
FONT1 = pygame.font.Font(None, 50)  # Larger font for title
FONT1.set_bold(True)

# Button dimensions and setup
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 70
BUTTON_SPACING = 40

button_texts = ["Post Order", "Pre Order", "In Order"]
button_positions = []
start_x = (SCREEN_WIDTH - (BUTTON_WIDTH * len(button_texts) + BUTTON_SPACING * (len(button_texts) - 1))) // 2
start_y = ((SCREEN_HEIGHT - BUTTON_HEIGHT) + 40) // 2

for i in range(len(button_texts)):
    button_x = start_x + i * (BUTTON_WIDTH + BUTTON_SPACING)
    button_y = start_y
    button_positions.append((button_x, button_y))


def draw_buttons(screen, positions, texts, hovered_idx=None):
    """Draw buttons with hover effects."""
    for idx, (x, y) in enumerate(positions):
        color = HOVER_COLOR if idx == hovered_idx else SE
        pygame.draw.rect(screen, color, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)
        pygame.draw.rect(screen, WHITE, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), 2, border_radius=10)

        text_surface = FONT.render(texts[idx], True, WHITE)
        text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2))
        screen.blit(text_surface, text_rect)


def display_loading_screen():
    """Display a loading screen."""
    loading_text = FONT.render("Loading, please wait...", True, SE)
    loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill(BG)
    screen.blit(loading_text, loading_rect)
    pygame.display.flip()
    time.sleep(2)


def main():
    """Main function to handle the menu loop."""
    running = True
    hovered_button = None
    traversal_type = None

    while running:
        screen.fill(BG)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hovered_button is not None:
                    traversal_type = button_texts[hovered_button]
                    print(f"{traversal_type} selected!")
                    display_loading_screen()

                    # Call the logic for the selected traversal and pass it to the main frontend
                    call(["python", "Tree_Games/Travesal_Tycon/mainFrontend.py", traversal_type])

                    running = False

        # Check hover
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_button = None
        for idx, (x, y) in enumerate(button_positions):
            if x < mouse_x < x + BUTTON_WIDTH and y < mouse_y < y + BUTTON_HEIGHT:
                hovered_button = idx
                break

        # Draw elements
        draw_buttons(screen, button_positions, button_texts, hovered_idx=hovered_button)

        label_surface = FONT1.render("Select Order Level:", True, SE)
        label_rect = label_surface.get_rect(center=(SCREEN_WIDTH // 2, 220))
        screen.blit(label_surface, label_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
