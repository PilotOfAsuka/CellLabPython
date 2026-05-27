from genome import Cell, Food, Predator
from misc.vars import GRID_SIZE_H, GRID_SIZE_W, START_NUM_OF_CELL, world_grid
from misc.func import random_position, set_global_var, get_global_var


def update_simulation(is_running=True):
    if is_running:
        calculate_surface()


def calculate_surface():
    current_cycle = get_global_var("count_of_cycle")
    count_of_cells = 0
    count_of_food = 0

    for y in range(GRID_SIZE_H):
        for x in range(GRID_SIZE_W):
            obj = world_grid[y][x]
            if obj is None or obj.count_of_cycle != current_cycle:
                continue

            if isinstance(obj, (Cell, Predator)):
                obj.execute_genome()

            elif isinstance(obj, Food):
                if obj.check_death():
                    continue
                obj.move()

            obj_x, obj_y = obj.position
            if world_grid[obj_y][obj_x] is obj:
                obj.augment_count_of_life()  # Увеличиваем счетчик прожитых циклов
                obj.count_of_cycle = current_cycle + 1
                if isinstance(obj, (Cell, Predator)):
                    count_of_cells += 1
                elif isinstance(obj, Food):
                    count_of_food += 1

    set_global_var(var="count_of_cells", value=count_of_cells)
    set_global_var(var="count_of_food", value=count_of_food)
    set_global_var(var="count_of_cycle", value=current_cycle + 1)


def init_cells():
    # Инициализация начальных клеток в мире
    for _ in range(START_NUM_OF_CELL):
        free_x, free_y = random_position()
        bot = Cell(x=free_x, y=free_y)
        world_grid[free_y][free_x] = bot
    pass
