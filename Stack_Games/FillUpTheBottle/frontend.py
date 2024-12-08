import pygame
from logic import FillUpTheBottle

# Constants for screen and bottle sizes
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BOTTLE_WIDTH, BOTTLE_HEIGHT = 80, 200
BALL_RADIUS = 20
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
]

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fill Up The Bottle Animation")
clock = pygame.time.Clock()


class FillUpTheBottleFrontend:
    def __init__(self, game):
        self.game = game
        self.ball_pos = None  # Stores (bottle_index, ball_color, ball_y_pos)
        self.selected_bottle = None

    def draw_bottles(self, screen, selected_bottle=None):
        screen.fill((255, 255, 255))
        x_offset = 50
        y_base = SCREEN_HEIGHT - 50

        for i, bottle in enumerate(self.game.get_bottles()):
            bottle_top = y_base - BOTTLE_HEIGHT
            bottle_rect = pygame.Rect(x_offset, bottle_top, BOTTLE_WIDTH, BOTTLE_HEIGHT)

            pygame.draw.line(screen, (0, 0, 0), (x_offset, bottle_top), (x_offset, y_base), 2)
            pygame.draw.line(screen, (0, 0, 0), (x_offset + BOTTLE_WIDTH, bottle_top), (x_offset + BOTTLE_WIDTH, y_base), 2)

            pygame.draw.arc(
                screen,
                (0, 0, 0),
                (x_offset, bottle_top + 150, BOTTLE_WIDTH, BOTTLE_WIDTH),
                3.14,
                6.28,
                2,
            )

            # Draw balls inside the bottle
            y_ball = y_base - BALL_RADIUS - 10
            for ball_idx, ball in enumerate(bottle):
                if self.ball_pos and i == self.ball_pos[0] and ball_idx == len(bottle) - 1:
                    # Skip drawing the ball currently in motion
                    continue
                color = COLORS[ball - 1]  # Get the color for the ball
                pygame.draw.circle(
                    screen, color, (x_offset + BOTTLE_WIDTH // 2, y_ball + 30), BALL_RADIUS
                )
                y_ball -= 2 * BALL_RADIUS + 5

            # Draw the moving ball if any
            if self.ball_pos and i == self.ball_pos[0]:
                ball_color = COLORS[self.ball_pos[1] - 1]
                pygame.draw.circle(screen, ball_color, (x_offset + BOTTLE_WIDTH // 2, self.ball_pos[2]), BALL_RADIUS)

            x_offset += BOTTLE_WIDTH + 30

        pygame.display.flip()

    def animate_ball_upward(self):
        if self.ball_pos:
            ball_y_pos = self.ball_pos[2]
            if ball_y_pos > SCREEN_HEIGHT - 300:  # Animate upward from the ball's current y position
                self.ball_pos = (self.ball_pos[0], self.ball_pos[1], ball_y_pos - 5)

    def reset_selected_bottle(self):
        """Reset the selected bottle and make the ball visible again."""
        self.ball_pos = None
        self.selected_bottle = None

    def move_ball_to_target(self, source, target):
        if self.game.is_valid_move(source, target):
            ball = self.game.get_bottles()[source].pop()
            self.game.get_bottles()[target].append(ball)
            self.reset_selected_bottle()
            return True
        else:
            # Invalid move, reset the selected bottle
            self.reset_selected_bottle()
            return False


def main():
    game = FillUpTheBottle(5)
    frontend = FillUpTheBottleFrontend(game)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                x_offset = 50
                for i, bottle in enumerate(game.get_bottles()):
                    bottle_rect = pygame.Rect(x_offset, SCREEN_HEIGHT - BOTTLE_HEIGHT - 50, BOTTLE_WIDTH, BOTTLE_HEIGHT)
                    if bottle_rect.collidepoint(mouse_x, mouse_y):
                        if frontend.selected_bottle is None:
                            if bottle:
                                frontend.selected_bottle = i
                                ball_color = bottle[-1]
                                ball_y_pos = SCREEN_HEIGHT - 80 - (2 * BALL_RADIUS + 5) * (len(bottle) - 1)
                                frontend.ball_pos = (frontend.selected_bottle, ball_color, ball_y_pos)
                        else:
                            target_bottle = i
                            if frontend.move_ball_to_target(frontend.selected_bottle, target_bottle):
                                pass
                            else:
                                frontend.reset_selected_bottle()
                            break
                    x_offset += BOTTLE_WIDTH + 30

        frontend.animate_ball_upward()
        frontend.draw_bottles(screen, frontend.selected_bottle)

        if game.is_game_complete():
            print("You Win! Total Moves:", game.moves)
            running = False

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
