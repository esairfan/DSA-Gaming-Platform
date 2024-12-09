class TicTacToe:
    def __init__(self, grid_size=3):
        self.grid_size = grid_size
        self.grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]
        self.current_player = "X"
        self.winner = None
        self.game_over = False

    def reset_game(self):
        """Reset the game state."""
        self.grid = [["" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.current_player = "X"
        self.winner = None
        self.game_over = False 
        # Restart the background music
    # Other reset logic
        global sound_played
        sound_played = False

    def make_move(self, row, col):
        """Place a mark at the given position if valid."""
        if not self.game_over and self.grid[row][col] == "":
            self.grid[row][col] = self.current_player
            self.check_winner()
            if not self.game_over:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        """Check if the current move leads to a win or draw."""
        # Check rows and columns
        for i in range(self.grid_size):
            if all(self.grid[i][j] == self.current_player for j in range(self.grid_size)):
                self.winner = self.current_player
                self.game_over = True
                return
            if all(self.grid[j][i] == self.current_player for j in range(self.grid_size)):
                self.winner = self.current_player
                self.game_over = True
                return

        # Check diagonals
        if all(self.grid[i][i] == self.current_player for i in range(self.grid_size)):
            self.winner = self.current_player
            self.game_over = True
            return
        if all(self.grid[i][self.grid_size - 1 - i] == self.current_player for i in range(self.grid_size)):
            self.winner = self.current_player
            self.game_over = True
            return

        # Check for a draw
        if all(self.grid[row][col] != "" for row in range(self.grid_size) for col in range(self.grid_size)):
            self.game_over = True
