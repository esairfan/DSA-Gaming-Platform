import pygame
from logic import generate_balanced_tree

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
NODE_RADIUS = 20
LINE_COLOR = (0, 0, 0)
NODE_COLOR = (0, 0, 255)  # Blue for extra nodes initially
SELECTED_NODE_COLOR = (255, 165, 0)  # Orange for selected extra node
ROOT_NODE_COLOR = (0, 255, 0)  # Green for root node
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (255, 255, 255)
EXTRA_NODES_COLOR = (255, 0, 0)
FPS = 60

# Variables to track the state of the game
selected_extra_node = None
root_node_selected = False

def draw_tree(screen, tree_structure):
    """
    Draw the balanced binary tree using Pygame.
    """
    # Draw edges
    for i in range(len(tree_structure) - 1):
        for parent_idx, parent_node in enumerate(tree_structure[i]):
            for child_idx in range(2):
                child_level = i + 1
                child_node = tree_structure[child_level][2 * parent_idx + child_idx]
                pygame.draw.line(screen, LINE_COLOR, parent_node['position'], child_node['position'], 2)

    # Draw nodes with numbers
    font = pygame.font.Font(None, 24)
    for level in tree_structure:
        for node in level:
            # Draw the node circle
            pygame.draw.circle(screen, NODE_COLOR, node['position'], NODE_RADIUS)
            # Draw the number
            number_text = font.render(str(node['number']), True, TEXT_COLOR)
            text_rect = number_text.get_rect(center=node['position'])
            screen.blit(number_text, text_rect)

def draw_extra_nodes(screen, extra_nodes):
    """
    Draw the extra nodes at the bottom of the screen.
    """
    global selected_extra_node

    font = pygame.font.Font(None, 24)
    y_position = SCREEN_HEIGHT - 50  # Position at the bottom of the screen
    x_spacing = SCREEN_WIDTH // (len(extra_nodes) + 1)

    for i, number in enumerate(extra_nodes):
        x_position = x_spacing * (i + 1)

        # Determine the color of the node (check if it's selected)
        if selected_extra_node == number:
            node_color = SELECTED_NODE_COLOR
        else:
            node_color = NODE_COLOR  # Default is blue

        pygame.draw.circle(screen, node_color, (x_position, y_position), NODE_RADIUS)

        number_text = font.render(str(number), True, TEXT_COLOR)
        text_rect = number_text.get_rect(center=(x_position, y_position))
        screen.blit(number_text, text_rect)

def draw_root_node(screen, tree_structure):
    """
    Draw the root node with a green color after selection.
    """
    if root_node_selected:
        root_position = tree_structure[0][0]['position']
        pygame.draw.circle(screen, ROOT_NODE_COLOR, root_position, NODE_RADIUS)
        font = pygame.font.Font(None, 24)
        number_text = font.render(str(tree_structure[0][0]['number']), True, TEXT_COLOR)
        text_rect = number_text.get_rect(center=root_position)
        screen.blit(number_text, text_rect)

def handle_node_click(mouse_pos, extra_nodes, tree_structure):
    """
    Handle the click on extra nodes and root node.
    """
    global selected_extra_node, root_node_selected

    # Check if an extra node is clicked
    x_spacing = SCREEN_WIDTH // (len(extra_nodes) + 1)
    y_position = SCREEN_HEIGHT - 50  # Position of the extra nodes
    for i, number in enumerate(extra_nodes):
        x_position = x_spacing * (i + 1)
        node_rect = pygame.Rect(x_position - NODE_RADIUS, y_position - NODE_RADIUS, NODE_RADIUS * 2, NODE_RADIUS * 2)

        if node_rect.collidepoint(mouse_pos):
            # If this node is clicked, toggle its selection
            if selected_extra_node == number:
                selected_extra_node = None  # Deselect
            else:
                selected_extra_node = number  # Select new node
                root_node_selected = True  # Mark root node as selected

    # Check if the root node is clicked
    root_position = tree_structure[0][0]['position']
    root_rect = pygame.Rect(root_position[0] - NODE_RADIUS, root_position[1] - NODE_RADIUS, NODE_RADIUS * 2, NODE_RADIUS * 2)

    if root_rect.collidepoint(mouse_pos):
        root_node_selected = True  # Mark root as selected

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Balanced Tree with Extra Nodes")
    clock = pygame.time.Clock()

    # Generate tree structure and extra nodes
    tree_structure, extra_nodes = generate_balanced_tree(SCREEN_WIDTH, SCREEN_HEIGHT)

    global selected_extra_node, root_node_selected

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse click
                handle_node_click(event.pos, extra_nodes, tree_structure)

        screen.fill(BACKGROUND_COLOR)
        draw_tree(screen, tree_structure)
        draw_extra_nodes(screen, extra_nodes)
        draw_root_node(screen, tree_structure)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
