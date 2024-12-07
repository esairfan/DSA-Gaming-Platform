import random
import pygame 

class Node:
    def __init__(self, position):
        self.position = position
        self.next = None
 
class Snake:
    def __init__(self, initial_positions):
        self.head = None
        self.tail = None
        self.direction = (0, 1)
        self.create_snake(initial_positions)

    def create_snake(self, positions): 
        for pos in positions:
            self.add_node(pos)

    def add_node(self, position): 
        new_node = Node(position)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def get_positions(self): 
        positions = []
        current = self.head
        while current:
            positions.append(current.position)
            current = current.next
        return positions

    def move(self): 
        if not self.head:
            return
        new_head_pos = (
            self.head.position[0] + self.direction[0] * 20,
            self.head.position[1] + self.direction[1] * 20,
        ) 
        new_head = Node(new_head_pos)
        new_head.next = self.head
        self.head = new_head
        current = self.head
        while current.next and current.next.next:
            current = current.next
        self.tail = current
        self.tail.next = None

    def grow(self): 
        if self.tail:
            self.tail.next = Node(self.tail.position)
            self.tail = self.tail.next

    def check_collision(self): 
        current = self.head.next
        while current:
            if self.head.position == current.position:
                print("Collision detected! Trimming the snake.")
                current.next = None
                
                return True
            current = current.next
        return False

    def has_single_segment(self): 
        return self.head and self.head.next is None
 
class Maze:
    def __init__(self, screen_width, screen_height, cell_size):
        self.cell_size = cell_size
        self.walls = self.generate_walls(screen_width, screen_height)

    def generate_walls(self, screen_width, screen_height):
        walls = []
        for _ in range(50):
            x = random.randint(0, screen_width // self.cell_size - 1) * self.cell_size
            y = random.randint(0, screen_height // self.cell_size - 1) * self.cell_size
            if (1200 <= x < 1200 + 200 and 50 <= y < 50 + 50):
                continue
            walls.append((x, y))
        return walls

    def draw(self, screen):
        apple_image = pygame.image.load("Assets/Rock2.png")
        apple_image = pygame.transform.scale(apple_image, (20, 20))
        for wall in self.walls:
            screen.blit(apple_image, (wall[0], wall[1]))


def generate_food(snake_positions, walls, screen_width, screen_height, cell_size):
    # Load and scale the apple image
    apple_image = pygame.image.load("Linked_List_games/Snake_Evolution/Assets/Food.png")
    apple_image = pygame.transform.scale(apple_image, (30, 30))  # Scale to fit the grid

    while True:
        # Generate a random food position aligned to the grid
        x = random.randint(0, screen_width // cell_size - 1) * cell_size
        y = random.randint(0, screen_height // cell_size - 1) * cell_size

        # Check if the generated coordinates are outside the restricted rectangle
        if (1200 <= x < 1200 + 200 and 50 <= y < 50 + 50):
            continue
        food_position = (x, y)

        # Ensure the position does not overlap with the snake or walls
        if food_position not in snake_positions and food_position not in walls:
            return food_position, apple_image

def draw_food(screen, food_position, apple_image):
    # Draw the food image at the exact grid position
    screen.blit(apple_image, food_position)