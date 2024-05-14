from misc.vars import world_grid, global_vars
from misc.func import set_global_var, get_global_var, weather_simulation, draw_obj
from genome_class.cell_exe import execute_genome
from pygame_init_graphic import gui


def update_surface():
    if gui.start_stop_button.click is True:
        set_global_var(var="temp", value=weather_simulation(get_global_var(var="count_of_cycle")))
        set_global_var(var="count_of_cells", value=0)
        set_global_var(var="count_of_food", value=0)
        calculate_surface()



def draw_surface():
    if gui.draw_button.click is True:
        for y, row in enumerate(world_grid):
            for x, obj in enumerate(row):
                if obj is not None:
                    draw_obj(bot=obj)
    pass


# Цикл обработки двумерного массива
def calculate_surface():
    for y, row in enumerate(world_grid):
        for x, obj in enumerate(row):
            if obj is not None:  # Проверяем, не прошел ли объект уже итерацию
                execute_genome(bot=obj)

                set_global_var(var="count_of_cells", value=get_global_var("count_of_cells") + 1)

    set_global_var(var="count_of_cycle", value=get_global_var("count_of_cycle") + 1)




