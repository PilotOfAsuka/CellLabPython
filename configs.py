
import pygame
import math
# Установка размеров окна
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Bot Simulation')
gui_offset = 200  # Отступ справа от края для интерфейса

# Мир теперь состоит из клеточек
CELL_SIZE = 4  # Размер клетки изменяя этот параметр меняется масштаб
GRID_SIZE_W = (width - gui_offset) // CELL_SIZE  # Задаем ширину сетки мира (-200 Это отступ для интерфейса)
GRID_SIZE_H = height // CELL_SIZE  # Задаем высоту сетки мира
START_NUM_OF_CELL = 1000  # Стартовое число клеток при создании мира
gen_size = 64  # Размер гена


world_size = math.sqrt(height**2 + (width - gui_offset)**2)
# Кортеж направлений
move_directions = (
    (0, -1),  # Вверх 0
    (1, -1),   # Вверх и вправо 1
    (1, 0),  # Вправо 2
    (1, 1),  # Вправо и вниз 3
    (0, 1),  # Вниз 4
    (-1, 1),  # Вниз и лево 5
    (-1, 0),  # Влево 6
    (-1, -1)  # Влево и вверх 7
)


class Camera:
    def __init__(self):
        self.cam = pygame.Rect(0, 0, width-200, height)
        self.scale = 1

        self.x_offset = 0
        self.y_offset = 0
        self.min_offset = 0

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        # Обновление камеры
        if self.scale == 1:
            self.y_offset = 0
            self.x_offset = 0

        if self.scale == 2:
            self.min_offset = -100
        elif self.scale == 3:
            self.min_offset = -133

        if self.scale == 2 and self.y_offset < -100:
            self.y_offset = -100

        if self.scale == 2 and self.x_offset < -100:
            self.x_offset = -100
        self.update_position()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.scale = self.scale + 1 if -1 < self.scale + 1 < 4 else self.scale
            elif event.key == pygame.K_MINUS:
                self.scale = self.scale - 1 if 0 < self.scale - 1 < 4 else self.scale

            elif event.key == pygame.K_LEFT:
                self.moving_left = True
                pass
            elif event.key == pygame.K_UP:
                self.moving_up = True
                pass
            elif event.key == pygame.K_RIGHT:
                self.moving_right = True
                pass
            elif event.key == pygame.K_DOWN:
                self.moving_down = True
                pass
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving_left = False
                pass
            elif event.key == pygame.K_UP:
                self.moving_up = False
                pass
            elif event.key == pygame.K_RIGHT:
                self.moving_right = False
                pass
            elif event.key == pygame.K_DOWN:
                self.moving_down = False
                pass

    def update_position(self):
        if self.moving_left is True:
            self.x_offset = self.x_offset + 1 if self.min_offset < self.x_offset + 1 < 1 else self.x_offset

        if self.moving_right is True:
            self.x_offset = self.x_offset - 1 if self.min_offset < self.x_offset - 1 < 1 else self.x_offset

        if self.moving_up is True:
            self.y_offset = self.y_offset + 1 if self.min_offset < self.y_offset + 1 < 1 else self.y_offset
            pass
        if self.moving_down is True:
            self.y_offset = self.y_offset - 1 if self.min_offset < self.y_offset - 1 < 1 else self.y_offset
            pass
