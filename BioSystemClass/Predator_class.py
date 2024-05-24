import random

from BioSystemClass.BotGenome_class import BotGenome
from BioSystemClass.Other_func_for_cells import move_cell
from BioSystemClass.Genome_class import Genome
from misc.func.func import normalize_value, get_global_var, get_free_adjacent_positions, mutate_genome_new

from misc.vars import food_values, world_grid, move_directions, GRID_SIZE_H, GRID_SIZE_W


class Predator(BotGenome):
    def __init__(self, food=800, x=0, y=0, color=(230, 1, 92), genome=None):
        super().__init__(food, x, y, color, genome)

    # Функция выполнения генома
    def execute_genome(self):
        # Проверка на смерть бота, если его пищи нет
        self.check_death()

        if self.food in range(1, 999):
            # За то что клетка думает, она теряет энергию
            self.food -= normalize_value(get_global_var("temp"), -15, 15,
                                         food_values['predator_thinks']['min'], food_values['predator_thinks']['max'])

            self.execute_command(self.genome.dna[self.genome.ptr])  # Выполнение команды генома (УТК)

        elif self.food >= 1000:  # Условие для деления клетки
            self.reproduce()

    def execute_command(self, command):
        # Выполнение команды в зависимости от числа
        if command in range(0, 20):
            self.move()
        elif command in range(20, 25):
            self.how_many_food()
        elif command in range(25, 40):
            self.is_this_temp()
        elif command in range(40, 50):
            self.command_view()
        elif command in range(50, 55):
            self.how_much_distance_to_sun()
        else:
            # Если у числа нет команды, то происходит безусловный переход
            self.genome.move_ptr_to()
        # Здесь могут быть другие команды....

    # функция движения клетки и проверки на столкновение
    def move(self):
        # Логика расхода энергии
        self.food -= normalize_value(get_global_var("temp"), -15, 15,
                                     food_values['predator_move']['min'], food_values['predator_move']['max'])

        # Выбираем направление на основе смещения
        dx, dy = move_directions[self.genome.self_get_next_index_of_bias(step=1, len_of_number=len(move_directions))]

        # Получаем текущие и новые координаты
        x, y = self.position
        new_x = (x + dx) % GRID_SIZE_W
        new_y = y + dy if -1 < y + dy < GRID_SIZE_H else y

        # Проверка, свободна ли новая позиция
        if world_grid[new_y][new_x] is None:
            move_cell(self, x, y, new_x, new_y)

        # Если куда хочет шагнуть клетка есть еда
        elif world_grid[new_y][new_x].__class__.__name__ is "Food":
            # Перемещаем клетку

            move_cell(self, x, y, new_x, new_y)
            self.food += 100  # Логика расхода энергии

            # Перемещаем УТК
            self.genome.ptr = self.genome.self_get_next_index(step=24)

        # Если куда хочет шагнуть клетка есть клетка
        elif world_grid[new_y][new_x].__class__.__name__ == "Cell":
            if world_grid[new_y][new_x].genome.self_get_bias(step=1) in range(32):
                # Перемещаем клетку
                move_cell(self, x, y, new_x, new_y)

                self.food += 25  # Логика расхода энергии

                # Перемещаем УТК
                self.genome.ptr = self.genome.self_get_next_index(step=24)
            else:
                # Перемещаем УТК
                self.genome.ptr = self.genome.self_get_next_index(step=42)

        # Если куда хочет шагнуть клетка есть хищник
        elif world_grid[new_y][new_x].__class__.__name__ == "Predator":
            self.genome.ptr = self.genome.self_get_next_index(step=59)

    # Функция деления
    def reproduce(self):
        # Получаем список свободных позиций вокруг бота
        free_positions = get_free_adjacent_positions(self.position)

        if not free_positions:
            """ x, y = self.position
            # Удаление бота из сетки если Нет свободных позиций для размножения
            world_grid[y][x] = None"""
            self.food = self.food // 2
            return

        # Выбираем случайную свободную позицию для нового бота
        x, y = free_positions[self.genome.self_get_next_index_of_bias(1, len(free_positions))]

        # Копируем геном родителя
        new_genome = self.genome.dna.copy()

        # Проводим мутацию в геноме
        mutate_genome_new(new_genome, 0.10, random.randint(0, 63))

        # Создаем нового бота с мутированным геномом
        new_color = (max(self.color[0] - 1, 90), 0, 0)  # Смещаем цвета
        new_bot = Predator(food=self.food // 4, x=x, y=y, color=new_color,
                           genome=Genome(dna=new_genome))  # Создание нового бота
        world_grid[y][x] = new_bot  # Помещаем нового бота в мир
        self.food //= 4  # Разделяем энергию между родительской и дочерней клетки
