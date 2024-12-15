import pygame
import sys
import os
from subprocess import Popen
# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 1383
SCREEN_HEIGHT = 512
BUTTONTEXTCOLOR = (255, 255, 255)
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{50},{50}"

class Button:
    def __init__(self, x, y, width, height, text, bg_color, text_color, 
                 border_radius=0, border_color=None, border_width=0, font_path=None, font_size=36):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_width = border_width
        # Load custom font or use default
        self.font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.Font(None, font_size)
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, screen):
        # Draw the border if needed
        if self.border_width > 0 and self.border_color:
            pygame.draw.rect(
                screen, 
                self.border_color, 
                self.rect, 
                border_radius=self.border_radius, 
                width=self.border_width
            )
        # Draw the button background
        pygame.draw.rect(
            screen, 
            self.bg_color, 
            self.rect, 
            border_radius=self.border_radius
        )
        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.is_hovered(pos)



aboutUs_button = Button(548, 335, 289, 57, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)
start_button = Button(548, 265, 289, 57, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)
quiz_button = Button(548, 193, 289, 57, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)
exit_button = Button(548, 406, 289, 57, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)

snake_game_button = Button(23, 129, 204, 183, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)
towerofhanoi_game_button = Button(249, 129, 204, 183, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)
fillupthebottle_game_button = Button(481, 129, 204, 183, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)
tictactoe_game_button = Button(710, 129, 204, 183, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)
memorymatch_game_button = Button(936, 129, 204, 183, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)
mazesolve_game_button = Button(1171, 129, 204, 183, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)
balanacetree_game_button = Button(136, 351, 204, 183, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)
wordsearch_game_button = Button(367, 351, 204, 183, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)
traversaltycon_game_button = Button(596, 351, 204, 183, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)
railwaytycon_game_button = Button(825, 351, 204, 183, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)
eulerpath_game_button = Button(1056, 351, 204, 183, '', (0, 0, 0, 0), BUTTONTEXTCOLOR)

def StartGame():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("DSA Gaming Platform")
    image = pygame.image.load("MainPAge/Assets/Hamdan.png")
    image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.is_clicked(mouse_pos):
                        print("Start Game button clicked")
                        play_games()
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        pygame.display.set_caption("DSA Gaming Platform")
                        image = pygame.image.load("MainPAge/Assets/Hamdan.png")
                        image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))

                    elif exit_button.is_clicked(mouse_pos):
                        print("Exit button clicked")
                        running = False# Exit the game
                    elif aboutUs_button.is_clicked(mouse_pos):
                        print("About Us button clicked")
                        about_us()
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        pygame.display.set_caption("DSA Gaming Platform")
                        image = pygame.image.load("MainPAge/Assets/Hamdan.png")
                        image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))

                    elif quiz_button.is_clicked(mouse_pos):
                        print("Quiz button clicked")
                        Popen(['python', 'Quiz_Menu/quiz.py'])
                        
                        

        screen.blit(image, (0, 0))
        # start_button.draw(screen)
        # aboutUs_button.draw(screen)
        # quiz_button.draw(screen)
        # exit_button.draw(screen)
        pygame.display.flip()

def about_us():
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{50},{50}"
    # Set up the screen dimensions and caption
    screen = pygame.display.set_mode((1400, 700))
    pygame.display.set_caption("About Us")
    
    # Load and scale the background image
    background_image = pygame.image.load("MainPAge/Assets/help_page.png")
    background_image = pygame.transform.scale(background_image, (1400, 700))
    
    back_button = Button(
        1250, 620, 100, 50, 'Back', 
        (39, 50, 64), (255, 255, 255), 
        border_radius=10, border_color=(255, 255, 255), border_width=2,
        font_path="MainPAge/Assets/BlackOpsOne-Regular.ttf", font_size=24
    )  # Red button with white text
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button.is_clicked(mouse_pos):
                        print("Back button clicked")
                        running=False
        # Draw the background and the back button
        screen.blit(background_image, (0, 0))
        back_button.draw(screen)
        pygame.display.flip()



def play_games():
    screen = pygame.display.set_mode((1400, 700))
    pygame.display.set_caption("Play Games")
    
    # Load and scale the background image
    background_image = pygame.image.load("MainPAge/Assets/gamebg.png")
    background_image = pygame.transform.scale(background_image, (1400, 700))

    back_button = Button(
        1250, 620, 100, 50, 'Back', 
        (39, 50, 64), (255, 255, 255), 
        border_radius=10, border_color=(255, 255, 255), border_width=2,
        font_path="MainPAge/Assets/BlackOpsOne-Regular.ttf", font_size=24
    )  # Red button with white text
    
    # Main game loop for the play_games screen
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button.is_clicked(mouse_pos):
                        print("Back button clicked")
                        running = False
                    elif snake_game_button.is_clicked(mouse_pos):
                        print("Snake Game button clicked")
                        Popen(['python', 'Linked_List_games/Snake_Evolution/Frontend.py'])
                    elif towerofhanoi_game_button.is_clicked(mouse_pos):
                        print("Tower of Hanoi Game button clicked")
                        Popen(['python', 'Stack_Games/TowerOfHanoi/Mainfrontend.py'])
                    elif fillupthebottle_game_button.is_clicked(mouse_pos):
                        print("Fill Up The Bottle Game button clicked")
                        Popen(['python', 'Stack_Games/FillUpTheBottle/frontend.py'])
                    elif tictactoe_game_button.is_clicked(mouse_pos):
                        print("Tic Tac Toe Game button clicked")
                        Popen(['python', 'Array_Games/Tic_Tac_Toe/Frontend.py'])
                    elif memorymatch_game_button.is_clicked(mouse_pos):
                        print("Memory Match Game button clicked")
                        Popen(['python', 'Array_Games/Memory_Match/Frontend.py'])
                    elif mazesolve_game_button.is_clicked(mouse_pos):
                        print("Maze Solve Game button clicked")
                        Popen(['python', 'Graph_Games/Maze_Game/main.py'])
                    elif balanacetree_game_button.is_clicked(mouse_pos):
                        print("Balance Tree Game button clicked")
                        Popen(['python', 'Tree_Games/Balanced_Tree/frontend.py'])
                    elif wordsearch_game_button.is_clicked(mouse_pos):
                        print("Word Search Game button clicked")
                        Popen(['python', 'Array_Games/Word_Search/main.py'])
                    elif traversaltycon_game_button.is_clicked(mouse_pos):
                        print("Traversal Tycon Game button clicked")
                        Popen(['python', 'Tree_Games/Travesal_Tycon/supportiveFrontend.py'])
                    elif railwaytycon_game_button.is_clicked(mouse_pos):
                        print("Railway Tycon Game button clicked")
                        Popen(['python', 'Graph_Games/railway_tycon/frontend.py'])
                    elif eulerpath_game_button.is_clicked(mouse_pos):
                        print("Euler Path Game button clicked")
                        Popen(['python', 'Graph_Games/one_way_out/frontend.py'])
                        
        
        # Draw the background image
        screen.blit(background_image, (0, 0))
        back_button.draw(screen)
        pygame.display.flip()

        

if __name__ == "__main__":
    StartGame()
    pygame.quit()
    sys.exit()
