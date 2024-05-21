
from simulation_test import test_update_surface, test_init_cells
from func import cls, get_global_var


test_init_cells()


def draw_info():
    while True:
        test_update_surface()
        cls()
        print("Cycle: " + str(get_global_var("count_of_cycle")))
        print("Count of Cells: " + str(get_global_var("count_of_cells")))
        print("Food: " + str(get_global_var("count_of_food")))
        print("Predators: " + str(get_global_var("count_of_predators")))
        print("Cells: " + str(get_global_var("count_of_cells") - get_global_var("count_of_predators")))
        print("Temp: " + str(get_global_var("temp")))


draw_info()

