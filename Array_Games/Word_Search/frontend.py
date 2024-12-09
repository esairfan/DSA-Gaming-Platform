import pygame

class WordSearchUI:
    def __init__(self, screen, grid, word_list):
        self.screen = screen
        self.grid = grid
        self.word_list = word_list
        self.font = pygame.font.Font(None, 36)
        self.cell_size = 40
        self.selected_cells = []  # Track currently selected cells (tuples of (row, col))
        self.highlighted_cells = []  # Track permanently highlighted cells for found words
        self.found_words = []  # Track found words

    def draw_grid(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                x = col * self.cell_size
                y = row * self.cell_size

                # Determine cell color
                if (row, col) in self.highlighted_cells:
                    color = (150, 250, 150)  # Highlighted color for found words
                elif (row, col) in self.selected_cells:
                    color = (200, 250, 200)  # Temporary highlight color
                else:
                    color = (200, 200, 200)  # Default color

                # Draw the cell
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size), 1)

                # Draw the letter
                letter = self.grid[row][col]
                text_surface = self.font.render(letter, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                self.screen.blit(text_surface, text_rect)

    def draw_word_list(self):
        x, y = len(self.grid) * self.cell_size + 20, 20
        for word in self.word_list:
            color = (100, 100, 100) if word in self.found_words else (0, 0, 0)
            text_surface = self.font.render(word, True, color)
            self.screen.blit(text_surface, (x, y))
            y += 30

    def mark_found_word(self, word, cells):
        """
        Mark a word as found by adding it to the found_words list,
        removing it from the word list, and storing its cells.
        """
        if word in self.word_list:
            self.found_words.append(word)
            self.word_list.remove(word)
            self.highlighted_cells.extend(cells)  # Save positions of found word's letters

    def get_cell_at_position(self, pos):
        """
        Convert a mouse position to grid coordinates.
        """
        x, y = pos
        row = y // self.cell_size
        col = x // self.cell_size
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
            return row, col
        return None
