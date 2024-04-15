from genome import BotGenome, Cell
from vars import GRID_SIZE_H, GRID_SIZE_W, START_NUM_OF_CELL
from func import draw_obj, random_position
from objects import Food
import gui


# Инициализация двумерного массива мира
world_grid = [[None for _ in range(GRID_SIZE_W)] for _ in range(GRID_SIZE_H)]  # Мир в котором живут клетки


def update_surface():
    if gui.start_stop_button.click is True:
        gui.count_of_cycle += 1
    gui.count_of_cell = 0
    gui.count_of_food = 0
    for y in range(GRID_SIZE_H):
        for x in range(GRID_SIZE_W):
            obj = world_grid[y][x]
            if obj and not obj.iterated:  # Проверяем, не прошел ли объект уже итерацию
                if isinstance(obj, BotGenome):
                    if gui.start_stop_button.click is True:
                        obj.execute_genome()
                    obj.draw_obj()
                    gui.count_of_cell += 1
                elif isinstance(obj, Food):
                    if gui.start_stop_button.click is True:
                        obj.count_of_cycle += 1
                        obj.check_death()
                        obj.move()
                    gui.count_of_food += 1
                    draw_obj(obj)
                obj.iterated = True  # Устанавливаем флаг, что объект уже прошел итерацию


def init_cells():
    # Инициализация начальных клеток в мире
    for _ in range(START_NUM_OF_CELL):
        free_x, free_y = random_position(world_grid)
        bot = Cell(x=free_x, y=free_y)
        world_grid[free_y][free_x] = bot
    pass


def check_iterated():
    for y in range(GRID_SIZE_H):
        for x in range(GRID_SIZE_W):
            obj = world_grid[y][x]
            if obj:
                obj.iterated = False


init_cells()
