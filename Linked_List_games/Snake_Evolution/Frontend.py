import pygame
import sys
import os
import time
from logic import *
import msvcrt

SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 700
CELL_SIZE = 20
FPS = 10
score=0
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
font = pygame.font.Font("Linked_List_games/Snake_Evolution/Assets/SourGummy-VariableFont_wdth,wght.ttf", 30)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Serpentine Symphony")
clock = pygame.time.Clock()
pygame.display.set_caption('Solitaire Game')
# pygame.mixer.music.load("Assets/Bg.m4a")
# pygame.mixer.music.set_volume(1.0)
# pygame.mixer.music.play(-1)

initial_snake_positions = [(100, 100), (100, 80), (100, 60), (100, 40)]
snake = Snake(initial_snake_positions)
maze = Maze(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
walls = maze.generate_walls(SCREEN_WIDTH, SCREEN_HEIGHT)
food_position, apple_image = generate_food(initial_snake_positions, maze.walls, SCREEN_WIDTH, SCREEN_HEIGHT, maze.cell_size)

def UpdateScore(val):
    global score
    score += val
def DisplayScore():
    apple_image = pygame.image.load("Linked_List_games/Snake_Evolution/Assets/Food.png")
    apple_image = pygame.transform.scale(apple_image, (50, 50))
    font1 = pygame.font.Font("Linked_List_games/Snake_Evolution/Assets/static/EduAUVICWANTPre-Bold.ttf", 30)
    screen.blit(apple_image, (1250, 50))
    scoreText = f"={score}"
    textSurface = font1.render(scoreText, True, (255, 0, 0))
    screen.blit(textSurface, (1300, 53))
def play_background_music():
    pygame.mixer.init()  
    pygame.mixer.music.load("Linked_List_games/Snake_Evolution/Assets/Bg.mp3")
    pygame.mixer.music.set_volume(1.0)  
    pygame.mixer.music.play(-1)  
def play_background_music_for_Food():
    food_sound = pygame.mixer.Sound("Linked_List_games/Snake_Evolution/Assets/Food.ogg")  # Load the food sound
    food_sound.set_volume(1.0)  # Set volume
    food_sound.play()  
def play_background_music_for_Collision():
    food_sound = pygame.mixer.Sound("Linked_List_games/Snake_Evolution/Assets/Pathar.mp3")  # Load the food sound
    food_sound.set_volume(1.0)  # Set volume
    food_sound.play() 
def play_background_music_for_Bite_Snake():
    food_sound = pygame.mixer.Sound("Linked_List_games/Snake_Evolution/Assets/Bite.mp3")  # Load the food sound
    food_sound.set_volume(1.0)  # Set volume
    food_sound.play() 
def GamePlay():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load('Linked_List_games/Snake_Evolution/Assets/2.png')
    background_image=pygame.transform.scale(background_image, (1400, 700))
    global food_position, apple_image, score, FPS
    running = True 
    paused = False 
    calculate=None
    screen.blit(background_image, (0,0))
    maze.draw(screen)
    draw_food(screen, food_position, apple_image)
    DisplayScore()
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
    wait_for_keypress(screen)
    while running:
        DisplayScore()
        draw_food(screen, food_position, apple_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    PauseGame()   # Toggle pause state
                elif not paused:  # Handle other keypresses only when not paused
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)

        if paused:
            continue  # Skip the game logic when paused
        if snake.head is None:
            print("Game Over! The snake has no remaining segments.")
            play_background_music_for_Collision()
            running = False
            continue
        snake.move()
        if snake.head and is_collision(snake.head.position, food_position):
            snake.grow()
            play_background_music_for_Food()
            UpdateScore(1)
            calculate=None
            food_position, apple_image = generate_food(snake.get_positions(), maze.walls, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
        if snake.head and (
            snake.head.position in maze.walls or 
            snake.head.position[0] < 0 or 
            snake.head.position[1] < 0 or 
            snake.head.position[0] >= SCREEN_WIDTH or 
            snake.head.position[1] >= SCREEN_HEIGHT
        ):
            print("Game Over! You hit a wall.")
            play_background_music_for_Collision()
            running = False
        
        if(snake.check_collision()):
            { play_background_music_for_Bite_Snake() }
        
        if snake.has_single_segment():
            play_background_music_for_Collision()
            print("Game Over! Only one segment remains.")
            running = False
        maze.draw(screen)
        if score%10==0 and score!=0  and calculate!=1:
            calculate=1
            FPS+=2
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
        screen.blit(background_image, (0,0))
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
    if food_x <= snake_x < food_x + 20 and food_y <= snake_y < food_y + 20:
        return True
    return False
def wait_for_keypress(screen):
    waiting=True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Allow quitting during the wait
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # Start game on key press
                waiting = False
def PauseGame():
    # Load the background image for pause screen
    background_image = pygame.image.load('Assets/Pause.png')
    background_image = pygame.transform.scale(background_image, (1400, 700))  # Adjust size if needed
    
    # Create the screen (if not already created)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Display the pause screen
    screen.blit(background_image, (0, 0))  # Draw the image on the screen
    
    # Update the display
    pygame.display.flip()

    # Wait for the user to press the space bar to resume
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Space bar to resume the game
                    waiting_for_key = False  # Exit the loop and resume the game
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
    play_background_music()
    GamePlay()
    pygame.quit()
    sys.exit()
