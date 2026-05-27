
# Установка размеров окна и его параметров.
RES = width, height = 1200, 800
gui_offset = 400  # Отступ справа от края для интерфейса
FPS = 60

# Мир состоит из клеточек. CELL_SIZE читается при старте и задает размер сетки.
CELL_SIZE = 5  # Размер клетки изменяя этот параметр меняется масштаб
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
bot_grid = bytearray(GRID_SIZE_W * GRID_SIZE_H)
neighbor_grid = bytearray(GRID_SIZE_W * GRID_SIZE_H)
active_objects = []
active_bots = []
active_food = []
photosynthesis_by_y = []
light_height_by_y = []
current_daylight = 0.65
cell_think_cost = 50
predator_think_cost = 50
predator_move_cost = 10
temp_ptr_step = 15
food_check_temp_offset = 2


def register_object(obj):
    active_objects.append(obj)
    if obj.__class__.__name__ == "Food":
        active_food.append(obj)
    else:
        active_bots.append(obj)


def grid_index(x, y):
    return y * GRID_SIZE_W + x


def set_bot_position(x, y, is_bot=True):
    index = grid_index(x, y)
    new_value = 1 if is_bot else 0
    if bot_grid[index] == new_value:
        return

    bot_grid[index] = new_value
    delta = 1 if is_bot else -1
    start_x = max(0, x - 1)
    end_x = min(GRID_SIZE_W, x + 2)
    start_y = max(0, y - 1)
    end_y = min(GRID_SIZE_H, y + 2)

    for ny in range(start_y, end_y):
        row_index = ny * GRID_SIZE_W
        for nx in range(start_x, end_x):
            if nx == x and ny == y:
                continue
            neighbor_grid[row_index + nx] += delta


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
    bot_grid[:] = bytearray(max_cells)
    neighbor_grid[:] = bytearray(max_cells)
    active_objects.clear()
    active_bots.clear()
    active_food.clear()

    global_vars["cell_size_setting"] = CELL_SIZE
    global_vars["genome_size_setting"] = gen_size
    global_vars["start_cells_setting"] = START_NUM_OF_CELL
    rebuild_math_caches()


def reset_world_counters():
    global_vars["count_of_cycle"] = 0
    global_vars["count_of_food"] = 0
    global_vars["count_of_cells"] = 0
    global_vars["simulation_ms"] = 0
    global_vars["draw_ms"] = 0
    global_vars["drawn_objects"] = 0


def normalize_int(input_value, original_min, original_max, target_min, target_max):
    return int(
        (input_value - original_min) / (original_max - original_min) * (target_max - target_min) + target_min
    )


def rebuild_math_caches():
    global photosynthesis_by_y, light_height_by_y

    photosynthesis_by_y = [
        normalize_int(y, 0, GRID_SIZE_H, 100, -50)
        for y in range(GRID_SIZE_H)
    ]
    light_height_by_y = [
        (1 - y / max(1, GRID_SIZE_H - 1)) * 100
        for y in range(GRID_SIZE_H)
    ]


def update_cycle_math(temp):
    global cell_think_cost, predator_think_cost, predator_move_cost, temp_ptr_step, food_check_temp_offset

    cell_think_cost = normalize_int(temp, -15, 15, 50, 30)
    predator_think_cost = normalize_int(temp, -15, 15, 50, 5)
    predator_move_cost = normalize_int(temp, -15, 15, 10, 5)
    temp_ptr_step = normalize_int(temp, -15, 15, 30, 0)
    food_check_temp_offset = normalize_int(temp, -15, 15, 5, 0)


rebuild_math_caches()
