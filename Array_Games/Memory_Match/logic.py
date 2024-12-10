import random
import pygame

# Define card dimensions
CARD_WIDTH = 45
CARD_HEIGHT = 80
MARGIN = 50
GRID_SIZE = 6  # 6x6 grid

colors = {
    'text': (255, 255, 255),  # White text for symbols
}
card_back_image = pygame.image.load("Array_Games/Memory_Match/Assets/cardbackground.png")  # Replace "card_back.png" with your actual image path
card_back_image = pygame.transform.scale(card_back_image, (CARD_WIDTH, CARD_HEIGHT))

# Define the Card class
class Card:
    def __init__(self, symbol, x, y):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.is_flipped = False
        self.is_matched = False

    def draw(self, screen, font, colors):
        if not self.is_flipped:
            screen.blit(card_back_image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, colors['flipped'], (self.x, self.y, CARD_WIDTH, CARD_HEIGHT))
            text = font.render(self.symbol, True, colors['text'])
            screen.blit(text, (self.x + CARD_WIDTH // 4, self.y + CARD_HEIGHT // 4))
            
        pygame.draw.rect(screen, (0, 0, 0), (self.x-2, self.y-2, CARD_WIDTH+6, CARD_HEIGHT+6), 6, border_radius=10)
        
    def is_clicked(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + CARD_WIDTH and self.y <= mouse_y <= self.y + CARD_HEIGHT


# Function to generate a shuffled set of symbols
def generate_card_symbols():
    symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I','J','K','L', 'M','N','O','P','Q','R']
    symbols = symbols * 2  # Duplicate each symbol to create pairs
    random.shuffle(symbols)
    return symbols


# Function to create the grid of cards
def create_grid():
    symbols = generate_card_symbols()
    cards = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = j * (CARD_WIDTH + MARGIN)
            y = i * (CARD_HEIGHT + MARGIN)
            card = Card(symbols.pop(), x, y)
            cards.append(card)
    return cards

# Function to check if two cards match
def check_match(card1, card2):
    return card1.symbol == card2.symbol
