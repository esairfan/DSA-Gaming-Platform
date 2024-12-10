import random
import string

class WordSearchLogic:
    def __init__(self, grid_size, word_count=8):
        self.grid_size = grid_size
        self.word_pool = [
            "PYTHON", "GAME", "SEARCH", "WORD", "ALGORITHM", "PUZZLE", "PROGRAMMING",
            "DEVELOPER", "DEBUG", "LOGIC", "GRAPHICS", "INTERFACE", "DISPLAY", "EVENT",
            "LOOP", "FUNCTION", "VARIABLE", "CONDITION", "ARRAY", "STRING", "INTEGER",
            "BOOLEAN", "OBJECT", "CLASS", "METHOD", "MODULE", "IMPORT", "EXPORT",
            "DATABASE", "QUERY", "NETWORK", "SERVER", "CLIENT", "PYGAME", "RECURSION",
            "STACK", "QUEUE", "HEAP", "SORT", "SEARCHING", "COMPILER", "INTERPRETER",
            "ENCRYPT", "DECRYPT", "BINARY", "DEBUGGING", "OPTIMIZATION", "THREADING",
            "CONCURRENCY", "SYNCHRONIZE", "PARALLEL", "MATRIX", "VECTOR", "GRAPH",
            "TREE", "TRAVERSAL", "DEPTH", "BREADTH", "ALPHA", "BETA", "DELTA", "GAMMA"
        ]
        self.word_list = random.sample(self.word_pool, word_count)
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
        word = "".join(selected_sequence)
        return word in self.word_list
    
    def get_grid(self):
        return self.grid

    def get_word_list(self):
        return self.word_list
