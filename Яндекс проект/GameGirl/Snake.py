import pygame
import sys
import random
import csv
from datetime import datetime
from MainMenu import *

# Настройка параметров игры
WINDOW_SIZE = 800, 600
SNAKE_SIZE = 20
SNAKE_SPEED = 20
APPLE_SIZE = 20
FPS = 15

# Цвета
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0
BLACK = 0, 0, 0
OBSTACLE_COLOR = 128, 128, 128  # Цвет препятствия

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("darkbrown.png").convert()
        self.image = pygame.transform.scale(original_image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = [pygame.Rect(300, 300, SNAKE_SIZE, SNAKE_SIZE)]
        self.snake_dir = (0, 0)
        self.apple = pygame.Rect(400, 300, APPLE_SIZE, APPLE_SIZE)
        self.obstacles = []  # Препятствия
        self.game_active = False
        self.game_over = False
        self.snake_speed = SNAKE_SPEED
        self.score = 0  # Переменная для отслеживания съеденных яблок
        self.obstacle_sprites = pygame.sprite.Group()

        # Генерация рандомных блоков
        self.generate_random_blocks()

    def generate_random_blocks(self):
        num_blocks = random.randint(5, 10)
        for _ in range(num_blocks):
            x = random.randint(50, WINDOW_SIZE[0] - 50)
            y = random.randint(50, WINDOW_SIZE[1] - 50)
            brick = Brick(x, y)
            self.obstacle_sprites.add(brick)

    def draw_obstacles(self):
        self.obstacle_sprites.draw(self.window)

    def save_results(self, game_type):
        # Сохранение результатов в файл results.csv
        with open('results.csv', 'a', newline='') as csvfile:
            fieldnames = ['Game Type', 'Score', 'Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Если файл пустой, записываем заголовок
            if csvfile.tell() == 0:
                writer.writeheader()

            # Записываем результат текущей игры
            writer.writerow({
                'Game Type': game_type.name,  # name возвращает строковое представление Enum
                'Score': self.score,
                'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

    def reset_game(self):
        self.snake = [pygame.Rect(300, 300, SNAKE_SIZE, SNAKE_SIZE)]
        self.snake_dir = (0, 0)
        self.apple = pygame.Rect(400, 300, APPLE_SIZE, APPLE_SIZE)
        self.obstacle_sprites.empty()  # Очищаем группу препятствий
        self.generate_random_blocks()
        self.score = 0
        self.game_over = False

    def draw_snake(self):
        # Отрисовка змейки
        for segment in self.snake:
            pygame.draw.rect(self.window, GREEN, segment)

    def move_snake(self):
        # Перемещение змейки
        head = self.snake[0].move(self.snake_dir)
        if head.colliderect(self.apple):
            # Если голова змейки столкнулась с яблоком
            self.apple.x = random.randint(0, WINDOW_SIZE[0] - APPLE_SIZE)
            self.apple.y = random.randint(0, WINDOW_SIZE[1] - APPLE_SIZE)
            self.snake_speed += 1  # Увеличение скорости после поедания яблока
            self.score += 1  # Увеличение счета
        else:
            self.snake.pop()

        # Проверка на столкновение со стеной или препятствием
        if (head.left < 0 or head.right > WINDOW_SIZE[0] or head.top < 0 or head.bottom > WINDOW_SIZE[1]
                or any(obstacle.rect.colliderect(head) for obstacle in self.obstacle_sprites)):
            self.game_over = True

        # Проверка на столкновение с хвостом
        if head in self.snake[1:]:
            self.game_over = True

        self.snake.insert(0, head)

    def draw_button(self, text, position):
        # Отрисовка кнопки
        font = pygame.font.Font(None, 36)
        button_text = font.render(text, True, WHITE)
        button_rect = pygame.Rect(position[0], position[1], 150, 50)
        pygame.draw.rect(self.window, RED, button_rect)
        self.window.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                                       button_rect.centery - button_text.get_height() // 2))
        return button_rect

    def handle_button_click(self, button_rect):
        # Обработка клика по кнопке
        mouse_pos = pygame.mouse.get_pos()
        click, _, _ = pygame.mouse.get_pressed()
        return button_rect.collidepoint(mouse_pos) and click

    def draw_game_over(self):
        # Отрисовка экрана завершения игры
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, RED)
        self.window.blit(game_over_text, (WINDOW_SIZE[0] // 2 - game_over_text.get_width() // 2,
                                          WINDOW_SIZE[1] // 2 - game_over_text.get_height() // 2))
        restart_button = self.draw_button("Restart", (325, 500))
        exit_button = self.draw_button("Quit", (500, 500))  # Добавлена кнопка "Выйти"
        return restart_button, exit_button

    def draw_score(self):
        # Отрисовка счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        self.window.blit(score_text, (10, 10))

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake_dir = (0, -self.snake_speed)
                    elif event.key == pygame.K_DOWN:
                        self.snake_dir = (0, self.snake_speed)
                    elif event.key == pygame.K_LEFT:
                        self.snake_dir = (-self.snake_speed, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.snake_dir = (self.snake_speed, 0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game_active:
                        button_rect = self.draw_button("Start", (350, 500))
                        if self.handle_button_click(button_rect):
                            self.game_active = True
                    elif self.game_over:
                        restart_button_rect, exit_button_rect = self.draw_game_over()
                        save_button_rect = self.draw_button("Save", (150, 500))  # Добавлено сохранение
                        if self.handle_button_click(restart_button_rect):
                            self.reset_game()
                        elif self.handle_button_click(save_button_rect):
                            # Сохранение результатов при нажатии на кнопку Save
                            self.save_results(GameType.SNAKE)
                        elif self.handle_button_click(exit_button_rect):
                            pygame.quit()
                            sys.exit()

            if self.game_active and not self.game_over:
                self.move_snake()

            self.window.fill(WHITE)
            self.draw_snake()
            self.draw_obstacles()
            pygame.draw.rect(self.window, RED, self.apple)
            self.draw_score()

            if not self.game_active:
                self.draw_button("Start", (325, 500))

            if self.game_over:
                restart_button_rect, exit_button_rect = self.draw_game_over()
                save_button_rect = self.draw_button("Save", (150, 500))  # Добавлено сохранение

            pygame.display.flip()
            self.clock.tick(self.snake_speed)


game = SnakeGame()
game.run_game()