import pygame
import sys
from logic import TicTacToe

pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1050, 700
GRID_SIZE = 3
CELL_SIZE = 200
LINE_WIDTH = 10
MARKER_WIDTH = 15
FONT_SIZE = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
NAVY_BLUE = (0, 0, 64)
BLUE = (0, 0, 255)
DARK_GREY = (105, 105, 105)
O_COLOR = (173, 216, 230)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("XO Arena")

# Load images
background_image = pygame.image.load("Array_Games/Tic_Tac_Toe/Assets/Bg.png") 
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
x_winner_image = pygame.image.load("Array_Games/Tic_Tac_Toe/Assets/XWinner.png")  
x_winner_image = pygame.transform.scale(x_winner_image, (1050, 700)) 
o_winner_image = pygame.image.load("Array_Games/Tic_Tac_Toe/Assets/OWinner.png")  
o_winner_image = pygame.transform.scale(o_winner_image, (1050, 700)) 
draw_image = pygame.image.load("Array_Games/Tic_Tac_Toe/Assets/Draw.png")  
draw_image = pygame.transform.scale(draw_image, (1050, 700))

# Fonts
font = pygame.font.SysFont("arial", FONT_SIZE, bold=True)
myfont = pygame.font.SysFont("arial", 50, bold=True)


# Load sounds
pygame.mixer.init()
click_sound = pygame.mixer.Sound("Array_Games/Tic_Tac_Toe/Assets/BG.mp3")
pygame.mixer.music.load("Array_Games/Tic_Tac_Toe/Assets/BG.mp3")
win_sound = pygame.mixer.Sound("Array_Games/Tic_Tac_Toe/Assets/Win.mp3")
draw_sound = pygame.mixer.Sound("Array_Games/Tic_Tac_Toe/Assets/Draw.mp3")

game = TicTacToe(grid_size=GRID_SIZE)

def draw_grid(): 
    for x in range(1, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (275, (100 + x * 167)), (775, (100 + x * 167)), LINE_WIDTH)
        pygame.draw.line(screen, WHITE, (275 + x * 167, 100), (275 + x * 167, 600), LINE_WIDTH)

def draw_marks(): 
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x_pos = 275 + col * 167
            y_pos = 100 + row * 167            
            if game.grid[row][col] == "X":
                start_pos1 = (x_pos + 30, y_pos + 30)
                end_pos1 = (x_pos + 137, y_pos + 137)
                start_pos2 = (x_pos + 147, y_pos + 20)
                end_pos2 = (x_pos + 20, y_pos + 147)
                pygame.draw.line(screen, NAVY_BLUE, start_pos1, end_pos1, MARKER_WIDTH)
                pygame.draw.line(screen, NAVY_BLUE, start_pos2, end_pos2, MARKER_WIDTH)
            elif game.grid[row][col] == "O":
                center = (x_pos + 83, y_pos + 83)
                radius = 55
                pygame.draw.circle(screen, O_COLOR, center, radius, MARKER_WIDTH)

def display_turn():
    turn_text = f"Player {game.current_player}'s Turn"
    turn_color = NAVY_BLUE if game.current_player == "X" else O_COLOR
    text_surface = myfont.render(turn_text, True, turn_color)
    screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 20))

def display_winner(): 
    global sound_played
    pygame.mixer.music.stop()    
    if game.winner == "X":
        screen.blit(x_winner_image, (0, 0))
        if not sound_played:
            win_sound.play()
            sound_played = True
    elif game.winner == "O":
        screen.blit(o_winner_image, (0, 0))
        if not sound_played:
            win_sound.play()
            sound_played = True
    else:
        screen.blit(draw_image, (0, 0))
        if not sound_played:
            draw_sound.play()
            sound_played = True

def handle_click(pos): 
    x, y = pos
    row = (y - 100) // 167
    col = (x - 275) // 167
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        click_sound.play()
        game.make_move(row, col)

running = True
while running:
    sound_played = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
            handle_click(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN and game.game_over:
            game.reset_game()
            
    screen.blit(background_image, (0, 0))
    draw_grid()
    draw_marks()
    if not game.game_over:
        display_turn()
    if game.game_over:
        display_winner()
    pygame.display.flip()
pygame.quit()
sys.exit()
