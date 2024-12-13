import pygame
pygame.mixer.init()

select = pygame.mixer.Sound("Array_Games/Word_Search/Assets/select.mp3")

class WordSearchUI:
    def __init__(self, screen, grid, word_list):
        self.screen = screen
        self.grid = grid
        self.word_list = word_list
        self.cell_size = 35  # Cell size for the grid
        self.letter_gap = 0  # Gap between letters in the grid
        self.font = pygame.font.SysFont("Array_Games/Word_Search/Assets/Roboto-Bold.ttf", 22)  # Font size for letters
        self.title_font = pygame.font.Font("Array_Games/Word_Search/Assets/Roboto-Bold.ttf", 40)
        self.word_font = pygame.font.SysFont("Arial", 20)
        self.selected_cells = []  # Keeps track of currently selected cells
        self.found_words = []  # List of found words
        self.word_cells = {}  # Dictionary to store word and its corresponding grid cells
        self.colors = [
            (173, 216, 230),  # Light Blue
            (144, 238, 144),  # Light Green
            (255, 228, 181),  # Light Orange
            (240, 128, 128),  # Light Coral
            (221, 160, 221),  # Plum
        ]
        self.current_color_index = 0
        
    def draw_title(self):
        # Draw the title at the top of the screen
        screen_width, _ = self.screen.get_size()
        title_surface = self.title_font.render("Search & Conquer", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, 50))  # Adjusted to 50px from the top
        self.screen.blit(title_surface, title_rect)
        
    def get_cell_at_position(self, pos):
        # Identify the grid position from mouse coordinates
        screen_width, screen_height = self.screen.get_size()
        grid_width = len(self.grid[0]) * (self.cell_size + self.letter_gap) - self.letter_gap
        grid_height = len(self.grid) * (self.cell_size + self.letter_gap) - self.letter_gap
        grid_x = (screen_width - grid_width) // 2
        grid_y = 120  # 50px gap from the title

        x, y = pos
        col = (x - grid_x) // (self.cell_size + self.letter_gap)
        row = (y - grid_y) // (self.cell_size + self.letter_gap)
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
            return row, col
        return None

    def draw_grid(self):
        # Calculate grid's top-left position to center it
        grid_width = len(self.grid[0]) * (self.cell_size + self.letter_gap) - self.letter_gap
        grid_height = len(self.grid) * (self.cell_size + self.letter_gap) - self.letter_gap
        screen_width, screen_height = self.screen.get_size()
        grid_x = (screen_width - grid_width) // 2
        grid_y = 120  # 50px gap from the title

        # Draw the border around the entire grid
        pygame.draw.rect(self.screen, (0, 0, 0), (grid_x - 5, grid_y - 5, grid_width + 10, grid_height + 10), 3)

        # Draw the letters in the grid with highlighting for selected cells
        for row_idx, row in enumerate(self.grid):
            for col_idx, letter in enumerate(row):
                x = grid_x + col_idx * (self.cell_size + self.letter_gap)
                y = grid_y + row_idx * (self.cell_size + self.letter_gap)

                # Highlight selected cell
                if (row_idx, col_idx) in self.selected_cells:
                    pygame.draw.rect(self.screen,(173, 216, 230),(x, y, self.cell_size, self.cell_size))  # Light blue for selection highlight
                    card_flip_sound = pygame.mixer.Sound("Array_Games/Word_Search/Assets/select.mp3")
                    card_flip_sound.play()
                # Highlight cells that are part of a found word
                for word, data in self.word_cells.items():
                    if (row_idx, col_idx) in data["cells"]:
                        pygame.draw.rect(
                            self.screen,
                            data["color"],  # Use the stored color for each word
                            (x, y, self.cell_size, self.cell_size)
                        )

                # Draw the letter on top of the cell
                text_surface = self.font.render(letter, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                self.screen.blit(text_surface, text_rect)

        # Return the bottom position of the grid for word list placement
        return grid_y + grid_height

    def mark_found_word(self, word, cells):
        
        color = self.colors[self.current_color_index]
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
 
        self.word_cells[word] = {"cells": cells, "color": color}
 
        self.found_words.append(word)
 
        pygame.display.flip()
        
    def draw_word_list(self, grid_bottom):
        # Draw the word list in a vertical layout below the grid
        screen_width, _ = self.screen.get_size()
        word_list_height = len(self.word_list) * 40  # Adjust the spacing between words
        list_x = (screen_width - 1100) // 2  # Position the list in the center horizontally
        list_y = 125  # Position the list below the grid

        # Draw the border around the word list
        list_width = 200  # Adjust the width of the word list box
        pygame.draw.rect(
            self.screen, (0, 0, 0), (list_x - 10, list_y - 10, list_width + 20, word_list_height + 20), 3, border_radius=15
        )
        pygame.draw.rect(
            self.screen, (22, 68, 81), (list_x - 10, list_y - 10, list_width + 20, word_list_height + 20), 0, border_radius=15
        )

        # Draw the words vertically inside the border
        for idx, word in enumerate(self.word_list):
            word_y = list_y + idx * 40  # Spacing between words vertically

            # Dim the color if the word is found
            color = (169, 169, 169) if word in self.found_words else (255, 255, 255)

            # Render the word with vertical positioning
            text_surface = self.word_font.render(word, True, color)
            text_rect = text_surface.get_rect(center=(list_x + 100, word_y + 20))  # Centered horizontally in the box
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()
