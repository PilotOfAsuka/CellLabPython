from genome_class.genome import Cell, Food, Predator
from misc.vars import GRID_SIZE_H, GRID_SIZE_W, START_NUM_OF_CELL, world_grid
from misc.func import random_position, set_global_var, get_global_var, weather_simulation
from pygame_init_graphic import gui


def update_surface():
    if gui.start_stop_button.click is True:
        set_global_var(var="temp", value=weather_simulation(get_global_var("count_of_cycle")))
        set_global_var(var="count_of_cells", value=0)
        set_global_var(var="count_of_food", value=0)
        calculate_surface()


def draw_surface():
    if gui.draw_button.click is True:
        for y in range(GRID_SIZE_H):
            for x in range(GRID_SIZE_W):
                obj = world_grid[y][x]
                if obj is not None:
                    obj.draw_obj()
    pass


def calculate_surface():
    for y in range(GRID_SIZE_H):
        for x in range(GRID_SIZE_W):
            obj = world_grid[y][x]
            if obj:  # Проверяем, не прошел ли объект уже итерацию
                if obj.__class__ in (Cell, Predator) and obj.count_of_cycle == get_global_var("count_of_cycle"):
                    obj.execute_genome()
                    set_global_var(var="count_of_cells", value=get_global_var("count_of_cells") + 1)
                elif obj.__class__ is Food and obj.count_of_cycle == get_global_var("count_of_cycle"):
                    obj.check_death()
                    obj.move()
                    set_global_var(var="count_of_food", value=get_global_var("count_of_food") + 1)
                    obj.count_of_life += 1

                obj.count_of_cycle = get_global_var("count_of_cycle") + 1
    set_global_var(var="count_of_cycle", value=get_global_var("count_of_cycle") + 1)


def init_cells():
    # Инициализация начальных клеток в мире
    for _ in range(START_NUM_OF_CELL):
        free_x, free_y = random_position()
        bot = Cell(x=free_x, y=free_y)
        world_grid[free_y][free_x] = bot
    pass
