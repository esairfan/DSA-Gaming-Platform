import pygame
import sys
from logic import Snake, Maze, generate_food
 
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 20
FPS = 10
BACKGROUND_COLOR = (30, 30, 30)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
WALL_COLOR = (100, 100, 100)
EYE_COLOR = (0, 0, 0)
 
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Evolution")
clock = pygame.time.Clock()
 
initial_snake_positions = [(100, 100), (100, 80), (100, 60), (100, 40)]
snake = Snake(initial_snake_positions)
maze = Maze(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
food = generate_food(snake.get_positions(), maze.walls, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
 
running = True
while running:
    screen.fill(BACKGROUND_COLOR)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != (0, 1):
                snake.direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                snake.direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                snake.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                snake.direction = (1, 0)
 
    if snake.head is None:
        print("Game Over! The snake has no remaining segments.")
        running = False
        continue
 
    snake.move()
 
    if snake.head and snake.head.position == food:
        snake.grow()
        food = generate_food(snake.get_positions(), maze.walls, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
 
    if snake.head and (
        snake.head.position in maze.walls or 
        snake.head.position[0] < 0 or 
        snake.head.position[1] < 0 or 
        snake.head.position[0] >= SCREEN_WIDTH or 
        snake.head.position[1] >= SCREEN_HEIGHT
    ):
        print("Game Over! You hit a wall.")
        running = False
 
    snake.check_collision()
    if snake.has_single_segment():
        print("Game Over! Only one segment remains.")
        running = False
 
    maze.draw(screen, WALL_COLOR)
 
    pygame.draw.rect(screen, FOOD_COLOR, (food[0], food[1], CELL_SIZE, CELL_SIZE))
 
    if snake.head: 
        positions = snake.get_positions()
        for idx, position in enumerate(positions):
            pygame.draw.rect(screen, SNAKE_COLOR, (position[0], position[1], CELL_SIZE - 2, CELL_SIZE - 2))
            if idx == 0:
                eye_radius = CELL_SIZE // 8
                left_eye = (position[0] + CELL_SIZE // 4, position[1] + CELL_SIZE // 4)
                right_eye = (position[0] + 3 * CELL_SIZE // 4, position[1] + CELL_SIZE // 4)
                pygame.draw.circle(screen, EYE_COLOR, left_eye, eye_radius)
                pygame.draw.circle(screen, EYE_COLOR, right_eye, eye_radius)
 
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
