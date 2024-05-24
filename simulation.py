from misc.vars import world_grid, START_NUM_OF_CELL
from misc.func.func import set_global_var, get_global_var, weather_simulation, random_position
from BioSystemClass.Food_class import Food
from BioSystemClass.Cell_class import Cell
from BioSystemClass.Predator_class import Predator


def update_surface():
    set_global_var(var="temp", value=weather_simulation(get_global_var(var="count_of_cycle")))
    set_global_var(var="count_of_cells", value=0)
    set_global_var(var="count_of_food", value=0)
    set_global_var(var="count_of_predators", value=0)
    calculate_surface()


# Цикл обработки двумерного массива
def calculate_surface():
    for y, row in enumerate(world_grid):
        for x, obj in enumerate(row):
            if obj:
                calculate_cells(obj)
                calculate_food(obj)

                obj.count_of_cycle = get_global_var("count_of_cycle") + 1

    set_global_var(var="count_of_cycle", value=get_global_var("count_of_cycle") + 1)


def test_init_cells():
    # Инициализация начальных клеток в мире
    for _ in range(START_NUM_OF_CELL):
        free_x, free_y = random_position()
        bot = Cell(x=free_x, y=free_y)
        world_grid[free_y][free_x] = bot
    pass


def calculate_cells(cell):
    if cell.__class__ in (Cell, Predator) and cell.count_of_cycle == get_global_var("count_of_cycle"):
        cell.execute_genome()
        set_global_var(var="count_of_cells", value=get_global_var("count_of_cells") + 1)
        if cell.__class__ is Predator:
            set_global_var(var="count_of_predators", value=get_global_var("count_of_predators") + 1)
    pass


def calculate_food(food):
    if food.__class__ is Food and food.count_of_cycle == get_global_var("count_of_cycle"):
        food.check_death()
        food.move()
        set_global_var(var="count_of_food", value=get_global_var("count_of_food") + 1)
        food.count_of_life += 1
    pass
