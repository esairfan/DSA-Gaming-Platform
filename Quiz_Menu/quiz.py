import pygame
import sys
import random
from question import ALL_QUESTIONS

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 700
WHITE = (39, 50, 64)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE1 = (255, 255, 255)
# Fonts
FONT = pygame.font.Font("Quiz_Menu/Assets/static/SourGummy_Expanded-Regular.ttf", 20)
BIG_FONT = pygame.font.Font("Quiz_Menu/Assets/static/SourGummy_Expanded-SemiBold.ttf", 48)

# Function to draw text
def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

class QuizGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quiz Game")
        self.clock = pygame.time.Clock()
        self.topic = None
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.selected_option = -1
        self.show_result = False
        self.mouse_down = False  # To handle debounce
        self.num_questions = 3  # Default number of questions

    def start_menu(self):
        """Menu for selecting topic."""
        running = True
        while running:
            self.screen.fill(WHITE)
            draw_text(self.screen, "Select a Topic", BIG_FONT, WHITE1, SCREEN_WIDTH // 2, 200)

            topics = list(ALL_QUESTIONS.keys())
            button_width = 600
            button_height = 50  # Height of each button
            button_spacing = 60  # Spacing between buttons
            total_buttons_height = len(topics) * button_spacing  # Total height required for all buttons
            
            # Calculate the starting position for vertical centering
            start_y = (SCREEN_HEIGHT - total_buttons_height) // 2
            
            for i, topic in enumerate(topics):
                button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, start_y + i * button_spacing, button_width, button_height)  # Center the button horizontally and position it vertically
                pygame.draw.rect(self.screen, WHITE1, button_rect, 2)
                draw_text(self.screen, topic, FONT, WHITE1, button_rect.centerx, button_rect.centery)

                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, RED, button_rect, 2)
                    if pygame.mouse.get_pressed()[0] and not self.mouse_down:
                        self.topic = topic
                        self.get_num_questions()
                        self.questions = random.sample(ALL_QUESTIONS[topic], min(self.num_questions, len(ALL_QUESTIONS[topic])))
                        self.mouse_down = True
                        running = False

            if not pygame.mouse.get_pressed()[0]:
                self.mouse_down = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(60)

    def get_num_questions(self):
        """Prompt the user to input the number of questions."""
        running = True
        input_text = ""
        while running:
            self.screen.fill(WHITE)
            draw_text(self.screen, "Enter number of questions (1-80):", BIG_FONT, WHITE1, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            draw_text(self.screen, input_text, FONT, WHITE1, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isdigit():
                        input_text += event.unicode
                    elif event.key == pygame.K_RETURN:
                        if input_text.isdigit():
                            num = int(input_text)
                            if 1 <= num <= 80:
                                self.num_questions = num
                                running = False

    def display_question(self):
        """Display the current question and options."""
        # Clear the screen
        self.screen.fill(WHITE)
    
        # Display the question text
        question = self.questions[self.current_question_index]
        draw_text(self.screen, f"Q: {question['question']}", FONT, WHITE1, SCREEN_WIDTH // 2, 100)
    
        # Button dimensions and layout settings
        button_height = 50
        padding = 20  # Padding for text inside the button
        vertical_spacing = 10  # Spacing between buttons
    
        # Calculate the maximum button width based on the longest option
        max_text_width = max(FONT.size(option)[0] for option in question['options'])
        button_width = max_text_width + padding * 2
    
        # Calculate the total height of buttons and their starting position
        total_buttons_height = len(question['options']) * (button_height + vertical_spacing)
        start_y = (SCREEN_HEIGHT - total_buttons_height) // 2  # Vertically center the buttons
    
        # Draw each option as a button
        for i, option in enumerate(question['options']):
            button_rect = pygame.Rect(
                (SCREEN_WIDTH - button_width) // 2,
                start_y + i * (button_height + vertical_spacing),
                button_width,
                button_height,
            )
    
            # Determine button color based on result visibility
            if self.show_result:
                if i + 1 == question['answer']:
                    color = GREEN  # Correct answer
                elif i + 1 == self.selected_option:
                    color = RED  # Wrong selection
                else:
                    color = WHITE1  # Default button color
            else:
                color = WHITE1  # Default button color when no result is shown
    
            # Draw the button and its text
            pygame.draw.rect(self.screen, color, button_rect, 2)
            draw_text(self.screen, option, FONT, WHITE1, button_rect.centerx, button_rect.centery)
    
            # Handle button hover and click interaction
            if button_rect.collidepoint(pygame.mouse.get_pos()) and not self.show_result:
                pygame.draw.rect(self.screen, RED, button_rect, 2)  # Highlight button on hover
                if pygame.mouse.get_pressed()[0] and not self.mouse_down:
                    self.selected_option = i + 1
                    self.check_answer()
                    self.mouse_down = True
    
        # Reset mouse state when the mouse button is released
        if not pygame.mouse.get_pressed()[0]:
            self.mouse_down = False
    
        # Display the "Next" button if the result is being shown
        if self.show_result:
            next_button_width = 200
            next_button_height = 50
            next_button = pygame.Rect(
                (SCREEN_WIDTH - next_button_width) // 2,
                SCREEN_HEIGHT - 100,
                next_button_width,
                next_button_height,
            )
            pygame.draw.rect(self.screen, WHITE1, next_button, 2)
            draw_text(self.screen, "Next", FONT, WHITE1, next_button.centerx, next_button.centery)
    
            # Handle interaction with the "Next" button
            if next_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.mouse_down:
                self.next_question()
                self.mouse_down = True
    
        # Update the screen
        pygame.display.flip()


    def check_answer(self):
        question = self.questions[self.current_question_index]
        if self.selected_option == question['answer']:
            self.score += 1
        self.show_result = True

    def next_question(self):
        self.current_question_index += 1
        self.selected_option = -1
        self.show_result = False

        if self.current_question_index >= len(self.questions):
            self.show_final_score()
        else:
            self.display_question()

    def show_final_score(self):
        self.screen.fill(WHITE)
        draw_text(self.screen, f"Quiz Completed! Your score: {self.score}/{len(self.questions)}", BIG_FONT, WHITE1, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(self.screen, "Press R to Retry or Q to Quit", FONT, WHITE1, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def reset_game(self):
        self.topic = None
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.selected_option = -1
        self.show_result = False
        self.start_menu()

    def run(self):
        self.start_menu()
        running = True
        while running:
            self.display_question()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = QuizGame()
    game.run()
