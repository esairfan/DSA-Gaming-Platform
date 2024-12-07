import pygame
import time
from logic import create_grid, is_match, all_matched

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GRID_ROWS = 6
GRID_COLS = 5  # Adjusted to fit the new screen width
CARD_WIDTH = 100
CARD_HEIGHT = 80
PADDING = 5
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Load assets
ASSETS_FOLDER = "Array_Games/Memory_Match/Assets/"
CARD_BACK = pygame.image.load(ASSETS_FOLDER + "cardbackground.png")
ITEMS = [
    "apple", "bird", "brinjal", "candle", "candy",
    "cherry", "cookie", "grape", "heart", "lolly",
    "mushroom", "pepper", "santa", "snake", "snow"
]
ITEM_IMAGES = {item: pygame.image.load(ASSETS_FOLDER + f"{item}.png") for item in ITEMS}


def draw_grid(screen, grid, revealed, matched, remaining_cards):
    """Draw the game grid with separated cards.""" 
    screen.fill(WHITE)

    # Display remaining cards counter
    font = pygame.font.Font(None, 36)
    text = font.render(f"Remaining Cards: {remaining_cards}", True, BLACK)
    screen.blit(text, (20, 20))

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * (CARD_WIDTH + PADDING) + PADDING
            y = row * (CARD_HEIGHT + PADDING) + 60  # Offset for card counter

            if matched[row][col]:
                # Card is matched (disappeared)
                pygame.draw.rect(screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT))
            elif revealed[row][col]:
                # Show the front of the card
                pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))  # Background
                screen.blit(ITEM_IMAGES[grid[row][col]], (x, y))
                pygame.draw.rect(screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 2)  # Border
            else:
                # Show the back of the card
                card_back = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
                pygame.draw.rect(card_back, WHITE, (0, 0, CARD_WIDTH, CARD_HEIGHT), border_radius=10)
                screen.blit(card_back, (x, y))
                screen.blit(CARD_BACK, (x, y))

            # Optional: Draw a border around the card for better separation
            pygame.draw.rect(screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 3)  # Border around each card


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Memory Match")
    clock = pygame.time.Clock()

    # Create grid and game states
    grid = create_grid(GRID_ROWS, GRID_COLS)
    revealed = [[False] * GRID_COLS for _ in range(GRID_ROWS)]
    matched = [[False] * GRID_COLS for _ in range(GRID_ROWS)]
    remaining_cards = GRID_ROWS * GRID_COLS

    first_click = None
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                col = pos[0] // (CARD_WIDTH + PADDING)
                row = (pos[1] - 60) // (CARD_HEIGHT + PADDING)

                if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS and not revealed[row][col] and not matched[row][col]:
                    revealed[row][col] = True

                    if first_click is None:
                        first_click = (row, col)
                    else:
                        # Second click
                        second_click = (row, col)
                        if is_match(grid, first_click, second_click):
                            matched[first_click[0]][first_click[1]] = True
                            matched[second_click[0]][second_click[1]] = True
                            remaining_cards -= 2
                        else:
                            # Pause to show mismatched pair
                            draw_grid(screen, grid, revealed, matched, remaining_cards)
                            pygame.display.update()
                            time.sleep(1)

                            # Flip the cards back
                            revealed[first_click[0]][first_click[1]] = False
                            revealed[second_click[0]][second_click[1]] = False

                        first_click = None

        # Check if all pairs are matched
        if all_matched(matched):
            game_over = True

        # Draw the grid
        draw_grid(screen, grid, revealed, matched, remaining_cards)
        pygame.display.update()
        clock.tick(FPS)

    # End of game
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("You Win!", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    time.sleep(3)
    pygame.quit()


if __name__ == "__main__":
    main()
