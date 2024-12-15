import pygame
import logic
import sys
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
font = pygame.font.Font("Array_Games/Memory_Match/Assets/Roboto-Italic.ttf", 36)
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_COLOR = (39, 50, 64)  # Green color for the buttons
BUTTON_HOVER_COLOR = (69, 80, 94)  # Darker green for button hover
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

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

    # Back button properties
    button_width, button_height = 120, 40
    button_x = 10  # Position the button near the top-left corner
    button_y = 10
    back_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    while running:
        screen.blit(bg_image, (0, 0))  # Draw background

        # Draw Back button with transparency
        transparent_surface = pygame.Surface((back_button_rect.width, back_button_rect.height), pygame.SRCALPHA)  # Create a surface with alpha
        transparent_surface.fill((39, 50, 64, 128))  # Fill with a semi-transparent color (RGBA format)
        screen.blit(transparent_surface, (back_button_rect.x, back_button_rect.y))  # Blit the transparent surface
        
        # Draw the text on top of the transparent button
        draw_text("Back", font, (255, 255, 255), back_button_rect.centerx, back_button_rect.centery)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the Back button was clicked
                if back_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Back button clicked!")
                    running = False  # Exit game loop to return to the main menu
                
                # Check card interactions
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

def restart_game():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Over")
    font = pygame.font.SysFont("Array_Games/Memory_Match/Assets/Roboto-Italic.ttf", 36)

    # Load background image
    background_image = pygame.image.load('Linked_List_games/Snake_Evolution/Assets/restart.png')
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Button positions
    restart_button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 2 - 60, BUTTON_WIDTH, BUTTON_HEIGHT)
    back_button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 2 + 20, BUTTON_WIDTH, BUTTON_HEIGHT)
    global score, sn
    # Game loop for restart page
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    # Restart the game logic (replace with actual restart function)
                    print("Restarting the game...")                  
                    game_loop()

                elif back_button_rect.collidepoint(event.pos):
                    # Exit the game
                    print("Exiting the game...")
                    pygame.quit()
                    sys.exit()

        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Highlight buttons on hover
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if restart_button_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, restart_button_rect)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, restart_button_rect)

        if back_button_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, back_button_rect)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)

        # Draw text on buttons
        draw_text("Start", font, (255, 255, 255), restart_button_rect.centerx, restart_button_rect.centery)
        draw_text("Back", font, (255, 255, 255), back_button_rect.centerx, back_button_rect.centery)

        pygame.display.flip()


# Run the game
if __name__ == '__main__':
    #game_loop()
    restart_game()
    pygame.quit()
