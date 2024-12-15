import pygame
import sys
import random
from logic import BinarySearchTree, Node  # Import BST logic

# Initialize Pygame
pygame.init()
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
# Set the screen dimensions
WIDTH, HEIGHT = 1400, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Binary Search Tree")

pygame.mixer.init()

# Load sound effect for card flip
button_click = pygame.mixer.Sound("Tree_Games/Balanced_Tree/Assets/button_click.mp3")
you_win = pygame.mixer.Sound("Tree_Games/Balanced_Tree/Assets/you_won.mp3")
you_loss = pygame.mixer.Sound("Tree_Games/Balanced_Tree/Assets/you_loss.mp3")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (102, 153, 255)  # Default node color
GREEN = (0, 153, 0)  # Green color for selected nodes
RED = (139, 0, 0)
ORANGE = (255, 165, 0)  # Orange color for selected extra node
WHITE1 = (250, 240, 230)  
BLACK1 = (0, 0, 0)
SE = (217, 71, 57) 
BG = (250, 236, 204)
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_COLOR = (39, 50, 64)  # Green color for the buttons
BUTTON_HOVER_COLOR = (69, 80, 94)  # Darker green for button hover
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
# Function to calculate the positions of nodes for tree visualization
def calculate_positions(root, x, y, spacing, positions):
    if root is None:
        return
    positions[root.key] = (x, y)
    
    # Calculate the positions for left and right children
    if root.left:
        calculate_positions(root.left, x - spacing, y + 80, spacing // 1.75, positions)
    if root.right:
        calculate_positions(root.right, x + spacing, y + 80, spacing // 1.75, positions)

# Function to draw the tree on the Pygame screen
def draw_tree(root, positions, current_node, color):
    if root is None:
        return
    
    x, y = positions[root.key]
    node_color = GREEN if root == current_node else color
    pygame.draw.circle(screen, node_color, (x, y), 20)
    font = pygame.font.Font(None, 26)
    text = font.render(str(root.key), True, WHITE)
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
    
    # Draw edges to children
    if root.left:
        left_x, left_y = positions[root.left.key]
        pygame.draw.line(screen, BLACK, (x - 15, y + 10), (left_x, left_y), 2)
        draw_tree(root.left, positions, current_node, color)
    if root.right:
        right_x, right_y = positions[root.right.key]
        pygame.draw.line(screen, BLACK, (x + 15, y + 10), (right_x, right_y), 2)
        draw_tree(root.right, positions, current_node, color)

# Function to handle 'R' key event (move to right or add node to the right)
def handle_r_key(tree, root, current_node, selected_extra_node, extra_nodes):
    if not current_node:
        return root, current_node, selected_extra_node, extra_nodes
    if current_node.right:
        current_node = current_node.right
    elif selected_extra_node is not None:
        current_node.right = Node(selected_extra_node)
        extra_nodes.remove(selected_extra_node)
        selected_extra_node = None
    return root, current_node, selected_extra_node, extra_nodes

# Function to handle 'L' key event (move to left or add node to the left)
def handle_l_key(tree, root, current_node, selected_extra_node, extra_nodes):
    if not current_node:
        return root, current_node, selected_extra_node, extra_nodes
    if current_node.left:
        current_node = current_node.left
    elif selected_extra_node is not None:
        current_node.left = Node(selected_extra_node)
        extra_nodes.remove(selected_extra_node)
        selected_extra_node = None
    return root, current_node, selected_extra_node, extra_nodes

# Function to handle 'Up Arrow' key event (move to parent)
def handle_up_key(root, current_node):
    parent_node = find_parent(root, current_node)
    if parent_node:
        current_node = parent_node
    return current_node

# Recursive function to find the parent of a given node
def find_parent(root, target):
    if root is None:
        return None
    if root.left == target or root.right == target:
        return root
    return find_parent(root.left, target) or find_parent(root.right, target)

# Function to handle mouse click event
def handle_mouse_click(extra_nodes, selected_extra_node, event):
    mouse_x, mouse_y = event.pos
    node_spacing = WIDTH // 7
    y_position = HEIGHT - 100

    for i, node in enumerate(extra_nodes):
        x_position = (i + 1) * node_spacing
        if abs(mouse_x - x_position) < 20 and abs(mouse_y - y_position) < 20:
            return None if selected_extra_node == node else node
    return selected_extra_node

# Function to draw extra nodes at the bottom
def draw_extra_nodes(extra_nodes, selected_node):
    node_spacing = WIDTH // 7
    y_position = HEIGHT - 100
    for i, node in enumerate(extra_nodes):
        x_position = (i + 1) * node_spacing
        color = ORANGE if node == selected_node else BLUE
        pygame.draw.circle(screen, color, (x_position, y_position), 20)
        font = pygame.font.Font(None, 26)
        text = font.render(str(node), True, WHITE)
        screen.blit(text, (x_position - text.get_width() // 2, y_position - text.get_height() // 2))

def main():
    tree = BinarySearchTree()
    keys = random.sample(range(1, 100), 7)  # Generates 7 unique random numbers between 1 and 100
    root = tree.get_root(keys)  # Initial balanced BST

    positions = {}
    calculate_positions(root, WIDTH // 2, 50, WIDTH // 4, positions)

    all_possible_values = set(range(0, 101)) - set(keys)
    extra_nodes = random.sample(list(all_possible_values), 6)  # Converts set or dict to a list

    # Calculate the hypothetical minimum height
    total_nodes = len(keys) + len(extra_nodes)
    hypothetical_height = tree.calculate_minimum_height(total_nodes)

    current_node = root  # Initially, start from the root node
    selected_extra_node = None  # No extra node is selected
    color = BLUE
    message = None

    # Run the Pygame loop
    running = True
    while running:
        screen.fill(BG)

        # Recalculate positions to account for AVL rebalancing
        positions = {}
        calculate_positions(root, WIDTH // 2, 50, WIDTH // 4, positions)

        draw_tree(root, positions, current_node, color)  # Draw BST
        draw_extra_nodes(extra_nodes, selected_extra_node)  # Draw extra nodes at the bottom

        # Check if all extra nodes are used
        if not extra_nodes:  # All extra nodes are used
            actual_height = tree.get_height(root)  # Get the actual height of the tree
            is_balanced = tree.isBST(root)  # Check if the tree is balanced

            if is_balanced:
                message = "You Won!"
                color = GREEN
                you_win.play()
            else:
                message = "You Lose!"
                color = RED
                you_loss.play()

            # Disable user actions once the game ends
            current_node = None

            # Draw the back button and message
            font = pygame.font.Font("Tree_Games/Balanced_Tree/Assets/SourGummy-Italic-VariableFont_wdth,wght.ttf", 50)
            text = font.render(message, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

            # Draw Back Button
            back_button_rect = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT // 2 + 100, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(screen, BG, back_button_rect)  # Set button color to BG when game ends
            draw_text("Back", font, BLACK, back_button_rect.centerx, back_button_rect.centery)

            # Event handling for back button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        print("Exiting the game...")
                        running=False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif current_node and event.type == pygame.MOUSEBUTTONDOWN:
                button_click.play()
                selected_extra_node = handle_mouse_click(extra_nodes, selected_extra_node, event)
            elif current_node and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    root, current_node, selected_extra_node, extra_nodes = handle_r_key(
                        tree, root, current_node, selected_extra_node, extra_nodes
                    )
                elif event.key == pygame.K_l:
                    root, current_node, selected_extra_node, extra_nodes = handle_l_key(
                        tree, root, current_node, selected_extra_node, extra_nodes
                    )
                elif event.key == pygame.K_UP:
                    current_node = handle_up_key(root, current_node)

        pygame.display.flip()
        pygame.time.Clock().tick(60)



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
