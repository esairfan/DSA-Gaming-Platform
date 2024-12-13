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
TOWER_X_POSITIONS = [ 400, 700, 1000]

tiles = int(os.getenv("TILE_COUNT", 4))
game = TowerOfHanoi(tiles)

def draw_rods():
    rod_y = SCREEN_HEIGHT - 285
    # Draw the rods
    for x in TOWER_X_POSITIONS:
        screen.blit(rod_image, (x - rod_image.get_width() // 2, rod_y))

    # Draw a connecting line (same color as rod)
    line_color = (100, 50, 10) # Use the same color as the rods
    pygame.draw.line(screen, line_color, 
                     (TOWER_X_POSITIONS[0], rod_y+264.7),  # Starting point of the line
                     (TOWER_X_POSITIONS[-1], rod_y+264.7),  # Ending point of the line
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

def animate_move(source, target, disk):
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
        redraw_screen(source_x, y, disk, source)

    # Move horizontally
    x = source_x
    step = 5 if target_x > source_x else -5
    while (step > 0 and x < target_x) or (step < 0 and x > target_x):
        x += step
        redraw_screen(x, 200, disk, source)

    # Move down
    target_y = SCREEN_HEIGHT - 50 - (DISK_HEIGHT + 5) * len(game.towers[target])
    while y < target_y:
        y += 5
        redraw_screen(target_x, y, disk, source)

    # After animation, place the disk in the target tower
    game.towers[target].append(disk)

def redraw_screen(x, y, disk, source):
    """
    Redraws the screen during animation with the moving disk at (x, y).
    """
    screen.blit(bg_image, (0, 0))
    draw_rods()
    draw_disks()

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
            pygame.draw.rect(screen, DISK_COLORS[disk_in_source % len(DISK_COLORS)],
                             (TOWER_X_POSITIONS[source] - width // 2, y_pos, width, DISK_HEIGHT), border_radius=10)

    pygame.display.flip()
    pygame.time.delay(10)  # Adjust for animation speed


def main():
    running = True
    global selected_tower  # Mark selected_tower as global to be used in the draw_disks function
    selected_tower = None  # Keeps track of the currently selected rod (source)

    while running:
        screen.blit(bg_image, (0, 0))
        draw_rods()
        draw_disks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

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
                            animate_move(selected_tower, clicked_tower, disk)
                            # Perform the actual move
                            game.make_move(selected_tower, clicked_tower)
                            print(f"Moved disk from Tower {selected_tower + 1} to Tower {clicked_tower + 1}")
                            tower_click.play()  # Play the sound effect
                        else:
                            print("Invalid move!")
                            distination_click.play()  # Play the sound effect
                        selected_tower = None  # Reset the selection

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
