import random

from BioSystemClass.Genome_class import Genome
from BioSystemClass.Food_class import Food
from BioSystemClass.Other_func_for_cells import get_colors_bias

from misc.func.func import normalize_value, get_global_var

from misc.vars import move_directions, GRID_SIZE_W, GRID_SIZE_H, world_grid

# Класс BotGenome, определяющий поведение и свойства бота
class BotGenome:
    def __init__(self, food=500, x=0, y=0, color=(50, 255, 50), genome=None):
        # Инициализация генома с заданным размером
        self.genome = Genome() if genome is None else genome
        self.food = food
        self.position = x, y
        self.color = color
        self.count_of_reproduce = 0
        self.count_of_cycle = 0
        self.max_energy = 1000

    # Функция команды "Сколько у меня еды?"
    def how_many_food(self):
        food_index = ((self.genome.ptr + 1 + normalize_value(get_global_var("temp"), -15, 15, 5, 0))
                      % len(self.genome.dna))  # Получаем смещение

        food_genome = normalize_value(self.genome.dna[food_index], 0, 63, 0, 1000)  # Получаем условие перехода

        if self.food >= food_genome:
            # Если условие перехода меньше количества собственной энергии
            self.genome.ptr = self.genome.self_get_next_index(step=2)
        else:
            # Если условие перехода больше количества собственной энергии
            self.genome.ptr = self.genome.self_get_next_index(step=3)

    # Опрос какая сейчас температура
    def is_this_temp(self):
        # Перемещаем указатель текущей команды
        self.genome.ptr = self.genome.self_get_next_index(step=normalize_value(get_global_var("temp"), -15, 15, 30, 0))

    # Команда посмотреть
    def command_view(self):
        # Выбираем направление на основе смещения
        dx, dy = move_directions[self.genome.self_get_next_index_of_bias(step=1, len_of_number=len(move_directions))]

        # Получаем точку куда мы смотрим
        x, y = self.position
        new_x = (x + dx) % GRID_SIZE_W
        new_y = y + dy if -1 < y + dy < GRID_SIZE_H else y

        # Если на пути пусто
        if world_grid[new_y][new_x] is None:
            # Перемещаем указатель текущей команды
            self.genome.ptr = self.genome.self_get_next_index(step=2)
        # Если на пути органика
        elif world_grid[new_y][new_x].__class__.__name__ is "Food":
            # Перемещаем указатель текущей команды
            self.genome.ptr = self.genome.self_get_next_index(step=43)
        # Если на пути клетка
        elif world_grid[new_y][new_x].__class__.__name__ is "Cell":
            # Перемещаем указатель текущей команды
            self.genome.ptr = self.genome.self_get_next_index(step=59)
        # Если на пути хищник
        elif world_grid[new_y][new_x].__class__.__name__ is "Predator":
            # Перемещаем указатель текущей команды
            self.genome.ptr = self.genome.self_get_next_index(step=24)

    # Функция опроса расстояния до солнца и смещения
    def how_much_distance_to_sun(self):
        # Перемещаем указатель текущей команды
        self.genome.ptr = self.genome.self_get_next_index(step=normalize_value(self.position[1], 0, GRID_SIZE_H, 0, 5))

    def check_death(self):
        if self.food <= 0:  # Условие смерти клетки при отрицательной энергии
            x, y = self.position
            world_grid[y][x] = None  # Удаление бота из сетки
            if random.random() < 0.1:
                world_grid[y][x] = Food(x=x, y=y, food=100, genome_number=0,
                                        color=get_colors_bias(self, 67, 117, 54, 104, 34, 84))

    def draw_obj(self):
        """
        Отрисовка объекта
        """


