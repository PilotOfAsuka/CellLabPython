
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
