from genome import Cell, Food, Predator
from misc import environment
from misc import vars as v
from misc.func import random_position


# Этот модуль отвечает только за логику мира: кто живет, двигается, ест и делится.
# Отрисовка находится в pygame_init_graphic/renderer.py, поэтому симуляцию можно тестировать без pygame.
def update_simulation(is_running=True):
    if is_running:
        calculate_surface()


def calculate_surface():
    # count_of_cycle защищает объекты от повторного хода после перемещения или рождения.
    current_cycle = v.global_vars["count_of_cycle"]
    v.update_cycle_math(v.global_vars["temp"])
    v.current_daylight = environment.get_daylight(current_cycle)
    count_of_cells = 0
    count_of_food = 0
    cycle_objects = v.active_objects
    v.active_objects = []
    active_append = v.active_objects.append
    world_grid = v.world_grid
    grid_w = v.GRID_SIZE_W
    grid_h = v.GRID_SIZE_H

    for obj in cycle_objects:
        x, y = obj.position
        if not (0 <= x < grid_w and 0 <= y < grid_h):
            continue
        if world_grid[y][x] is not obj:
            continue
        if obj.count_of_cycle != current_cycle:
            active_append(obj)
            continue

        if obj.__class__ is Food:
            if obj.count_of_life >= 10000:
                world_grid[y][x] = None
                continue
        else:
            obj.execute_genome()

        obj_x, obj_y = obj.position
        if world_grid[obj_y][obj_x] is obj:
            obj.count_of_life += 1  # Увеличиваем счетчик прожитых циклов
            obj.count_of_cycle = current_cycle + 1
            active_append(obj)
            if obj.__class__ is Food:
                count_of_food += 1
            else:
                count_of_cells += 1

    v.global_vars["count_of_cells"] = count_of_cells
    v.global_vars["count_of_food"] = count_of_food
    v.global_vars["count_of_cycle"] = current_cycle + 1
    environment.update_environment(current_cycle)


def init_cells():
    # Инициализация начальных клеток в мире
    for _ in range(v.START_NUM_OF_CELL):
        free_x, free_y = random_position()
        bot = Cell(x=free_x, y=free_y)
        v.world_grid[free_y][free_x] = bot
        v.set_bot_position(free_x, free_y)
        v.register_object(bot)
    pass


def restart_world(cell_size=None, genome_size=None, start_cells=None):
    v.apply_world_settings(cell_size, genome_size, start_cells)
    v.reset_world_counters()
    environment.reset_environment()
    init_cells()
