import pygame
import sys
from logic import TicTacToe

pygame.init()
 
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 3
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
LINE_WIDTH = 10
MARKER_WIDTH = 15
FONT_SIZE = 100
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
 
font = pygame.font.Font(None, FONT_SIZE)
 
game = TicTacToe(grid_size=GRID_SIZE)


def draw_grid(): 
    screen.fill(WHITE)
    for x in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, SCREEN_HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (0, x * CELL_SIZE), (SCREEN_WIDTH, x * CELL_SIZE), LINE_WIDTH)


def draw_marks(): 
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if game.grid[row][col] == "X":
                start_pos1 = (col * CELL_SIZE + 20, row * CELL_SIZE + 20)
                end_pos1 = ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20)
                start_pos2 = ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20)
                end_pos2 = (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20)
                pygame.draw.line(screen, RED, start_pos1, end_pos1, MARKER_WIDTH)
                pygame.draw.line(screen, RED, start_pos2, end_pos2, MARKER_WIDTH)
            elif game.grid[row][col] == "O":
                center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
                radius = CELL_SIZE // 3
                pygame.draw.circle(screen, BLUE, center, radius, MARKER_WIDTH)


def display_winner(): 
    if game.winner:
        text = font.render(f"{game.winner} Wins!", True, BLACK)
    else:
        text = font.render("Draw!", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)


def handle_click(pos): 
    x, y = pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    game.make_move(row, col)

 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
            handle_click(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN and game.game_over:
            game.reset_game()

    draw_grid()
    draw_marks()
    if game.game_over:
        display_winner()

    pygame.display.flip()

pygame.quit()
sys.exit()
