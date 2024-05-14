from genome_class.cell_func import check_death, reproduce, photosynthesis,how_much_distance_to_sun, how_many_food, is_this_temp, command_view
from genome_class.genome_func import move_ptr_to
from misc.func import normalize_value, get_global_var
from misc.vars import food_values
from numba import jit


def execute_genome(bot):
    ptr = bot[4]
    dna = bot[6:]
    # Проверка на смерть бота, если его пищи нет
    check_death(bot=bot)
    if bot[5] >= 1000:  # Условие для деления клетки
        reproduce(bot=bot)

    elif bot[5] in range(1, 1000):
        # За то что клетка думает, она теряет энергию
        bot[5] -= normalize_value(get_global_var(var="temp"), -15, 15, food_values['cell_thinks']['min'],
                                     food_values['cell_thinks']['max'])

        execute_command(command=dna[ptr], bot=bot)  # Выполнение команды генома (УТК)


def execute_command(command, bot):
    # Выполнение команды в зависимости от числа
    if command in range(0, 15):
        photosynthesis(bot=bot)
    elif command in range(15, 24):
        how_many_food(bot=bot)
    elif command in range(24, 40):
        is_this_temp(bot=bot)
    elif command in range(40, 50):
        command_view(bot=bot)
    elif command in range(50, 55):
        how_much_distance_to_sun(bot=bot)
    else:
        # Если у числа нет команды, то происходит безусловный переход
        move_ptr_to(bot=bot)
    # Здесь могут быть другие команды....
