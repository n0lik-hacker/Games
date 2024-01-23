import pygame
import random
import csv
from datetime import datetime

# Инициализация Pygame
pygame.init()

# Определение размеров окна
window_width = 400
window_height = 400

# Определение цветов
white = (255, 255, 255)
black = (0, 0, 0)
score = 0

# Определение размеров игровой доски
board_size = 2
tile_size = window_width // board_size


# Создание окна
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("FIFTEEN_PUZZLE")

# Определение размеров кнопок в меню окончания
button_width = 200
button_height = 50

# Определение прямоугольников для кнопок в меню окончания
save_button_rect = pygame.Rect(window_width // 2 - button_width // 2, window_height // 2 - button_height // 2,
                               button_width, button_height)
restart_button_rect = pygame.Rect(window_width // 2 - button_width // 2, window_height // 2 + button_height,
                                  button_width, button_height)


def save_game_info(game_type, score):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('results.csv', 'a', newline='') as csvfile:
        fieldnames = ['Game Type', 'Score', 'Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Если файл пустой, записываем заголовки
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({'Game Type': game_type, 'Score': score, 'Date': date})


# Функция для отрисовки текста на экране
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)


# Функция для отрисовки игровой доски
def draw_board(board):
    for row in range(board_size):
        for col in range(board_size):
            tile = board[row][col]
            if tile != 0:
                x = col * tile_size
                y = row * tile_size
                pygame.draw.rect(window, white, (x, y, tile_size, tile_size))
                draw_text(str(tile), pygame.font.Font(None, 50), black, x + tile_size // 2, y + tile_size // 2)


# Функция для перемещения плиток
def move_tile(board, row, col, clicked_row, clicked_col):
    if abs(row - clicked_row) <= 1 and abs(col - clicked_col) <= 1:
        board[row][col], board[clicked_row][clicked_col] = board[clicked_row][clicked_col], board[row][col]


def is_winner(board):
    global score
    win_board = [[j for j in range(board_size * i + 1, board_size * (i + 1) + 1)] for i in range(board_size)]
    win_board[board_size - 1][board_size - 1] = 0
    if board == win_board:
        score += 1
        return True
    else:
        return False


# Функция для проверки, является ли доска решаемой
def is_solvable(board):
    flat_board = [tile for row in board for tile in row if tile != 0]

    inversions = sum(
        1 for i in range(len(flat_board)) for j in range(i + 1, len(flat_board)) if flat_board[i] > flat_board[j])
    blank_row = board_size - (len(flat_board) // board_size)

    if board_size % 2 == 1:  # Для досок нечетного размера
        return inversions % 2 == 0
    else:  # Для досок четного размера
        return (inversions + blank_row) % 2 == 1


# Функция для перемешивания плиток на игровой доске
def shuffle_board(board):
    while True:
        shuffled_board = [[row * board_size + col for col in range(board_size)] for row in range(board_size)]
        random.shuffle(shuffled_board)
        if is_solvable(shuffled_board):
            return shuffled_board


# Создание начальной игровой доски
board = [[row * board_size + col for col in range(board_size)] for row in range(board_size)]
board[board_size - 1][board_size - 1] = 0

board = shuffle_board(board)



# Определение кнопок для главного меню
new_game_button_rect = pygame.Rect(window_width // 2 - 100, window_height // 2 - 30, 200, 60)
exit_button_rect = pygame.Rect(window_width // 2 - 100, window_height // 2 + 50, 200, 60)


# Основной игровой цикл
def run():
    global board
    running = True
    selected_row = None
    selected_col = None

    # Определение состояний игры
    MAIN_MENU = 0
    PLAYING = 1
    END_MENU = 2
    WINNER_SCREEN = 3
    EXIT = 4

    # Изначальное состояние - главное меню
    game_state = MAIN_MENU
    while True:
       global SAVE_OPTION, RESTART_OPTION
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               quit()
           elif event.type == pygame.MOUSEBUTTONDOWN:
               mouse_pos = pygame.mouse.get_pos()

           if game_state == MAIN_MENU:
               # Обработка событий для кнопок в главном меню
               if game_state == MAIN_MENU:
                   # Отрисовка главного меню
                   window.fill(black)
                   draw_text("Главное меню", pygame.font.Font(None, 36), white, window_width // 2, 50)

                   # Отрисовка кнопки "1 - Новая игра"
                   pygame.draw.rect(window, white, new_game_button_rect)
                   draw_text("1 - Новая игра", pygame.font.Font(None, 30), black,
                             new_game_button_rect.centerx, new_game_button_rect.centery)

                   # Отрисовка кнопки "2 - Выход"
                   pygame.draw.rect(window, white, exit_button_rect)
                   draw_text("2 - Выход", pygame.font.Font(None, 30), black,
                             exit_button_rect.centerx, exit_button_rect.centery)

                   pygame.display.update()

                   # Обработка событий для кнопок
                   mouse_pos = pygame.mouse.get_pos()
                   mouse_click = pygame.mouse.get_pressed()

                   # Нажатие кнопки "1 - Новая игра"
                   if new_game_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                       game_state = PLAYING
                       break


                   # Нажатие кнопки "2 - Выход"
                   elif exit_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                       game_state = EXIT

               elif game_state == PLAYING:
                   if event.type == pygame.MOUSEBUTTONDOWN:
                       mouse_pos = pygame.mouse.get_pos()
                       clicked_row = mouse_pos[1] // tile_size
                       clicked_col = mouse_pos[0] // tile_size

                   # Очистка экрана
                   window.fill(black)

                   # Отрисовка игровой доски
                   draw_board(board)

                   # Обновление экрана
                   pygame.display.update()

               elif game_state == EXIT:
                   pygame.quit()
                   quit()

           elif game_state == PLAYING:
               if event.type == pygame.MOUSEBUTTONDOWN:
                   mouse_pos = pygame.mouse.get_pos()
                   clicked_row = mouse_pos[1] // tile_size
                   clicked_col = mouse_pos[0] // tile_size

                   # Если пользователь нажал на плитку, установите ее в качестве выбранной
                   if board[clicked_row][clicked_col] != 0:
                       selected_row, selected_col = clicked_row, clicked_col
                   elif selected_row is not None and selected_col is not None:
                       # Если есть выбранная плитка и пользователь нажал на пустую клетку, переместите плитку
                       move_tile(board, selected_row, selected_col, clicked_row, clicked_col)
                       selected_row, selected_col = None, None
                   # Очистка экрана
                   window.fill(black)

               # Отрисовка игровой доски
               draw_board(board)

               # Отрисовка выделения выбранной плитки (если есть)
               if selected_row is not None and selected_col is not None:
                   x = selected_col * tile_size
                   y = selected_row * tile_size
                   pygame.draw.rect(window, (255, 0, 0), (x, y, tile_size, tile_size), 3)

               # Обновление экрана
               pygame.display.update()

               # Очистка экрана
               window.fill(black)

               # Отрисовка игровой доски
               draw_board(board)

               # Обновление экрана
               pygame.display.update()
               if is_winner(board):
                   game_state = END_MENU
                   window.fill(black)
                   break
           elif game_state == END_MENU:
               # Отрисовка экрана окончания
               window.fill(black)
               draw_text("Поздравляю, ты выиграл!", pygame.font.Font(None, 36), white, window_width // 2, 50)

               # Отрисовка кнопки "3 - Сохранить"
               pygame.draw.rect(window, white, save_button_rect)
               draw_text("3 - Сохранить", pygame.font.Font(None, 30), black,
                         save_button_rect.centerx, save_button_rect.centery)

               # Отрисовка кнопки "4 - Начать заново"
               pygame.draw.rect(window, white, restart_button_rect)
               draw_text("4 - Начать заново", pygame.font.Font(None, 30), black,
                         restart_button_rect.centerx, restart_button_rect.centery)

               pygame.display.update()

               # Обработка событий для кнопок
               mouse_pos = pygame.mouse.get_pos()
               mouse_click = pygame.mouse.get_pressed()

               # Нажатие кнопки " - Сохранить"
               if save_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                   # Добавьте код для сохранения текущего состояния игры
                   print("Игра сохранена")
                   save_game_info("FIFTEEN_PUZZLE", score)

               # Нажатие кнопки " - Начать заново"
               elif restart_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                   game_state = PLAYING
                   board = shuffle_board(board)

       # Обновление экрана
       pygame.display.update()

    pygame.quit()
run()
# Выход из игры
