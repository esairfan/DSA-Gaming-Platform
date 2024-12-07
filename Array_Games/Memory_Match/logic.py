import random

# Constants
GRID_ROWS = 6
GRID_COLS = 5
ITEMS = [
    "apple", "bird", "brinjal", "candle", "candy",
    "cherry", "cookie", "grape", "heart", "lolly",
    "mushroom", "pepper", "santa", "snake", "snow"
]

def create_grid(rows, cols):
    """Create a grid with shuffled pairs of items."""
    items = ITEMS.copy()  # Use the global ITEMS list
    if rows * cols % 2 != 0:
        raise ValueError("Grid must have an even number of cells for pairs.")
    
    required_pairs = rows * cols // 2  # Calculate the required number of pairs

    # Check if there are enough unique items
    if len(items) < required_pairs:
        raise ValueError("Not enough unique items to fill the grid.")
    
    # Duplicate and shuffle items
    pairs = items[:required_pairs] * 2  # Limit to required unique items and create pairs
    random.shuffle(pairs)

    # Create the grid
    grid = [[pairs.pop() for _ in range(cols)] for _ in range(rows)]
    return grid

def is_match(grid, first, second):
    """Check if two positions in the grid match."""
    if not all(0 <= idx[0] < len(grid) and 0 <= idx[1] < len(grid[0]) for idx in [first, second]):
        raise IndexError("One or both indices are out of grid bounds.")
    return grid[first[0]][first[1]] == grid[second[0]][second[1]]

def all_matched(matched):
    """
    Check if all cards are matched.

    Parameters:
        matched (list[list[bool]]): A 2D list representing the matched state of the grid.
    Returns:
        bool: True if all cards are matched, False otherwise.
    """
    return all(all(row) for row in matched)
