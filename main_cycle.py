from misc.func.func import get_global_var
from misc.func.clear_scr import cls
from simulation import update_surface
import time


def draw_info(elapsed_time):
    cls()
    print("Cycle: " + str(get_global_var("count_of_cycle")))
    print("Elapsed time: " + str(elapsed_time) + " sec.")
    print("Count of Cells: " + str(get_global_var("count_of_cells")))
    print("Food: " + str(get_global_var("count_of_food")))
    print("Predators: " + str(get_global_var("count_of_predators")))
    print("Cells: " + str(get_global_var("count_of_cells") - get_global_var("count_of_predators")))
    print("Temp: " + str(get_global_var("temp")))


def main_cycle(run=False):
    while run:
        start_time = time.time()
        update_surface()
        end_time = time.time()
        elapsed_time = end_time - start_time
        draw_info(elapsed_time)

