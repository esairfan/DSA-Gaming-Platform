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

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Node radius and click tolerance
node_radius = 20
click_tolerance = 30

# Manually set node positions (based on your image)
nodes = [
    (300, 250),  # Node 0
    (600, 50),  # Node 1
    (1000, 150),  # Node 2
    (150, 300),  # Node 3
    (400, 600),  # Node 4   
    (350, 150),  # Node 5
    (880, 500),  # Node 6 
]

# Function to calculate the surface point on the node
def get_surface_point(x, y, node_x, node_y):
    # Calculate the angle from the node center to the point (x, y)
    angle = math.atan2(y - node_y, x - node_x)
    # Calculate the point on the circumference of the node
    surface_x = node_x + node_radius * math.cos(angle)
    surface_y = node_y + node_radius * math.sin(angle)
    return surface_x, surface_y

# Draw the graph function
def draw_graph():
    # Clear screen
    screen.fill(WHITE)

    # Draw nodes
    for i, (x, y) in enumerate(nodes):
        # If the node is clicked, change the color to green
        color = GREEN if node_clicked[i] else BLUE
        pygame.draw.circle(screen, color, (int(x), int(y)), node_radius)

    # Draw edges
    for (u, v) in edges:
        x1, y1 = nodes[u]
        x2, y2 = nodes[v]

        # Get the surface points for the edges
        x1_surface, y1_surface = get_surface_point(x1-50, y1, x1, y1)
        x2_surface, y2_surface = get_surface_point(x2-50, y2, x2, y2)
        
        # Draw the edge from the surface of the nodes
        pygame.draw.line(screen, BLACK, (int(x1_surface), int(y1_surface)), (int(x2_surface), int(y2_surface)), 2)

        # Calculate the weight and place it offset from the middle of the edge
        weight = round(get_edge_weight(u, v), 2)
        mid_x, mid_y = (x1_surface + x2_surface) / 2, (y1_surface + y2_surface) / 2
        
        # Offsetting the text slightly to the right and down from the midpoint
        font = pygame.font.Font(None, 36)
        weight_text = font.render(str(weight), True, BLACK)
        screen.blit(weight_text, (mid_x + 10, mid_y + 10))  # Slight offset for the weight

    pygame.display.update()

# Detect if a node is clicked
def check_node_click(x, y):
    for i, (node_x, node_y) in enumerate(nodes):
        if (x - node_x)**2 + (y - node_y)**2 <= click_tolerance**2:
            return i
    return -1

# Store the clicked node states
node_clicked = [False] * len(nodes)

# Main game loop
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_node = check_node_click(mouse_x, mouse_y)
                if clicked_node != -1:
                    node_clicked[clicked_node] = True
                    print(f"Node {clicked_node} clicked")

        # Draw the graph with updated node states
        draw_graph()

        # If space is pressed, run Kruskal's algorithm
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            print("Running Kruskal's Algorithm...")
            # Here you can run the Kruskal algorithm if needed.
            # You can call `kruskal()` function from logic.py and visualize the result.

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
