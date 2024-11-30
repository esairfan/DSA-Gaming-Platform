import pygame
import sys
import os
import time
from logic import *
 
SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 700
CELL_SIZE = 20
FPS = 10
BACKGROUND_COLOR = (102, 205, 102)
SNAKE_COLOR = (65, 105, 225)
food_position_COLOR = (255, 0, 0)
WALL_COLOR = (100, 100, 100)
EYE_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
apple_image=None
pygame.init()
font = pygame.font.Font("Assets/SourGummy-VariableFont_wdth,wght.ttf", 30)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Serpentine Symphony")
clock = pygame.time.Clock()
pygame.display.set_caption('Solitaire Game')
# pygame.mixer.music.load("Pictures/Sound.mp3")
# pygame.mixer.music.set_volume(1.0)
# pygame.mixer.music.play(-1)

initial_snake_positions = [(100, 100), (100, 80), (100, 60), (100, 40)]
snake = Snake(initial_snake_positions)
maze = Maze(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
food_position, apple_image = generate_food(initial_snake_positions, maze.walls, SCREEN_WIDTH, SCREEN_HEIGHT, maze.cell_size)

def UpdateScore(val):
    global score
    score += val
def DisplayScore():
    font1 = pygame.font.Font("Assets/static/EduAUVICWANTPre-Bold.ttf", 30)
    scoreText = f"Score: {score}"
    textSurface = font1.render(scoreText, True, (255, 255, 255))
    screen.blit(textSurface, (30, 170))
def GamePlay():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load('Assets/2.png')
    background_image=pygame.transform.scale(background_image, (1400, 700))
    global food_position, apple_image
    running = True
    while running:
        screen.blit(background_image, (0,0))
        draw_food(screen, food_position, apple_image)
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
        if snake.head and is_collision(snake.head.position, food_position):
            snake.grow()
            food_position, apple_image = generate_food(snake.get_positions(), maze.walls, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
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
        #pygame.draw.rect(screen, food_position_COLOR, (food_position[0], food_position[1], CELL_SIZE, CELL_SIZE))
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
def DrawRoundedRect(surface, color, rect, radius):
    roundedRectSurface = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(roundedRectSurface, color, (0, 0, rect.width, rect.height), border_radius=radius)
    surface.blit(roundedRectSurface, rect.topleft)
def DrawButtonWithBorder(surface, color, borderColor, rect, radius):
    DrawRoundedRect(surface, color, rect, radius)
    pygame.draw.rect(surface, borderColor, rect, width=2, border_radius=radius)
def is_collision(snake_position, food_position):
    # Extract snake head position
    snake_x, snake_y = snake_position
    # Extract food position
    food_x, food_y = food_position

    # Check if the snake's head is within the 20x20 rectangle around the food
    if food_x <= snake_x < food_x + 30 and food_y <= snake_y < food_y + 30:
        return True
    return False
class Button:
    def __init__(self, x, y, width, height, color, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def draw(self, screen):
        DrawButtonWithBorder(screen, self.color, WHITE, self.rect, radius=10)
        textSurface = font.render(self.text, True, WHITE)
        screen.blit(textSurface, (self.rect.x + (self.rect.width - textSurface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - textSurface.get_height()) // 2))
    def IsClicked(self, mousePos):
        return self.rect.collidepoint(mousePos)

if __name__ == "__main__":
    GamePlay()
    pygame.quit()
    sys.exit()
