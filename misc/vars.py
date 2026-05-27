
# Установка размеров окна и его параметров.
RES = width, height = 1200, 800
gui_offset = 400  # Отступ справа от края для интерфейса
FPS = 60

# Мир состоит из клеточек. CELL_SIZE читается при старте и задает размер сетки.
CELL_SIZE = 3  # Размер клетки изменяя этот параметр меняется масштаб
GRID_SIZE_W = (width - gui_offset) // CELL_SIZE  # Задаем ширину сетки мира (-200 Это отступ для интерфейса)
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

# Глобальные переменные - простой общий словарь для симуляции и GUI.
global_vars = {
    "count_of_cycle": 0,
    "count_of_food": 0,
    "count_of_cells": 0,
    "temp": 0,
    "simulation_ms": 0,
    "draw_ms": 0,
    "drawn_objects": 0,
    "temp_running": True,
    "cell_size_setting": CELL_SIZE,
    "genome_size_setting": gen_size,
    "start_cells_setting": START_NUM_OF_CELL,
}

# Инициализация двумерного массива мира.
world_grid = [[None for _ in range(GRID_SIZE_W)] for _ in range(GRID_SIZE_H)]  # Мир в котором живут клетки
active_objects = []


def register_object(obj):
    active_objects.append(obj)


def prune_active_objects():
    alive_objects = []
    seen_objects = set()

    for obj in active_objects:
        x, y = obj.position
        obj_id = id(obj)
        if obj_id in seen_objects:
            continue
        if 0 <= x < GRID_SIZE_W and 0 <= y < GRID_SIZE_H and world_grid[y][x] is obj:
            alive_objects.append(obj)
            seen_objects.add(obj_id)

    active_objects[:] = alive_objects


def apply_world_settings(cell_size=None, genome_size=None, start_cells=None):
    global CELL_SIZE, GRID_SIZE_W, GRID_SIZE_H, START_NUM_OF_CELL, gen_size

    if cell_size is not None:
        CELL_SIZE = max(1, int(cell_size))
    if genome_size is not None:
        gen_size = max(8, int(genome_size))
    if start_cells is not None:
        START_NUM_OF_CELL = max(1, int(start_cells))

    GRID_SIZE_W = (width - gui_offset) // CELL_SIZE
    GRID_SIZE_H = height // CELL_SIZE
    max_cells = GRID_SIZE_W * GRID_SIZE_H
    START_NUM_OF_CELL = min(START_NUM_OF_CELL, max_cells)
    world_grid[:] = [[None for _ in range(GRID_SIZE_W)] for _ in range(GRID_SIZE_H)]
    active_objects.clear()

    global_vars["cell_size_setting"] = CELL_SIZE
    global_vars["genome_size_setting"] = gen_size
    global_vars["start_cells_setting"] = START_NUM_OF_CELL


def reset_world_counters():
    global_vars["count_of_cycle"] = 0
    global_vars["count_of_food"] = 0
    global_vars["count_of_cells"] = 0
    global_vars["simulation_ms"] = 0
    global_vars["draw_ms"] = 0
    global_vars["drawn_objects"] = 0
