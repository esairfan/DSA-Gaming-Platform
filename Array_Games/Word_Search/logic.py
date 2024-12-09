import random
import string

class WordSearchLogic:
    def __init__(self, grid_size, word_list):
        self.grid_size = grid_size
        self.word_list = word_list
        self.grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]

    def place_words(self):
        directions = ["horizontal", "vertical"]
        for word in self.word_list:
            placed = False
            while not placed:
                direction = random.choice(directions)
                row, col = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
                placed = self.try_place_word(word, row, col, direction)

    def try_place_word(self, word, row, col, direction):
        length = len(word)
        if direction == "horizontal" and col + length <= self.grid_size:
            if all(self.grid[row][col + i] in ["", word[i]] for i in range(length)):
                for i in range(length):
                    self.grid[row][col + i] = word[i]
                return True
        elif direction == "vertical" and row + length <= self.grid_size:
            if all(self.grid[row + i][col] in ["", word[i]] for i in range(length)):
                for i in range(length):
                    self.grid[row + i][col] = word[i]
                return True
        return False

    def fill_random_letters(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.grid[row][col] == "":
                    self.grid[row][col] = random.choice(string.ascii_uppercase)
                    
    def is_valid_word(self, selected_sequence):
        """
        Check if the selected sequence forms a valid word.
        """
        word = "".join(selected_sequence)
        return word in self.word_list
    
    def get_grid(self):
        return self.grid
