import sys
import pygame
from logic import generate_random_tree, get_tree_layout, get_traversals

# Pygame initialization
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Random Tree Traversal Visualization")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (255, 69, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Font
FONT = pygame.font.Font(None, 28)
TITLE_FONT = pygame.font.Font(None, 40)

# Global variable for selected nodes and incorrect nodes
selected_nodes = []
current_incorrect_nodes = []
current_click_time = 0

def draw_tree(tree_layout, tree_root, traversal_type):
    """Draw the tree structure on the screen."""
    for parent_value, (px, py) in tree_layout.items():
        parent_node = find_node_by_value(tree_root, parent_value)  # Find the parent node using its value
        if parent_node:
            for child in parent_node.children:
                cx, cy = tree_layout[child.value]  # Use child.value to get the position
                pygame.draw.line(screen, GRAY, (px, py + 20), (cx, cy - 20), 2)

    # Draw nodes
    for node_value, (x, y) in tree_layout.items():
        border_color = BLUE  # Default border color

        # Check if node is in selected_nodes and change the border color
        if node_value in selected_nodes:
            border_color = GREEN
        elif node_value in current_incorrect_nodes:
            border_color = RED

        pygame.draw.circle(screen, border_color, (x, y), 20)
        pygame.draw.circle(screen, WHITE, (x, y), 20, 2)  # Outline

        # Render the node's value
        node_text = FONT.render(str(node_value), True, WHITE)
        text_rect = node_text.get_rect(center=(x, y))
        screen.blit(node_text, text_rect)

    # Display the selected traversal
    traversals = get_traversals(tree_root)
    display_traversals(traversals, traversal_type)

def find_node_by_value(node, value):
    """Helper function to find a node by its value in the tree."""
    if node is None:
        return None
    if node.value == value:
        return node
    for child in node.children:
        found_node = find_node_by_value(child, value)
        if found_node:
            return found_node
    return None

def display_traversals(traversals, traversal_type):
    """Display the selected traversal result on the screen."""
    y_offset = 600
    x_spacing = 20
    # Show the traversal order with the correct selections so far
    traversal_text = f"{traversal_type}: {' '.join(map(str, selected_nodes))}"
    rendered_text = FONT.render(traversal_text, True, BLACK)
    screen.blit(rendered_text, (x_spacing, y_offset))

def handle_mouse_click(mouse_pos, tree_layout, traversal_order):
    """Handle mouse clicks on nodes and provide feedback."""
    global selected_nodes, current_incorrect_nodes, current_click_time

    for node_value, (x, y) in tree_layout.items():
        # Check if the mouse click is inside the node's circle (within 20 pixels radius)
        if (x - mouse_pos[0]) ** 2 + (y - mouse_pos[1]) ** 2 <= 20 ** 2:
            # Check if the node is the next correct one in the traversal
            if node_value == traversal_order[0]:  # Correct node
                selected_nodes.append(node_value)
                current_incorrect_nodes = []  # Clear incorrect nodes
                traversal_order.pop(0)  # Move to the next node in the order
                current_click_time = pygame.time.get_ticks()  # Record the click time
            else:  # Incorrect node
                # Highlight in red for 1 second and reset after 1 second
                current_incorrect_nodes = [node_value]
                pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # Reset color after 1 second

def main():
    """Main function to visualize the tree and its traversals."""
    global SCREEN_WIDTH, SCREEN_HEIGHT, selected_nodes, current_incorrect_nodes, current_click_time

    # Generate random tree and layout
    tree_root = generate_random_tree()
    tree_layout = get_tree_layout(tree_root, SCREEN_WIDTH, SCREEN_HEIGHT, min_gap=100)

    # Get the selected traversal type passed via command line argument
    if len(sys.argv) > 1:
        traversal_type = sys.argv[1]
    else:
        traversal_type = "Pre Order"  # Default to Pre Order if no argument

    # Get traversal order list (Pre Order, In Order, Post Order)
    traversals = get_traversals(tree_root)
    traversal_order = list(traversals[traversal_type])  # Make a copy of the list

    selected_nodes = []  # List to track correctly selected nodes
    current_incorrect_nodes = []  # To track incorrectly selected nodes
    current_click_time = 0  # For timing the reset of the red border

    # Main loop
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Draw tree and selected traversal
        draw_tree(tree_layout, tree_root, traversal_type)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse click event
                mouse_pos = pygame.mouse.get_pos()
                handle_mouse_click(mouse_pos, tree_layout, traversal_order)
            elif event.type == pygame.USEREVENT + 1:  # Reset red border after 1 second
                current_incorrect_nodes = []  # Clear incorrect nodes

        pygame.display.flip()

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
