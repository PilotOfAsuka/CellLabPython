import random
from BioSystemClass.BotGenome_class import BotGenome
from BioSystemClass.Predator_class import Predator
from BioSystemClass.Genome_class import Genome
from misc.vars import food_values, world_grid, GRID_SIZE_H
from misc.func.func import normalize_value, get_global_var, get_free_adjacent_positions, mutate_genome_new


class Cell(BotGenome):
    def __init__(self, food=500, x=0, y=0, color=(0, 255, 0), genome=None):
        super().__init__(food, x, y, color, genome)

    # Функция выполнения генома
    def execute_genome(self):
        # Проверка на смерть бота, если его пищи нет
        self.check_death()
        if self.food >= 1000:  # Условие для деления клетки
            self.reproduce()

        elif self.food in range(1, 1000):
            # За то что клетка думает, она теряет энергию
            self.food -= normalize_value(get_global_var("temp"), -15, 15, food_values['cell_thinks']['min'],
                                         food_values['cell_thinks']['max'])

            self.execute_command(self.genome.dna[self.genome.ptr])  # Выполнение команды генома (УТК)

    def execute_command(self, command):
        # Выполнение команды в зависимости от числа
        if command in range(0, 15):
            self.photosynthesis()
        elif command in range(15, 24):
            self.how_many_food()
        elif command in range(24, 40):
            self.is_this_temp()
        elif command in range(40, 50):
            self.command_view()
        elif command in range(50, 55):
            self.how_much_distance_to_sun()
        else:
            # Если у числа нет команды, то происходит безусловный переход
            self.genome.move_ptr_to()
        # Здесь могут быть другие команды....

        # Функция фотосинтеза

    def photosynthesis(self):
        # Логика получения энергии при фотосинтезе
        self.food += normalize_value(self.position[1], 0, GRID_SIZE_H,
                                     food_values['photosynthesis']['min'], food_values['photosynthesis']['max'])
        # Ограничиваем максимальное количество энергии
        self.food = min(self.food, self.max_energy)
        self.genome.move_ptr()  # Переход УТК

    # Функция деления
    def reproduce(self):
        # Получаем список свободных позиций вокруг бота
        free_positions = get_free_adjacent_positions(self.position)

        if not free_positions:
            self.food = self.food // 2
            return

        # Выбираем случайную свободную позицию для нового бота
        x, y = free_positions[self.genome.self_get_next_index_of_bias(1, len(free_positions))]
        # Копируем геном родителя
        new_genome = self.genome.dna.copy()

        # Проводим мутацию в геноме
        mutate_genome_new(new_genome, 0.5, random.randint(0, 63))

        # Создаем нового бота с мутированным геномом
        if self.genome.self_get_bias(step=1) in range(20):
            new_bot = Predator(food=self.food // 2, x=x, y=y,
                               color=(230, 1, 92), genome=Genome(dna=new_genome))  # Создание нового бота
            world_grid[y][x] = new_bot  # Помещаем нового бота в мир
            self.food //= 4  # Разделяем энергию между родительской и дочерней клетки
        else:
            new_bot = Cell(food=self.food // 4, x=x, y=y,
                           color=(50, 150 + self.genome.dna[0], 50),
                           genome=Genome(dna=new_genome))  # Создание нового бота
            world_grid[y][x] = new_bot  # Помещаем нового бота в мир
            self.food //= 4  # Разделяем энергию между родительской и дочерней клетки

        self.count_of_reproduce += 1
