import pygame
import logic

# Initialize the game window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Memory Match Game')

# Define colors for UI
colors = {
    'back': (0, 128, 255),    # Blue for the back of the card
    'flipped': (0, 255, 0),   # Green for flipped cards
    'text': (255, 255, 255),   # White text for symbols
}

# Initialize the font
pygame.font.init()
font = pygame.font.Font(None, 36)

# Function to display the game
def game_loop():
    cards = logic.create_grid()  # Get the shuffled cards
    flipped_cards = []  # List to track flipped cards
    running = True

    # Calculate the total grid width and height
    total_width = (logic.CARD_WIDTH + logic.MARGIN) * logic.GRID_SIZE - logic.MARGIN
    total_height = (logic.CARD_HEIGHT + logic.MARGIN) * logic.GRID_SIZE - logic.MARGIN

    # Calculate the offset to center the grid
    offset_x = (SCREEN_WIDTH - total_width) // 2
    offset_y = (SCREEN_HEIGHT - total_height) // 2

    # Adjust the position of each card in the grid
    for card in cards:
        card.x += offset_x
        card.y += offset_y

    while running:
        screen.fill((255, 255, 255))  # Fill screen with white

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for card in cards:
                    if card.is_clicked(mouse_x, mouse_y) and not card.is_flipped and not card.is_matched:
                        card.is_flipped = True
                        flipped_cards.append(card)

                # If two cards are flipped, check for a match
                if len(flipped_cards) == 2:
                    card1, card2 = flipped_cards
                    if logic.check_match(card1, card2):
                        card1.is_matched = True
                        card2.is_matched = True
                        flipped_cards = []
                    else:
                        for _ in range(10):  # Adjust the number of iterations for desired delay
                            screen.fill((255, 255, 255))
                            for card in cards:
                                card.draw(screen, font, colors)
                        pygame.display.flip()
                        pygame.time.delay(1000)
                            
                        card1.is_flipped = False
                        card2.is_flipped = False
                        flipped_cards = []  # Reset flipped cards

        # Draw all the cards on the screen
        for card in cards:
            card.draw(screen, font, colors)

        # Update the display
        pygame.display.flip()

# Run the game
if __name__ == '__main__':
    game_loop()
    pygame.quit()
