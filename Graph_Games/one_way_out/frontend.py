import pygame
import logic

# Initialize Pygame
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
# Set screen dimensions
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Euler Path Game")
pygame.mixer.init()

# Load the background music
button = pygame.mixer.Sound("Graph_Games/one_way_out/Assets/button_click.mp3")
win1 = pygame.mixer.Sound("Graph_Games/one_way_out/Assets/win.mp3")
loss1 = pygame.mixer.Sound("Graph_Games/one_way_out/Assets/you_loss.mp3")

# Define colors
WHITE = (250, 236, 204)
BLACK = (0, 0, 0)
RED = (139, 0, 0)
GREEN = (0, 139, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Initialize nodes and edges
nodes = logic.nodes
edges = logic.edges
clicked_nodes = []
used_edges = set()
game_over = False  # Track game status (win/loss)

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_COLOR1 = (51, 25, 0)
BUTTON_COLOR = (39, 50, 64)  # Green color for the buttons
BUTTON_HOVER_COLOR = (69, 80, 94)  # Darker green for button hover
BUTTON_HOVER_COLOR1 = (102, 51, 25)
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Function to draw the edges
def draw_edges():
    for edge in edges:
        u, v = edge
        color = PURPLE if edge in used_edges else BLACK  # Color the used edges purple
        pygame.draw.line(screen, color, nodes[u], nodes[v], 2)


# Function to draw the nodes
def draw_nodes():
    for i, node in enumerate(nodes):
        color = RED if i not in clicked_nodes else GREEN  # Highlight selected nodes
        pygame.draw.circle(screen, color, (int(node[0]), int(node[1])), 10)

# Function to draw the path so far
def draw_path():
    if len(clicked_nodes) > 1:
        for i in range(len(clicked_nodes) - 1):
            u, v = clicked_nodes[i], clicked_nodes[i + 1]
            pygame.draw.line(screen, BLUE, nodes[u], nodes[v], 3)
def draw_return_button():
    global return_button_rect

    # Button position for "Return"
    return_button_rect = pygame.Rect(50, 600, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Highlight button on hover
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if return_button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR1, return_button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR1, return_button_rect)

    # Draw text on the "Return" button
    font = pygame.font.SysFont("Array_Games/Memory_Match/Assets/Roboto-Italic.ttf", 36)
    draw_text("Return", font, (255, 255, 255), return_button_rect.centerx, return_button_rect.centery)

def main():
    global used_edges, clicked_nodes, game_over
    # Main loop
    nodes = None
    edges = None
    clicked_nodes = None
    used_edges = set()
    nodes = logic.nodes
    edges = logic.edges
    clicked_nodes = []
    used_edges = set()
    game_over = False
    running = True
    while running:
        screen.fill(WHITE)

        # Draw edges, nodes, path, and buttons
        draw_edges()
        draw_nodes()
        draw_path()
        draw_return_button()

        # Check win/lose conditions
        win = logic.check_win(used_edges)
        lose = logic.check_lose(clicked_nodes, edges, used_edges)

        # Display win/lose message
        if win:
            font = pygame.font.Font("Graph_Games/one_way_out/Assets/SourGummy-Italic-VariableFont_wdth,wght.ttf", 36)
            text = font.render("You Win!", True, GREEN)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))
            win1.play()
            game_over = True
        elif lose:
            font = pygame.font.Font("Graph_Games/one_way_out/Assets/SourGummy-Italic-VariableFont_wdth,wght.ttf", 36)
            text = font.render("You Lose!", True, RED)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))
            loss1.play()
            game_over = True

        # If the game is over, display the "Back" button
        if game_over:
            draw_back_button()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left-click
                    # Check if "Return" button is clicked
                    if return_button_rect.collidepoint(event.pos):
                        print("Exiting game...")
                        running = False  # Exit the game when "Return" button is clicked

                    # Check if a node was clicked (when game is not won/lost)
                    if not win and not lose:
                        for i, node in enumerate(nodes):
                            x, y = node
                            if (event.pos[0] - x) ** 2 + (event.pos[1] - y) ** 2 < 10 ** 2:
                                clicked_nodes, used_edges = logic.handle_node_click(clicked_nodes, used_edges, edges, i)

                # Handle clicks on the "Back" button if game is over
                if game_over and back_button_rect.collidepoint(event.pos):
                    running = False  # Exit the game when "Back" button is clicked

        # Update the screen
        pygame.display.flip()

def draw_back_button():
    global back_button_rect

    # Button position for "Back"
    back_button_rect = pygame.Rect(900, 600, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Highlight button on hover
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if back_button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR1, back_button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR1, back_button_rect)

    # Draw text on the "Back" button
    font = pygame.font.SysFont("Array_Games/Memory_Match/Assets/Roboto-Italic.ttf", 36)
    draw_text("Back", font, (255, 255, 255), back_button_rect.centerx, back_button_rect.centery)

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

    # Quit Pygame
pygame.quit()
