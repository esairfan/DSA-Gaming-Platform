import pygame
from logic import FillUpTheBottle

# Constants for screen and bottle sizes
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
BOTTLE_WIDTH, BOTTLE_HEIGHT = 100, 300
BALL_RADIUS = 25
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
]

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
back_button_rect = pygame.Rect(900, 600, 200, 50)

# Load images
background_image = pygame.image.load("Stack_Games/FillUpTheBottle/Assets/bg2.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
win_image = pygame.image.load("Stack_Games/FillUpTheBottle/Assets/YouWin.png")
win_image = pygame.transform.scale(win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load sounds
pygame.mixer.init()
invalid_move_sound = pygame.mixer.Sound("Stack_Games/FillUpTheBottle/Assets/BallMoveSound (mp3cut.net).mp3")
bottle_click_sound = pygame.mixer.Sound("Stack_Games/FillUpTheBottle/Assets/BottleClickSound (mp3cut.net).mp3")
ball_move_sound = pygame.mixer.Sound("Stack_Games/FillUpTheBottle/Assets/Invalid.mp3")


pygame.display.set_caption("Hydro Hustle")
clock = pygame.time.Clock()
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_COLOR = (39, 50, 64)  # Green color for the buttons
BUTTON_HOVER_COLOR = (69, 80, 94)  # Darker green for button hover
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


class FillUpTheBottleFrontend:
    def __init__(self, game):
        self.game = game
        self.ball_pos = None
        self.selected_bottle = None

    def draw_rounded_rect(self, surface, color, rect, radius=10):
        x, y, width, height = rect
        pygame.draw.rect(surface, color, (x + radius, y, width - 2 * radius, height))
        pygame.draw.rect(surface, color, (x, y + radius, width, height - 2 * radius))
        pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
        pygame.draw.circle(surface, color, (x + width - radius, y + radius), radius)
        pygame.draw.circle(surface, color, (x + radius, y + height - radius), radius)
        pygame.draw.circle(surface, color, (x + width - radius, y + height - radius), radius)
        
    def draw_bottles(self, screen, selected_bottle=None):
        num_bottles = len(self.game.get_bottles()) 
        total_width = num_bottles * BOTTLE_WIDTH + (num_bottles - 1) * 50
        x_offset = (SCREEN_WIDTH - total_width) // 2
        y_base = SCREEN_HEIGHT - 150
        for i, bottle in enumerate(self.game.get_bottles()):
             
            bottle_top = y_base - BOTTLE_HEIGHT
            neck_radius = 12.5
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (x_offset + BOTTLE_WIDTH // 2, bottle_top + neck_radius),
                neck_radius,
                5
            )
            bottle_body_rect = pygame.Rect(x_offset, bottle_top + 25, BOTTLE_WIDTH, BOTTLE_HEIGHT - 25)
            self.draw_rounded_rect(screen, (255, 255, 255), bottle_body_rect, radius=10)
            y_ball = bottle_top + BOTTLE_HEIGHT - BALL_RADIUS - 35
            for ball_idx, ball in enumerate(bottle):
                if self.ball_pos and i == self.ball_pos[0] and ball_idx == len(bottle) - 1:
                    # Skip drawing the ball currently in motion
                    continue
                color = COLORS[ball - 1]  
                pygame.draw.circle(
                    screen, color, (x_offset + BOTTLE_WIDTH // 2, y_ball + 30), BALL_RADIUS
                )
                y_ball -= 2 * BALL_RADIUS + 5
            if self.ball_pos and i == self.ball_pos[0]:
                ball_color = COLORS[self.ball_pos[1] - 1]
                pygame.draw.circle(
                    screen, ball_color, (x_offset + BOTTLE_WIDTH // 2, self.ball_pos[2]), BALL_RADIUS
                )
            x_offset += BOTTLE_WIDTH + 50
        pygame.display.flip()

    def animate_ball_upward(self): 
        if self.ball_pos:
            ball_y_pos = self.ball_pos[2]
            if ball_y_pos > 220:
                self.ball_pos = (self.ball_pos[0], self.ball_pos[1], ball_y_pos - 5)

    def move_ball_to_target(self, source, target): 
        if self.game.is_valid_move(source, target):
            ball = self.game.get_bottles()[source].pop()
            self.game.get_bottles()[target].append(ball)
            y_pos = SCREEN_HEIGHT - 80 - (2 * BALL_RADIUS + 5) * (len(self.game.get_bottles()[target]) - 1)
            self.ball_pos = (target, ball, y_pos)
            self.reset_selected_bottle()
            return True
        else:
            self.reset_selected_bottle()
            return False
        
    def reset_selected_bottle(self): 
        self.ball_pos = None
        self.selected_bottle = None

def main():
    game = FillUpTheBottle(5)
    frontend = FillUpTheBottleFrontend(game)
    running = True

    # Define the "Return" button properties
    return_button_rect = pygame.Rect(50, 600, 200, 50)
    font = pygame.font.SysFont("Array_Games/Memory_Match/Assets/Roboto-Italic.ttf", 36)
    
    while running:
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Draw the "Return" button
        pygame.draw.rect(screen, (75, 0, 130), return_button_rect)  # Red button
        draw_text("Return", font, (255, 255, 255), return_button_rect.centerx, return_button_rect.centery)

        if not game.is_game_complete():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check if the "Return" button was clicked
                    if return_button_rect.collidepoint(mouse_x, mouse_y):
                        running = False  # Exit the game

                    # Handle bottle clicks
                    x_offset = (SCREEN_WIDTH - (len(game.get_bottles()) * (BOTTLE_WIDTH + 50) - 50)) // 2
                    for i, bottle in enumerate(game.get_bottles()): 
                        bottle_rect = pygame.Rect(x_offset + i * (BOTTLE_WIDTH + 50), SCREEN_HEIGHT - BOTTLE_HEIGHT - 50, BOTTLE_WIDTH, BOTTLE_HEIGHT)
                        if bottle_rect.collidepoint(mouse_x, mouse_y):
                            bottle_click_sound.play()
                            if frontend.selected_bottle is None:
                                if bottle:
                                    frontend.selected_bottle = i
                                    ball_color = bottle[-1]
                                    ball_y_pos = SCREEN_HEIGHT - 180 - (2 * BALL_RADIUS + 5) * (len(bottle) - 1)
                                    frontend.ball_pos = (frontend.selected_bottle, ball_color, ball_y_pos)
                            else:
                                target_bottle = i
                                if frontend.move_ball_to_target(frontend.selected_bottle, target_bottle):
                                    ball_move_sound.play()
                                else:
                                    frontend.reset_selected_bottle()
                                    invalid_move_sound.play()
                                break

            frontend.animate_ball_upward()
            frontend.draw_bottles(screen, frontend.selected_bottle)

        if game.is_game_complete():
            screen.blit(win_image, (0, 0))
            pygame.draw.rect(screen, (200, 150, 255), back_button_rect)  # Draw the button
            draw_text("Back", font, (255, 255, 255), back_button_rect.centerx, back_button_rect.centery)

            # Handle win-screen events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):  # Check if the click is within the button
                        running = False

        pygame.display.flip()
        clock.tick(30)


def restart_game():
    # Initialize Pygame
    pygame.init()
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
    restart_game()
