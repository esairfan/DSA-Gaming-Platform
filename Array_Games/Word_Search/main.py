import pygame
from logic import WordSearchLogic
from frontend import WordSearchUI
pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((1200, 700))
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_COLOR = (39, 50, 64)  # Green color for the buttons
BUTTON_HOVER_COLOR = (69, 80, 94)  # Darker green for button hover
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



def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def main():
    grid_size = 12
    word_count = 10  # Total words to display

    logic = WordSearchLogic(grid_size, word_count)
    logic.place_words()
    logic.fill_random_letters()

    screen = pygame.display.set_mode((1200, 700))  # Adjusted screen size
    pygame.display.set_caption("Word Seeker")
    ui = WordSearchUI(screen, logic.get_grid(), logic.get_word_list())

    # Back button settings
    BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
    BUTTON_COLOR = (34, 103, 119)  # Red color for the button
    button_rect = pygame.Rect(20, 20, BUTTON_WIDTH, BUTTON_HEIGHT)
    font = pygame.font.SysFont("arial", 24, bold=True)
    BUTTONTEXTCOLOR=(255,255,255)
    back_button = Button(100, 10, 100, 50, 'Back', (0, 0, 0, 0), BUTTONTEXTCOLOR, 6)

    running = True
    selecting = False
    selected_sequence = []
    selected_cells = []

    while running:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle button click
                mouse_pos=pygame.mouse.get_pos()
                if back_button.is_clicked(mouse_pos):
                    print("Back button clicked!")
                    running = False

                cell = ui.get_cell_at_position(pygame.mouse.get_pos())
                if cell:
                    selecting = True
                    ui.selected_cells = [cell]
                    selected_cells = [cell]
                    selected_sequence = [ui.grid[cell[0]][cell[1]]]
            elif event.type == pygame.MOUSEMOTION:
                if selecting:
                    cell = ui.get_cell_at_position(pygame.mouse.get_pos())
                    if cell and cell not in ui.selected_cells:
                        ui.selected_cells.append(cell)
                        selected_cells.append(cell)
                        selected_sequence.append(ui.grid[cell[0]][cell[1]])

            elif event.type == pygame.MOUSEBUTTONUP:
                if selecting:
                    selecting = False
                    selected_word = "".join(selected_sequence)
                    if logic.is_valid_word(selected_sequence):
                        print(f"Word Found: {selected_word}")
                        ui.mark_found_word(selected_word, selected_cells)
                    else:
                        print(f"Invalid Word: {selected_word}")
                    ui.selected_cells = []  # Reset selected cells after selection
            screen.fill((34, 103, 119))
            # Drawing UI elements
            ui.draw_title(back_button)
            grid_bottom = ui.draw_grid(back_button)
            ui.draw_word_list(grid_bottom, back_button)
            # Draw the button with the fixed color (no hover effect)

            # pygame.display.flip()





def restart_game():
    # Initialize Pygame
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
    #main()
    restart_game()
