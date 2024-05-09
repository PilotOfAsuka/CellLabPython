from genome_class.genome import Cell, Food, Predator
from genome_class.genome_2d import Cell_2d
from misc.vars import START_NUM_OF_CELL, world_grid, world_grid_2d
from misc.func import random_position, set_global_var, get_global_var, weather_simulation
from misc.func_2d import get_index
from pygame_init_graphic import gui




def update_surface():
    if gui.start_stop_button.click is True:
        set_global_var(var="temp", value=weather_simulation(get_global_var("count_of_cycle")))
        set_global_var(var="count_of_cells", value=0)
        set_global_var(var="count_of_food", value=0)
        calculate_surface()
        #calculate_2d_surface()


def draw_surface():
    if gui.draw_button.click is True:
        for y, row in enumerate(world_grid):
            for x, obj in enumerate(row):
                if obj:
                    obj.draw_obj()
    pass


def draw_2d_surface():
    if gui.draw_button.click is True:
        for obj in world_grid_2d:
            if obj:
                obj.draw_obj()
    pass


# Цикл обработки двумерного массива
def calculate_surface():
    for y, row in enumerate(world_grid):
        for x, obj in enumerate(row):
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


# Цикл обработки одномерного массива
def calculate_2d_surface():
    for obj in world_grid_2d:
        if obj:
            if obj.__class__ in (Cell_2d, Predator) and obj.count_of_cycle == get_global_var("count_of_cycle"):
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


def init_2d_cells():
    # Инициализация начальных клеток в мире
    for _ in range(START_NUM_OF_CELL):
        free_x, free_y = random_position()
        bot = Cell_2d(x=free_x, y=free_y)
        index = get_index(free_x,free_y)
        world_grid_2d[index] = bot
    pass

