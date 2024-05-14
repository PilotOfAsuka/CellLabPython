import random
from misc.func import random_position
from misc.vars import START_NUM_OF_CELL, world_grid
from numba import jit


# Функция инициализации одной клетки
def init_one_new_cell() -> list:
    type_of_cell = 0  # 0 клетка, 1 хищник (index - 0)
    x, y = random_position()  # Свободная позиция в мире при инициализации (index - 1, 2)
    color_bias = random.randint(0, 64)  # Число смещения цвета (index - 3)
    ptr = 0  # Указатель текущей команды клетки
    food = 100
    command_list = [random.randint(0, 63) for _ in range(64)]  # Список команд (index - 6 ...)
    cell = [type_of_cell, x, y, color_bias, ptr, food] + command_list
    return cell


# Функция для создания кастомной клетки
def create_one_new_cell(type_of_cell, x, y, color_bias, food, dna) -> list:
    self_type_of_cell = type_of_cell
    self_x = x
    self_y = y
    self_color_bias = color_bias
    ptr = 0  # Указатель текущей команды клетки
    self_food = food
    command_list = dna
    cell = [self_type_of_cell, self_x, self_y, self_color_bias, ptr, self_food] + command_list
    return cell


# Функция постановки клетки в мир
def init_cells():
    # Инициализация начальных клеток в мире
    for _ in range(START_NUM_OF_CELL):
        bot = init_one_new_cell()
        x, y = bot[1:3]
        world_grid[y][x] = bot
    pass
