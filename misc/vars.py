
# Установка размеров окна и его параметров
RES = width, height = 800, 800
FPS = 120

# Мир состоит из клеточек
CELL_SIZE = 1  # Размер клетки изменяя этот параметр меняется масштаб
GRID_SIZE_W = width // CELL_SIZE  # Задаем ширину сетки мира
GRID_SIZE_H = height // CELL_SIZE  # Задаем высоту сетки мира
START_NUM_OF_CELL = 1000  # Стартовое число клеток при создании мира
gen_size = 64  # Размер гена

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

food_values = {
    'cell_thinks': {'min': 40, 'max': 30},  # Зависит от температуры
    'photosynthesis': {'min': 55, 'max': 55},  # Зависит от расстояния до солнца
    'predator_thinks': {'min':  10, 'max': 5},  # Зависит от температуры
    'predator_move': {'min': 5, 'max': 1},  # Зависит от температуры
}


# Глобальные переменные
global_vars = {"count_of_cycle": 0, "count_of_food": 0, "count_of_cells": 0, "temp": 0, "count_of_predators": 0}

# Инициализация двумерного массива мира
world_grid = [[None for _ in range(GRID_SIZE_W)] for _ in range(GRID_SIZE_H)]  # Мир в котором живут клетки

to_draw_obj = []