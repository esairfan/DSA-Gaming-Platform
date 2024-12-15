import pygame
import sys
import math
from logic import edges, get_edge_weight

# Initialize Pygame
pygame.init()

# Set up the window size
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Kruskal\'s Algorithm Visualization')
pygame.mixer.init()

# Load the background music
button = pygame.mixer.Sound("Graph_Games/one_way_out/Assets/button_click.mp3")

# Define colors
BLACK = (0, 0, 0)
WHITE = (250, 236, 204)
RED = (139, 0, 0)
GREEN = (0, 139, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (39, 50, 64)
BUTTON_HOVER_COLOR = (69, 80, 94)

# Node radius and click tolerance
node_radius = 20
click_tolerance = 30

# Manually set node positions (based on your image)
nodes = [
    (270, 550),  # Node 0
    (600, 50),   # Node 1
    (1000, 150), # Node 2
    (150, 300),  # Node 3
    (400, 600),  # Node 4   
    (350, 150),  # Node 5
    (880, 500),  # Node 6 
]

# Function to calculate the surface point on the node
def get_surface_point(x, y, node_x, node_y):
    angle = math.atan2(y - node_y, x - node_x)
    surface_x = node_x + node_radius * math.cos(angle)
    surface_y = node_y + node_radius * math.sin(angle)
    return surface_x, surface_y

# Draw the graph function
def draw_graph():
    screen.fill(WHITE)

    # Draw nodes
    for i, (x, y) in enumerate(nodes):
        color = GREEN if node_clicked[i] else BLUE
        pygame.draw.circle(screen, color, (int(x), int(y)), node_radius)

    # Draw edges
    for (u, v) in edges:
        x1, y1 = nodes[u]
        x2, y2 = nodes[v]
        x1_surface, y1_surface = get_surface_point(x1 - 50, y1, x1, y1)
        x2_surface, y2_surface = get_surface_point(x2 - 50, y2, x2, y2)
        pygame.draw.line(screen, BLACK, (int(x1_surface), int(y1_surface)), (int(x2_surface), int(y2_surface)), 2)

        weight = round(get_edge_weight(u, v), 2)
        mid_x, mid_y = (x1_surface + x2_surface) / 2, (y1_surface + y2_surface) / 2
        font = pygame.font.Font(None, 36)
        weight_text = font.render(str(weight), True, BLACK)
        screen.blit(weight_text, (mid_x + 10, mid_y + 10))

    # Draw the return button
    draw_return_button()

    pygame.display.update()

# Detect if a node is clicked
def check_node_click(x, y):
    for i, (node_x, node_y) in enumerate(nodes):
        if (x - node_x)**2 + (y - node_y)**2 <= click_tolerance**2:
            return i
    return -1

# Store the clicked node states
node_clicked = [False] * len(nodes)
last_clicked_node = -1

# Draw the return button
def draw_return_button():
    global return_button_rect
    button_width, button_height = 200, 50
    button_x, button_y = width - 220, height - 80
    return_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if return_button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, return_button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, return_button_rect)

    font = pygame.font.Font(None, 36)
    text_surface = font.render("Return", True, WHITE)
    text_rect = text_surface.get_rect(center=return_button_rect.center)
    screen.blit(text_surface, text_rect)

# Main game loop
def main():
    global last_clicked_node
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if return_button_rect.collidepoint(mouse_x, mouse_y):
                    button.play()
                    print("Exiting the game...")
                    running = False  # Exit the game
                
                clicked_node = check_node_click(mouse_x, mouse_y)
                if clicked_node != -1:
                    node_clicked[clicked_node] = True
                    last_clicked_node = clicked_node
                    print(f"Node {clicked_node} clicked")

        draw_graph()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
