from misc.vars import world_grid, START_NUM_OF_CELL
from misc.func import set_global_var, get_global_var, weather_simulation, random_position
from genome_class.genome import Cell, Food, Predator
from pygame_init_graphic import gui


def test_update_surface():
    if gui.start_stop_button.click is True:
        set_global_var(var="temp", value=weather_simulation(get_global_var(var="count_of_cycle")))
        set_global_var(var="count_of_cells", value=0)
        set_global_var(var="count_of_food", value=0)
        test_calculate_surface()




def test_draw_surface():
    if gui.draw_button.click is True:
        for y, row in enumerate(world_grid):
            for x, obj in enumerate(row):
                if obj:
                    obj.draw_obj()
    pass


# Цикл обработки двумерного массива
def test_calculate_surface():
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

def test_init_cells():
    # Инициализация начальных клеток в мире
    for _ in range(START_NUM_OF_CELL):
        free_x, free_y = random_position()
        bot = Cell(x=free_x, y=free_y)
        world_grid[free_y][free_x] = bot
    pass







