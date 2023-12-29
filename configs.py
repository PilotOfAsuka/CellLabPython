
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
    def __init__(self, wd, hd):
        self.cam = pygame.Rect(0, 0, width-200, height)
        self.scale = 1
        self.wd = wd
        self.hd = hd
        self.x_offset = 0
        self.y_offset = 0

    def update(self):
        # Обновление камеры
        self.cam.width = int((width-200) * self.scale)
        self.cam.height = int(height * self.scale)

        # Ограничение масштаба
        if self.cam.width < self.wd - 200:
            self.cam.width = self.wd - 200
        if self.cam.height < self.hd:
            self.cam.height = self.hd

    def handle_event(self, event):
        event = event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.scale = self.scale + 1 if -1 < self.scale + 1 < 4 else self.scale
                print(self.scale)
            elif event.key == pygame.K_MINUS:
                self.scale = self.scale - 1 if 0 < self.scale - 1 < 4 else self.scale
                print(self.scale)

            elif event.key == pygame.K_LEFT:
                self.x_offset = self.x_offset + CELL_SIZE if 0 < self.x_offset < (GRID_SIZE_W//self.scale) else self.x_offset
                pass
            elif event.key == pygame.K_UP:
                self.y_offset = self.y_offset + CELL_SIZE if 0 < self.y_offset < (GRID_SIZE_H//self.scale) else self.y_offset
                pass
            elif event.key == pygame.K_RIGHT:
                self.x_offset = self.x_offset - CELL_SIZE if 0 < self.x_offset < (GRID_SIZE_W//self.scale) else self.x_offset
                pass
            elif event.key == pygame.K_DOWN:
                self.y_offset = self.y_offset - CELL_SIZE if 0 < self.x_offset < (GRID_SIZE_H//self.scale) else self.y_offset
                pass
