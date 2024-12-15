import pygame
import logic

# Initialize the game window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flip & Match')

# Initialize Pygame mixer for sound
pygame.mixer.init()

# Load sound effect for card flip
card_flip_sound = pygame.mixer.Sound("Array_Games/Memory_Match/Assets/CardFlip.mp3")
good_match = pygame.mixer.Sound("Array_Games/Memory_Match/Assets/goodmatch.mp3")
# Define colors for UI
colors = {
    'back': (0, 128, 255),    # Blue for the back of the card
    'flipped': (0, 255, 0),   # Green for flipped cards
    'text': (255, 255, 255),   # White text for symbols
}

bg_image = pygame.image.load("Array_Games/Memory_Match/Assets/The Journey Creative Writing Task.png")  # Make sure the image is in the same directory or provide the correct path
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the image to fit the screen

# Initialize the font
pygame.font.init()
font = pygame.font.Font(None, 36)

# Function to display the game
def game_loop():
    cards = logic.create_grid()  # Get the shuffled cards
    flipped_cards = []  # List to track flipped cards
    running = True

    # Calculate the total grid width and height
    total_width = (logic.CARD_WIDTH + logic.MARGIN_X) * logic.GRID_SIZE - logic.MARGIN_X
    total_height = (logic.CARD_HEIGHT + logic.MARGIN_Y) * logic.GRID_SIZE - logic.MARGIN_Y

    # Calculate the offset to center the grid
    offset_x = (SCREEN_WIDTH - total_width) // 2
    offset_y = (SCREEN_HEIGHT - total_height) // 2

    # Adjust the position of each card in the grid
    for card in cards:
        card.x += offset_x
        card.y += offset_y

    while running:
        screen.blit(bg_image, (0, 0))
        #screen.fill((0, 128, 128))
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
                        card_flip_sound.play()  # Play the card flip sound
                        flipped_cards.append(card)

                # If two cards are flipped, check for a match
                if len(flipped_cards) == 2:
                    card1, card2 = flipped_cards
                    if logic.check_match(card1, card2):
                        card1.is_matched = True
                        card2.is_matched = True
                        good_match.play()  # Play the good match sound
                        flipped_cards = []
                    else:
                        for _ in range(10):  # Adjust the number of iterations for desired delay
                            #screen.fill((0, 128, 128))
                            screen.blit(bg_image, (0, 0))
                            for card in cards:
                                card.draw(screen, font, colors)
                        pygame.display.flip()
                        pygame.time.delay(1000)
                            
                        card1.is_flipped = False
                        card2.is_flipped = False
                        card_flip_sound.play()  # Play the card flip sound
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
