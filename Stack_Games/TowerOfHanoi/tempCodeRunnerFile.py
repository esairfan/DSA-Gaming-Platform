import pygame
from logic import TowerOfHanoi
 
pygame.init()
 
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower of Hanoi")
 
WHITE = (255, 255, 255)
DISK_COLORS = [(205, 133, 63), (160, 82, 45), (139, 69, 19), (244, 164, 66), (112, 128, 144)]
 
rod_image = pygame.image.load("Stack_Games/TowerOfHanoi/Assets/rod.png")
rod_image = pygame.transform.scale(rod_image, (20, 300))
 
DISK_HEIGHT = 20
TOWER_X_POSITIONS = [150, 400, 650]

tiles = 5
game = TowerOfHanoi(tiles)
 
def draw_rods():
    for x in TOWER_X_POSITIONS:
        rod_y = SCREEN_HEIGHT - 285
        screen.blit(rod_image, (x - rod_image.get_width() // 2, rod_y))
 
def draw_disks():
    for tower_idx, tower in enumerate(game.towers):
        x = TOWER_X_POSITIONS[tower_idx]
        for disk_idx, disk in enumerate(tower):
            width = 25 + disk * 20
            y = SCREEN_HEIGHT - 50 - (DISK_HEIGHT + 5) * disk_idx
             
            pygame.draw.rect(screen, DISK_COLORS[disk % len(DISK_COLORS)],
                            (x - width // 2, y, width, DISK_HEIGHT), border_radius=10) 
def animate_move(source, target, disk):
    """
    Animates the movement of a disk from the source rod to the target rod.
    """
    source_x = TOWER_X_POSITIONS[source]
    target_x = TOWER_X_POSITIONS[target]
    source_y = SCREEN_HEIGHT - 50 - (DISK_HEIGHT + 5) * (len(game.towers[source]) - 1)

    # Move up
    y = source_y
    while y > 200:  # Arbitrary height for the upward movement
        y -= 5
        redraw_screen(source_x, y, disk)
    
    # Move horizontally
    x = source_x
    step = 5 if target_x > source_x else -5
    while (step > 0 and x < target_x) or (step < 0 and x > target_x):
        x += step
        redraw_screen(x, 200, disk)

    # Move down
    target_y = SCREEN_HEIGHT - 50 - (DISK_HEIGHT + 5) * len(game.towers[target])
    while y < target_y:
        y += 5
        redraw_screen(target_x, y, disk)


def redraw_screen(x, y, disk):
    """
    Redraws the screen during animation with the moving disk at (x, y).
    """
    screen.fill(WHITE)
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
    pygame.display.flip()
    pygame.time.delay(10)  # Adjust for animation speed


def main():
    running = True
    selected_tower = None  # Keeps track of the currently selected rod (source)

    while running:
        screen.fill(WHITE)
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
                        else:
                            print("Invalid move!")
                        selected_tower = None  # Reset the selection

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
