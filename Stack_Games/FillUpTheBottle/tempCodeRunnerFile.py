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


# Load images
background_image = pygame.image.load("Stack_Games/FillUpTheBottle/Assets/bg2.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Hydro Hustle")
clock = pygame.time.Clock()


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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                x_offset = (SCREEN_WIDTH - (len(game.get_bottles()) * (BOTTLE_WIDTH + 50) - 50)) // 2
                for i, bottle in enumerate(game.get_bottles()): 
                    bottle_rect = pygame.Rect(x_offset + i * (BOTTLE_WIDTH + 50), SCREEN_HEIGHT - BOTTLE_HEIGHT - 50, BOTTLE_WIDTH, BOTTLE_HEIGHT)

                    if bottle_rect.collidepoint(mouse_x, mouse_y):
                        if frontend.selected_bottle is None:
                            if bottle:
                                frontend.selected_bottle = i
                                ball_color = bottle[-1]
                                ball_y_pos = SCREEN_HEIGHT - 180 - (2 * BALL_RADIUS + 5) * (len(bottle) - 1)
                                frontend.ball_pos = (frontend.selected_bottle, ball_color, ball_y_pos)
                        else:
                            target_bottle = i
                            if frontend.move_ball_to_target(frontend.selected_bottle, target_bottle):
                                pass
                            else:
                                frontend.reset_selected_bottle()
                            break
 
        frontend.animate_ball_upward()
 
        frontend.draw_bottles(screen, frontend.selected_bottle)
 
        screen.blit(background_image, (0, 0))
 
        if game.is_game_complete():
            print("You Win! Total Moves:", game.moves) 

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
