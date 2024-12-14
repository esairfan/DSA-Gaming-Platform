import pygame
import logic

# Initialize Pygame
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Euler Path Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Initialize nodes and edges
nodes = logic.nodes
edges = logic.edges
clicked_nodes = []
used_edges = set()
win = False
lose = False

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

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Draw edges, nodes, and path
    draw_edges()
    draw_nodes()
    draw_path()

    # Check win/lose conditions
    win = logic.check_win(used_edges)
    lose = logic.check_lose(clicked_nodes, edges, used_edges)

    # Display win/lose message
    if win:
        font = pygame.font.Font(None, 36)
        text = font.render("You Win!", True, GREEN)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))
    elif lose:
        font = pygame.font.Font(None, 36)
        text = font.render("You Lose!", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not win and not lose:
            if event.button == 1:  # Left-click
                # Check if a node was clicked
                for i, node in enumerate(nodes):
                    x, y = node
                    if (event.pos[0] - x) ** 2 + (event.pos[1] - y) ** 2 < 10 ** 2:
                        clicked_nodes, used_edges = logic.handle_node_click(clicked_nodes, used_edges, edges, i)

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
