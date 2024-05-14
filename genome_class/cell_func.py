from misc.func import normalize_value, get_global_var, get_free_adjacent_positions, mutate_genome_new
from misc.vars import move_directions, GRID_SIZE_H, GRID_SIZE_W, world_grid, food_values
from genome_class.genome_func import self_get_next_index, self_get_next_index_of_bias, move_ptr
from genome_class.init_new_genome import create_one_new_cell

import random

# Функция команды "Сколько у меня еды?"

def how_many_food(bot):
    ptr = bot[4]
    dna = bot[6:]
    food = bot[5]
    food_index = ((ptr + 1 + normalize_value(get_global_var("temp"), -15, 15, 5, 0))
                  % len(dna))  # Получаем смещение

    food_genome = normalize_value(dna[food_index], 0, 63, 0, 1000)  # Получаем условие перехода

    if food >= food_genome:
        # Если условие перехода меньше количества собственной энергии
        bot[4] = self_get_next_index(step=2, bot=bot)
    else:
        # Если условие перехода больше количества собственной энергии
        bot[4] = self_get_next_index(step=3, bot=bot)


# Опрос какая сейчас температура

def is_this_temp(bot):
    ptr = bot[4]
    dna = bot[6:]
    food = bot[5]
    # Перемещаем указатель текущей команды
    bot[4] = self_get_next_index(step=normalize_value(get_global_var("temp"), -15, 15, 30, 0), bot=bot)


# Команда посмотреть

def command_view(bot):
    # Выбираем направление на основе смещения
    dx, dy = move_directions[self_get_next_index_of_bias(step=1, len_of_number=len(move_directions), bot=bot)]

    # Получаем точку куда мы смотрим
    x, y = bot[1:3]
    new_x = (x + dx) % GRID_SIZE_W
    new_y = y + dy if -1 < y + dy < GRID_SIZE_H else y

    # Если на пути пусто
    if world_grid[new_y][new_x] is None:
        # Перемещаем указатель текущей команды
        bot[4] = self_get_next_index(step=2, bot=bot)
    # Если на пути клетка
    elif world_grid[new_y][new_x] is list:
        # Перемещаем указатель текущей команды
        bot[4] = self_get_next_index(step=59, bot=bot)


# Функция опроса расстояния до солнца и смещения

def how_much_distance_to_sun(bot):
    y = bot[2]
    # Перемещаем указатель текущей команды
    bot[4] = self_get_next_index(step=normalize_value(y, 0, GRID_SIZE_H, 0, 5), bot=bot)


def check_death(bot):
    if bot[5] <= 0:  # Условие смерти клетки при отрицательной энергии
        x, y = bot[1:3]
        world_grid[y][x] = None  # Удаление бота из сетки


# Функция фотосинтеза

def photosynthesis(bot):
    y = bot[2]
    food = bot[5]
    # Логика получения энергии при фотосинтезе
    bot[5] += normalize_value(y, 0, GRID_SIZE_H,
                              food_values['photosynthesis']['min'], food_values['photosynthesis']['max'])
    move_ptr(bot=bot)  # Переход УТК


# Функция деления

def reproduce(bot):
    position = bot[1:3]
    # Получаем список свободных позиций вокруг бота
    free_positions = get_free_adjacent_positions(position)

    if not free_positions:
        bot[5] = bot[5] // 2
        return

    # Выбираем случайную свободную позицию для нового бота
    new_x, new_y = free_positions[self_get_next_index_of_bias(step=1, len_of_number=len(free_positions), bot=bot)]
    # Копируем геном родителя
    dna = bot[6:]
    new_dna = dna.copy()

    # Проводим мутацию в геноме
    new_mutate_dna = mutate_genome_new(new_dna, 0.5, random.randint(0, 63))
    new_food = bot[5] // 2
    # Создаем нового бота с мутированным геномом
    new_bot = create_one_new_cell(type_of_cell=0, x=new_x, y=new_y, color_bias=bot[3], food=new_food, dna=new_mutate_dna)

    world_grid[new_y][new_x] = new_bot