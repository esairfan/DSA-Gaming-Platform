import pygame
from logic import WordSearchLogic
from frontend import WordSearchUI

def main():
    pygame.init()
    grid_size = 10
    word_list = ["PYTHON", "GAME", "SEARCH", "WORD", "ALGORITHM"]
    
    logic = WordSearchLogic(grid_size, word_list)
    logic.place_words()
    logic.fill_random_letters()

    screen = pygame.display.set_mode((grid_size * 40 + 200, grid_size * 40))
    pygame.display.set_caption("Word Search")
    ui = WordSearchUI(screen, logic.get_grid(), word_list)

    running = True
    selecting = False
    selected_sequence = []
    selected_cells = []

    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cell = ui.get_cell_at_position(pygame.mouse.get_pos())
                if cell:
                    selecting = True
                    ui.selected_cells = [cell]
                    selected_cells = [cell]
                    selected_sequence = [ui.grid[cell[0]][cell[1]]]
            elif event.type == pygame.MOUSEMOTION:
                if selecting:
                    cell = ui.get_cell_at_position(pygame.mouse.get_pos())
                    if cell and cell not in ui.selected_cells:
                        ui.selected_cells.append(cell)
                        selected_cells.append(cell)
                        selected_sequence.append(ui.grid[cell[0]][cell[1]])
            elif event.type == pygame.MOUSEBUTTONUP:
                if selecting:
                    selecting = False
                    selected_word = "".join(selected_sequence)
                    if logic.is_valid_word(selected_sequence):
                        print(f"Word Found: {selected_word}")
                        ui.mark_found_word(selected_word, selected_cells)  # Highlight and remove
                    else:
                        print(f"Invalid Word: {selected_word}")
                    ui.selected_cells = []

        ui.draw_grid()
        ui.draw_word_list()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
