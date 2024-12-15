import pygame
import os
from logic import TowerOfHanoi

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Trek")
WHITE1 = (255, 253, 208)
WHITE = (255, 255, 255)
DISK_COLORS = [(205, 133, 63), (160, 82, 45), (139, 69, 19), (244, 164, 66), (112, 128, 144)]
pygame.mixer.init()

# Load sound effect for card flip
tower_click = pygame.mixer.Sound("Stack_Games/TowerOfHanoi/Assets/tower_click.mp3")
distination_click = pygame.mixer.Sound("Stack_Games/TowerOfHanoi/Assets/invalid.mp3")

rod_image = pygame.image.load("Stack_Games/TowerOfHanoi/Assets/rod.png")
rod_image = pygame.transform.scale(rod_image, (20, 300))
bg_image = pygame.image.load("Stack_Games/TowerOfHanoi/Assets/ui1 (2).jpg")
bg_image = pygame.transform.scale(bg_image, (1400, 700))

DISK_HEIGHT = 20
TOWER_X_POSITIONS = [400, 700, 1000]

# Load "You Win" image
you_win_image = pygame.image.load("Stack_Games/TowerOfHanoi/Assets/you_win.png")
you_win_image = pygame.transform.scale(you_win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Back button image
back_button_image = pygame.image.load("Stack_Games/TowerOfHanoi/Assets/BG.jpg")
back_button_image = pygame.transform.scale(back_button_image, (150, 50))

tiles = int(os.getenv("TILE_COUNT", 4))
game = TowerOfHanoi(tiles)
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_COLOR = (39, 50, 64)  # Green color for the buttons
BUTTON_HOVER_COLOR = (69, 80, 94)  # Darker green for button hover
class Button:
    def __init__(self, x, y, width, height, text, bg_color, text_color, 
                 border_radius=0, border_color=None, border_width=0, font_path=None, font_size=36):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_width = border_width
        # Load custom font or use default
        self.font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.Font(None, font_size)
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, screen):
        # Draw the border if needed
        if self.border_width > 0 and self.border_color:
            pygame.draw.rect(
                screen, 
                self.border_color, 
                self.rect, 
                border_radius=self.border_radius, 
                width=self.border_width
            )
        # Draw the button background
        pygame.draw.rect(
            screen, 
            self.bg_color, 
            self.rect, 
            border_radius=self.border_radius
        )
        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.is_hovered(pos)
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_rods():
    rod_y = SCREEN_HEIGHT - 285
    # Draw the rods
    for x in TOWER_X_POSITIONS:
        screen.blit(rod_image, (x - rod_image.get_width() // 2, rod_y))

    # Draw a connecting line (same color as rod)
    line_color = (100, 50, 10)  # Use the same color as the rods
    pygame.draw.line(screen, line_color, 
                     (TOWER_X_POSITIONS[0], rod_y + 264.7),  # Starting point of the line
                     (TOWER_X_POSITIONS[-1], rod_y + 264.7),  # Ending point of the line
                     width=14)  # Thickness of the line

def draw_disks():
    for tower_idx, tower in enumerate(game.towers):
        x = TOWER_X_POSITIONS[tower_idx]
        for disk_idx, disk in enumerate(tower):
            width = 25 + disk * 20
            y = SCREEN_HEIGHT - 50 - (DISK_HEIGHT + 5) * disk_idx
            # If it's the top disk of the selected rod, highlight it with a green border
            border_color = (0, 255, 0) if tower_idx == selected_tower and disk_idx == len(tower) - 1 else (255, 255, 255)
            pygame.draw.rect(screen, DISK_COLORS[disk % len(DISK_COLORS)],
                            (x - width // 2, y, width, DISK_HEIGHT), border_radius=10)
            # Draw the green border if it's the selected disk
            if border_color != (255, 255, 255):
                pygame.draw.rect(screen, border_color, 
                                 (x - width // 2, y, width, DISK_HEIGHT), width=3, border_radius=10)

def animate_move(source, target, disk, screen, back_button):
    """
    Animates the movement of a disk from the source rod to the target rod.
    """
    source_x = TOWER_X_POSITIONS[source]
    target_x = TOWER_X_POSITIONS[target]
    source_y = SCREEN_HEIGHT - 50 - (DISK_HEIGHT + 5) * (len(game.towers[source]) - 1)

    # Remove the disk from the source tower during animation
    game.towers[source].remove(disk)

    # Move up
    y = source_y
    while y > 200:  # Arbitrary height for the upward movement
        y -= 5
        redraw_screen(source_x, y, disk, source, back_button)


    # Move horizontally
    x = source_x
    step = 5 if target_x > source_x else -5
    while (step > 0 and x < target_x) or (step < 0 and x > target_x):
        x += step
        redraw_screen(x, 200, disk, source, back_button)


    # Move down
    target_y = SCREEN_HEIGHT - 50 - (DISK_HEIGHT + 5) * len(game.towers[target])
    while y < target_y:
        y += 5
        redraw_screen(target_x, y, disk, source, back_button)


    # After animation, place the disk in the target tower
    game.towers[target].append(disk)

def redraw_screen(x, y, disk, source, back_button):
    """
    Redraws the screen during animation with the moving disk at (x, y).
    """
    screen.blit(bg_image, (0, 0))
    draw_rods()
    draw_disks()
    back_button.draw(screen)
    # Draw the moving disk
    width = 25 + disk * 20
    pygame.draw.rect(
        screen,
        DISK_COLORS[disk % len(DISK_COLORS)],
        (x - width // 2, y, width, DISK_HEIGHT),
        border_radius=10
    )

    # Draw the remaining disks in the source tower (invisible disk during animation)
    if source is not None:
        for disk_idx, disk_in_source in enumerate(game.towers[source]):
            width = 25 + disk_in_source * 20
            y_pos = SCREEN_HEIGHT - 50 - (DISK_HEIGHT + 5) * disk_idx
            pygame.draw.rect(screen, DISK_COLORS[disk_in_source % len(DISK_COLORS) ],
                             (TOWER_X_POSITIONS[source] - width // 2, y_pos, width, DISK_HEIGHT), border_radius=10)

    pygame.display.flip()
    pygame.time.delay(10)  # Adjust for animation speed

def show_game_complete_screen():
    """Display the win screen and Back button."""
    screen.blit(you_win_image, (0, 0))
    
    # Draw Back Button with dark brown background and white text
    back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 1.3 - 25, 150, 50)  # Position and size of the button
    pygame.draw.rect(screen, (101, 67, 33), back_button_rect)  # Dark brown background color
    
    # Add text to the button
    font = pygame.font.SysFont('Arial', 25)
    text = font.render('Back', True, (255, 255, 255))  # White text color
    screen.blit(text, (back_button_rect.x + (back_button_rect.width - text.get_width()) // 2, 
                       back_button_rect.y + (back_button_rect.height - text.get_height()) // 2))

    pygame.display.flip()

def handle_back_button_click(mouse_x, mouse_y):
    """Handle click on the Back button."""
    back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 1.3 - 25, 150, 50)  # Position and size of the button
    if back_button_rect.collidepoint(mouse_x, mouse_y):
        return True
    return False


def show_main_screen():
    """Display the main screen with a 'Return' button."""
    screen.blit(bg_image, (0, 0))  # Background
    draw_rods()  # Draw rods and disks
    
    # Draw Return Button (similar to the Back button)
    return_button_rect = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 75, 150, 50)
    pygame.draw.rect(screen, (101, 67, 33), return_button_rect)  # Dark brown color
    
    # Draw text on the Return button
    font = pygame.font.SysFont('Arial', 25)
    text = font.render('Return', True, (255, 255, 255))  # White text color
    screen.blit(text, (return_button_rect.x + (return_button_rect.width - text.get_width()) // 2, 
                       return_button_rect.y + (return_button_rect.height - text.get_height()) // 2))

    pygame.display.flip()

def handle_return_button_click(mouse_x, mouse_y):
    """Handle click on the Return button to exit the game."""
    return_button_rect = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 75, 150, 50)  # Position and size of the button
    if return_button_rect.collidepoint(mouse_x, mouse_y):
        return True
    return False

def main():
    BUTTONTEXTCOLOR = (255, 255, 255)
    back_button = Button(1200, 600, 100, 60, 'Back', (0, 0, 0, 0), BUTTONTEXTCOLOR, 6)
    running = True
    global selected_tower  # Mark selected_tower as global to be used in the draw_disks function
    selected_tower = None  # Keeps track of the currently selected rod (source)

    while running:
        screen.blit(bg_image, (0, 0))
        draw_rods()
        draw_disks()
        back_button.draw(screen)
        pygame.display.flip()

        # Check if the game is complete
        if game.is_game_complete():
            show_game_complete_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        if back_button.is_clicked(mouse_pos):
                            print("Back button clicked")
                            running=False
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     mouse_x, mouse_y = pygame.mouse.get_pos()
                #     if handle_back_button_click(mouse_x, mouse_y):
                #         print("Back button clicked")
                #         restart_game()
                #         running = False
        else:
            # Add the "Return" button to the main screen
            # show_main_screen()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check for clicks on the Return button
                    if handle_return_button_click(mouse_x, mouse_y):
                        print("Return button clicked - Exiting game")
                        running = False  # Exit the game
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            mouse_pos = pygame.mouse.get_pos()
                            if back_button.is_clicked(mouse_pos):
                                print("Back button clicked")
                                running=False
                    # Determine which tower was clicked
                    clicked_tower = None
                    for idx, x in enumerate(TOWER_X_POSITIONS):
                        if abs(mouse_x - x) < 50:  # Check if the click is near the tower
                            clicked_tower = idx
                            break

                    if clicked_tower is not None:
                        if selected_tower is None:
                            # First click: Set the source tower
                            tower_click.play()  # Play the sound effect
                            selected_tower = clicked_tower
                        else:
                            # Second click: Set the target tower and make a move
                            if game.is_valid_move(selected_tower, clicked_tower):
                                # Animate the disk movement
                                disk = game.towers[selected_tower][-1]
                                animate_move(selected_tower, clicked_tower, disk, screen, back_button)
                                # Perform the actual move
                                game.make_move(selected_tower, clicked_tower)
                                print(f"Moved disk from Tower {selected_tower + 1} to Tower {clicked_tower + 1}")
                                tower_click.play()  # Play the sound effect
                            else:
                                print("Invalid move!")
                                distination_click.play()  # Play the sound effect
                            selected_tower = None  # Reset the selection
            

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
                    main()

                elif back_button_rect.collidepoint(event.pos):
                    # Exit the game
                    print("Exiting the game...")
                    running=False

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

if __name__ == "__main__":
    restart_game()
