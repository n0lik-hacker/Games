import pygame
import sys
from enum import Enum

# Определение игр
class GameType(Enum):
    SNAKE = 1
    FIFTEEN_PUZZLE = 2
    MAIN_MENU = 3

class GameSelection:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Game Selection")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.selection_active = True
        self.selected_game = None

    def draw_buttons(self):
        # Отрисовка кнопок выбора игр
        snake_button = self.draw_button("Snake", (125, 85))
        fifteen_puzzle_button = self.draw_button("15 Puzzle", (125, 180))
        return snake_button, fifteen_puzzle_button

    def draw_button(self, text, position):
        # Отрисовка кнопки
        button_text = self.font.render(text, True, (255, 255, 255))
        button_rect = pygame.Rect(position[0], position[1], 150, 50)
        pygame.draw.rect(self.window, (255, 0, 0), button_rect)
        self.window.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                                       button_rect.centery - button_text.get_height() // 2))
        return button_rect

    def handle_button_click(self, button_rect):
        # Обработка клика по кнопке
        mouse_pos = pygame.mouse.get_pos()
        click, _, _ = pygame.mouse.get_pressed()
        return button_rect.collidepoint(mouse_pos) and click

    def run_selection(self):
        while self.selection_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    snake_button, fifteen_puzzle_button = self.draw_buttons()
                    if self.handle_button_click(snake_button):
                        self.selection_active = False
                        self.selected_game = GameType.SNAKE
                    elif self.handle_button_click(fifteen_puzzle_button):
                        self.selection_active = False
                        self.selected_game = GameType.FIFTEEN_PUZZLE

            snake_button, fifteen_puzzle_button = self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(15)

        return self.selected_game

def main_menu():
    game_selection = GameSelection()
    selected_game = game_selection.run_selection()

    if selected_game == GameType.SNAKE:
        from Snake import SnakeGame  # Импорт SnakeGame только если выбрана змейка
        snake_game = SnakeGame()
        snake_game.run_game()
    elif selected_game == GameType.FIFTEEN_PUZZLE:
        from Tag import run
        run()
    # Добавленный блок для возврата в главное меню
    elif selected_game == GameType.MAIN_MENU:
        pygame.quit()
        main_menu()


if __name__ == "__main__":
    main_menu()