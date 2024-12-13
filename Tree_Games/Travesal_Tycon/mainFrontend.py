import sys
import pygame
from logic import generate_random_tree, get_tree_layout, get_traversals

# Pygame initialization
pygame.init()
# Set up the timer once for 300ms delay
pygame.time.set_timer(pygame.USEREVENT + 1, 300)

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Random Tree Traversal Visualization")


pygame.mixer.init()

# Load sound effect for card flip
button_click = pygame.mixer.Sound("Tree_Games/Travesal_Tycon/Assets/right_click.mp3")
incorrect_click = pygame.mixer.Sound("Tree_Games/Travesal_Tycon/Assets/incorrect_click.mp3")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (255, 69, 0)
GREEN = (0, 255, 0)
BG = (250, 236, 204)

# Font
FONT = pygame.font.Font("Tree_Games/Travesal_Tycon/Assets/static1/static/SourceSans3-Regular.ttf", 20)
TITLE_FONT = pygame.font.Font("Tree_Games/Travesal_Tycon/Assets/static1/static/SourceSans3-Bold.ttf", 30)

# Global variable for selected nodes and incorrect nodes
selected_nodes = []
current_incorrect_nodes = []
sound_played = False  # Tracks if the incorrect sound was already played

def draw_tree(tree_layout, tree_root, traversal_type):
    """Draw the tree structure on the screen."""
    global sound_played
    for parent_value, (px, py) in tree_layout.items():
        parent_node = find_node_by_value(tree_root, parent_value)
        if parent_node:
            for child in parent_node.children:
                cx, cy = tree_layout[child.value]
                pygame.draw.line(screen, BLACK, (px, py + 20), (cx, cy - 20), 1)

    # Draw nodes
    for node_value, (x, y) in tree_layout.items():
        border_color = BLUE
        if node_value in selected_nodes:
            border_color = GREEN
        elif node_value in current_incorrect_nodes:
            if not sound_played:  # Play sound only once
                incorrect_click.play()
                sound_played = True
            border_color = RED

        pygame.draw.circle(screen, border_color, (x, y), 20)
        pygame.draw.circle(screen, WHITE, (x, y), 20, 2)

        # Render the node's value
        node_text = FONT.render(str(node_value), True, BG)
        text_rect = node_text.get_rect(center=(x, y))
        screen.blit(node_text, text_rect)

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

def handle_mouse_click(mouse_pos, tree_layout, traversal_order):
    """Handle mouse clicks on nodes and provide feedback."""
    global selected_nodes, current_incorrect_nodes, sound_played

    for node_value, (x, y) in tree_layout.items():
        if (x - mouse_pos[0]) ** 2 + (y - mouse_pos[1]) ** 2 <= 20 ** 2:
            if node_value == traversal_order[0]:  # Correct node
                selected_nodes.append(node_value)
                current_incorrect_nodes = []  # Clear incorrect nodes
                sound_played = False  # Reset sound flag on correct click
                traversal_order.pop(0)
            else:  # Incorrect node
                current_incorrect_nodes = [node_value]
                sound_played = False  # Reset so the sound plays once per incorrect click
                pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

def main():
    """Main function to visualize the tree and its traversals."""
    global selected_nodes, current_incorrect_nodes, sound_played

    tree_root = generate_random_tree()
    tree_layout = get_tree_layout(tree_root, SCREEN_WIDTH, SCREEN_HEIGHT, min_gap=100)

    if len(sys.argv) > 1:
        traversal_type = sys.argv[1]
    else:
        traversal_type = "Pre Order"

    traversals = get_traversals(tree_root)
    traversal_order = list(traversals[traversal_type])

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BG)
        draw_tree(tree_layout, tree_root, traversal_type)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                handle_mouse_click(mouse_pos, tree_layout, traversal_order)
                button_click.play()
            elif event.type == pygame.USEREVENT + 1:  # Reset red border after 1 second
                current_incorrect_nodes = []
                sound_played = False  # Reset sound flag

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
