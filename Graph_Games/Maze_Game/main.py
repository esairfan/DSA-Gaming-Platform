# main.py
import pygame, sys
from maze import Maze
from player import Player
from game import Game
from clock import Clock

pygame.init()
pygame.font.init()
class Button:
    def __init__(self, x, y, width, height, text, bg_color, text_color, 
                 border_radius=0, border_color=None, border_width=0, font_path=None, font_size=36):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_width = border_width
        # Load custom font or use default
        self.font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.Font(None, font_size)
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, screen):
        # Draw the border if needed
        if self.border_width > 0 and self.border_color:
            pygame.draw.rect(
                screen, 
                self.border_color, 
                self.rect, 
                border_radius=self.border_radius, 
                width=self.border_width
            )
        # Draw the button background
        pygame.draw.rect(
            screen, 
            self.bg_color, 
            self.rect, 
            border_radius=self.border_radius
        )
        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.is_hovered(pos)



class Main():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 30)
        self.message_color = pygame.Color("cyan")
        self.running = True
        self.game_over = False
        self.FPS = pygame.time.Clock()
    
    def instructions(self):
        instructions1 = self.font.render('Use', True, self.message_color)
        instructions2 = self.font.render('Arrow Keys', True, self.message_color)
        instructions3 = self.font.render('to Move', True, self.message_color)
        self.screen.blit(instructions1,(1250,300))
        self.screen.blit(instructions2,(1205,331))
        self.screen.blit(instructions3,(1220,362))
        
        # draws all configs; maze, player, instructions, and time
    def _draw(self, maze, tile, player, game, clock):
        # draw maze
        [cell.draw(self.screen, tile) for cell in maze.grid_cells]
        # add a goal point to reach
        game.add_goal_point(self.screen)
        # draw every player movement
        player.draw(self.screen)
        player.update()
        # instructions, clock, winning message
        self.instructions()
        if self.game_over:
            clock.stop_timer()
            self.screen.blit(game.message(),(1225,120))
        else:
            clock.update_timer()
        self.screen.blit(clock.display_timer(), (1225,200))
        
        pygame.display.flip()    # draws all configs; maze, player, instructions, and time
    def _draw(self, maze, tile, player, game, clock, back_button):
        # draw maze
        [cell.draw(self.screen, tile) for cell in maze.grid_cells]
        # add a goal point to reach
        game.add_goal_point(self.screen)
        # draw every player movement
        player.draw(self.screen)
        player.update()
        # instructions, clock, winning message
        self.instructions()
        if self.game_over:
            clock.stop_timer()
            self.screen.blit(game.message(),(610,120))
        else:
            clock.update_timer()
        self.screen.blit(clock.display_timer(), (1225,200))
        back_button.draw(screen)
        pygame.display.flip()
        
    def main(self, frame_size, tile):
        BUTTONTEXTCOLOR=(255, 255, 255)
        back_button = Button(1225, 600, 100, 60, 'Back', (0, 0, 0, 0), BUTTONTEXTCOLOR,6)
        cols, rows = frame_size[0] // tile, frame_size[-1] // tile
        maze = Maze(cols, rows)
        game = Game(maze.grid_cells[-1], tile)
        player = Player(tile // 3, tile // 3)
        clock = Clock()
        maze.generate_maze()
        clock.start_timer()
        while self.running:
            self.screen.fill("gray")
            self.screen.fill( pygame.Color("darkslategray"), (1200, 0, self.screen.get_width() - 1200 , self.screen.get_height()))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if back_button.is_clicked(mouse_pos):
                            print("Start Game button clicked")
                            self.running=False

            # if keys were pressed still
            if event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_LEFT:
                        player.left_pressed = True
                    if event.key == pygame.K_RIGHT:
                        player.right_pressed = True
                    if event.key == pygame.K_UP:
                        player.up_pressed = True
                    if event.key == pygame.K_DOWN:
                        player.down_pressed = True
                    player.check_move(tile, maze.grid_cells, maze.thickness)
            # if pressed key released
            if event.type == pygame.KEYUP:
                if not self.game_over:
                    if event.key == pygame.K_LEFT:
                        player.left_pressed = False
                    if event.key == pygame.K_RIGHT:
                        player.right_pressed = False
                    if event.key == pygame.K_UP:
                        player.up_pressed = False
                    if event.key == pygame.K_DOWN:
                        player.down_pressed = False
                    player.check_move(tile, maze.grid_cells, maze.thickness)
            if game.is_game_over(player):
                self.game_over = True
                player.left_pressed = False
                player.right_pressed = False
                player.up_pressed = False
                player.down_pressed = False
            self._draw(maze, tile, player, game, clock, back_button)
            
            self.FPS.tick(60)
            
# main.py

if __name__ == "__main__":
    window_size = (1200, 800)
    screen = (window_size[0] + 150, window_size[-1])
    tile_size = 30
    screen = pygame.display.set_mode(screen)
    pygame.display.set_caption("Maze")

    game = Main(screen)
    game.main(window_size, tile_size)