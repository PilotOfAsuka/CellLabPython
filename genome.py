import random
import configs as cfg
import func
import objects as objs
import surface

food_values = {
    'cell_thinks': {'min': 50, 'max': 30},  # Зависит от температуры
    'photosynthesis': {'min': 100, 'max': -100},  # Зависит от расстояния до солнца
    'predator_thinks': {'min': 10, 'max': 5},  # Зависит от температуры
    'predator_move': {'min': 10, 'max': 5},  # Зависит от температуры
    'cell_move': {'min': 10, 'max': 5},  # Зависит от температуры
}

temp, sun_coord = 0, (0, 0)
# Класс BotGenome, определяющий поведение и свойства бота


class BotGenome:
    def __init__(self, food=500, x=0, y=0, color=(148, 255, 204), genome=None):
        # Инициализация генома с заданным размером
        self.genome = [random.randint(0, 63) for _ in range(cfg.gen_size)] if genome is None else genome
        self.ptr = 0  # УТК (указатель текущей команды)
        self.food = food
        self.position = x, y
        self.color = color
        self.count_of_reproduce = 0
        self.screen_position = x * cfg.CELL_SIZE, y * cfg.CELL_SIZE
        
    MAX_ENERGY = 1100  # Максимальный уровень энергии для бота

    # функция выполнения генома
    def execute_genome(self):
        self.check_death()
        if self.food >= 1000:  # Условие для деления клетки
            self.reproduce()
        elif self.food in range(1, 1000):
            # За то что клетка думает, она теряет энергию
            self.food -= func.normalize_value(temp, -15, 15,
                                              food_values['cell_thinks']['min'], food_values['cell_thinks']['max'])
            self.check_death()
            command = self.genome[self.ptr]  # УТК
            self.execute_command(command)  # Выполнение команды генома (УТК)

        # функция выполнений команд
    def execute_command(self, command):
        # Выполнение команды в зависимости от числа
        if command in range(6, 20):
            self.photosynthesis()
        elif command in range(21, 25):
            self.move()
        elif command in range(0, 5):
            self.how_many_food()
        elif command in range(26, 30):
            self.is_this_temp()
        elif command in range(31, 40):
            self.command_view()
        elif command in range(41, 50):
            self.how_much_distance_to_sun() 
        else:
            # Если у числа нет команды, то происходит безусловный переход
            self.move_ptr_to()
        # Здесь могут быть другие команды....

    # Функция фотосинтеза
    def photosynthesis(self):
        # Логика получения энергии при фотосинтезе
        self.food += func.normalize_value(func.euclidean_distance(self.screen_position, sun_coord),
                                          0, cfg.width, food_values['photosynthesis']['min'],
                                          food_values['photosynthesis']['max'])
        # Ограничиваем максимальное количество энергии
        self.food = min(self.food, self.MAX_ENERGY)
        self.move_ptr()  # Переход УТК

    # Функция команды "Сколько у меня еды?"
    def how_many_food(self):
        food_index = (self.ptr + 1 + func.normalize_value(temp, -15, 15, 5, 0)) % len(self.genome)  # Получаем смещение
        food_genome = func.normalize_value(self.genome[food_index], 0, 63, 0, 1000)  # Получаем условие перехода

        if self.food >= food_genome:
            # Если условие перехода меньше количества собственной энергии
            self.ptr = get_next_index(self, step=2)
        else:
            # Если условие перехода больше количества собственной энергии
            self.ptr = get_next_index(self, step=3)

    # Функция перемещения УТК
    def move_ptr_to(self):
        # Перемещение УТК к следующей команде на основе числа безусловного перехода
        self.ptr = (self.ptr + self.genome[self.ptr]) % len(self.genome)

    # Функция перемещения указателя текущей команды
    def move_ptr(self):
        # Перемещения УТК к следующей команде
        self.ptr = (self.ptr + 1) % len(self.genome)

    # Опрос какая сейчас температура
    def is_this_temp(self):
        # Перемещаем указатель текущей команды
        self.ptr = get_next_index(self, step=func.normalize_value(temp, -15, 15, 30, 0))
        
    # Команда посмотреть    
    def command_view(self):
        # Выбираем направление на основе смещения
        move_dir = get_index_of_bias(self, step=1, len_of_number=len(cfg.move_directions))
        dx, dy = cfg.move_directions[move_dir]  # Получаем Направление
        
        # Получаем точку куда мы смотрим
        x, y = self.position
        new_x = (x + dx) % cfg.GRID_SIZE_W
        new_y = (y + dy) % cfg.GRID_SIZE_H
        
        # Если на пути пусто
        if surface.world_grid[new_y][new_x] is None:
            # Перемещаем указатель текущей команды
            self.ptr = get_next_index(self, step=2)
        # Если на пути органика
        elif isinstance(surface.world_grid[new_y][new_x], objs.Food):
            # Перемещаем указатель текущей команды
            self.ptr = get_next_index(self, step=43)
        # Если на пути клетка
        elif isinstance(surface.world_grid[new_y][new_x], Cell):
            # Перемещаем указатель текущей команды
            self.ptr = get_next_index(self, step=59)
        # Если на пути хищник
        elif isinstance(surface.world_grid[new_y][new_x], Predator):
            # Перемещаем указатель текущей команды
            self.ptr = get_next_index(self, step=24)
            
    # Функция опроса расстояния до солнца и смещения  
    def how_much_distance_to_sun(self):
        sun_dist = func.normalize_value(func.euclidean_distance(self.screen_position, sun_coord),
                                        0, cfg.world_size, 0, 64)
        # Перемещаем указатель текущей команды
        self.ptr = get_next_index(self, step=sun_dist)

    def check_death(self):
        if self.food <= 0:  # Условие смерти клетки при отрицательной энергии
            x, y = self.position
            surface.world_grid[y][x] = None  # Удаление бота из сетки


class Predator(BotGenome):
    def __init__(self, food=800, x=0, y=0, color=(230, 1, 92), genome=None):
        super().__init__(food, x, y, color, genome)
        
    # Функция выполнения генома
    def execute_genome(self):
        # Проверка на смерть бота, если его пищи нет
        self.check_death()
        if self.food >= 1000:  # Условие для деления клетки
            self.reproduce()
        elif self.food in range(1, 1000):
            # За то что клетка думает, она теряет энергию
            self.food -= func.normalize_value(temp, -15, 15, food_values['predator_thinks']['min'],
                                              food_values['predator_thinks']['max'])
            self.check_death()
            command = self.genome[self.ptr]  # УТК
            self.execute_command(command)  # Выполнение команды генома (УТК)
        
    def execute_command(self, command):
        # Выполнение команды в зависимости от числа
        if command in range(0, 15):
            self.move()
        elif command in range(16, 24):
            self.how_many_food()
        elif command in range(25, 40):
            self.is_this_temp()
        elif command in range(41, 50):
            self.command_view()
        elif command in range(51, 55):
            self.how_much_distance_to_sun()
        else:
            # Если у числа нет команды, то происходит безусловный переход
            self.move_ptr_to()
        # Здесь могут быть другие команды....
        
    # функция движения клетки и проверки на столкновение
    def move(self):
        # Логика расхода энергии
        self.food -= func.normalize_value(temp, -15, 15, food_values['predator_move']['min'],
                                          food_values['predator_move']['max'])
        self.check_death()
        # Выбираем направление на основе смещения
        move_dir = get_index_of_bias(self, step=1, len_of_number=len(cfg.move_directions))
        # Получаем Направление
        dx, dy = cfg.move_directions[move_dir]  

        # Получаем текущие и новые координаты
        x, y = self.position
        new_x = (x + dx) % cfg.GRID_SIZE_W
        new_y = (y + dy) % cfg.GRID_SIZE_H

        # Проверка, свободна ли новая позиция
        if surface.world_grid[new_y][new_x] is None:
            move_cell(self, x, y, new_x, new_y)
            
        # Если куда хочет шагнуть клетка есть еда
        elif isinstance(surface.world_grid[new_y][new_x], objs.Food):
            # Перемещаем клетку
            move_cell(self, x, y, new_x, new_y)
            
            self.food += 1  # Логика расхода энергии
            
            # Перемещаем УТК
            self.ptr = get_next_index(self, step=43)

        # Если куда хочет шагнуть клетка есть клетка
        elif isinstance(surface.world_grid[new_y][new_x], Cell):
            # Перемещаем клетку
            move_cell(self, x, y, new_x, new_y)
            
            self.food += 70  # Логика расхода энергии
            
            # Перемещаем УТК
            self.ptr = get_next_index(self, step=24)
            
        # Если куда хочет шагнуть клетка есть хищник   
        elif isinstance(surface.world_grid[new_x][new_y], Predator):
            self.ptr = get_next_index(self, step=59)

    # Функция деления
    def reproduce(self):
        # Получаем список свободных позиций вокруг бота
        free_positions = func.get_free_adjacent_positions(self.position, surface.world_grid)

        if not free_positions:
            x, y = self.position
            # Удаление бота из сетки если Нет свободных позиций для размножения
            surface.world_grid[y][x] = None
            if random.random() < 0.1:
                # С шансом 10 процентов после смерти бота появляется органика (Если нет места для размножения)
                surface.world_grid[y][x] = objs.Food(self, x=x, y=y, food=100)
            return

        # Выбираем случайную свободную позицию для нового бота
        x, y = random.choice(free_positions)

        # Копируем геном родителя
        new_genome = self.genome.copy()

        # Проводим мутацию в геноме
        func.mutate_genome(new_genome)

        # Создаем нового бота с мутированным геномом
        new_color = (max(self.color[0] - 1, 90), 0, 0)  # Смещаем цвета
        new_bot = Predator(food=self.food // 4, x=x, y=y, color=new_color, genome=new_genome)  # Создание нового бота
        surface.world_grid[y][x] = new_bot  # Помещаем нового бота в мир
        self.food //= 4  # Разделяем энергию между родительской и дочерней клетки


class Cell(BotGenome):
    def __init__(self, food=500, x=0, y=0, color=(0, 255, 0), genome=None):
        super().__init__(food, x, y, color, genome)
        
    # функция движения клетки и проверки на столкновение
    def move(self):
        # Логика расхода энергии
        self.food -= func.normalize_value(temp, -15, 15, food_values['cell_move']['min'],
                                          food_values['cell_move']['max'])
        self.check_death()
        # Выбираем направление на основе смещения
        move_dir = get_index_of_bias(self, step=1, len_of_number=len(cfg.move_directions))
        dx, dy = cfg.move_directions[move_dir]  # Получаем Направление

        # Получение текущей и новой позиции
        x, y = self.position
        new_x = (x + dx) % cfg.GRID_SIZE_W
        new_y = (y + dy) % cfg.GRID_SIZE_H

        # Проверка, свободна ли новая позиция
        if surface.world_grid[new_y][new_x] is None:
            # Перемещаем клетку
            move_cell(self, x, y, new_x, new_y)

        # Если куда хочет шагнуть клетка есть еда
        elif isinstance(surface.world_grid[new_y][new_x], objs.Food):
            # Перемещаем клетку
            move_cell(self, x, y, new_x, new_y)
            
            self.food += 1  # Логика расхода энергии
            # Перемещаем указатель текущей команды
            self.ptr = get_next_index(self, step=43)

        # Если куда хочет шагнуть клетка есть такая же клетка
        elif isinstance(surface.world_grid[new_y][new_x], Cell):
            # Перемещаем указатель текущей команды
            self.ptr = get_next_index(self, step=59)
            
        # Если куда хочет шагнуть клетка есть хищник
        elif isinstance(surface.world_grid[new_y][new_x], Predator):
            # Перемещаем указатель текущей команды
            self.ptr = get_next_index(self, step=24)
            
    # Функция деления
    def reproduce(self):
        # Получаем список свободных позиций вокруг бота
        free_positions = func.get_free_adjacent_positions(
            self.position, surface.world_grid)

        if not free_positions:
            x, y = self.position
            # Удаление бота из сетки если Нет свободных позиций для размножения
            surface.world_grid[y][x] = None
            if random.random() < 0.1:
                # С шансом 10 процентов после смерти бота появляется органика (Если нет места для размножения)
                surface.world_grid[y][x] = objs.Food(self, x=x, y=y, food=100)
            return

        # Выбираем случайную свободную позицию для нового бота
        x, y = random.choice(free_positions)

        # Копируем геном родителя
        new_genome = self.genome.copy()

        # Проводим мутацию в геноме
        func.mutate_genome(new_genome)

        # Создаем нового бота с мутированным геномом
        new_color = (self.color[0], max(self.color[1] - 1, 90), self.color[2])  # Смещаем цвета
        
        if self.count_of_reproduce == 10 and get_index_of_bias(self, step=2, len_of_number=2) == 1:
            new_bot = Predator(food=self.food // 2, x=x, y=y,
                               color=(230, 1, 92), genome=new_genome)  # Создание нового бота
            surface.world_grid[y][x] = new_bot  # Помещаем нового бота в мир
            self.food //= 4  # Разделяем энергию между родительской и дочерней клетки
        else:
            new_bot = Cell(food=self.food // 4, x=x, y=y,
                           color=new_color, genome=new_genome)  # Создание нового бота
            surface.world_grid[y][x] = new_bot  # Помещаем нового бота в мир
            self.food //= 4  # Разделяем энергию между родительской и дочерней клетки 
            
        self.count_of_reproduce += 1
        
        
def get_index_of_bias(self, step, len_of_number):
    """
    Функция получения смещения.
    Используется для получения условия на основе числа смещения
    [...33,43,24,...]
    [... 5, 6, 7,...]
    Пример self.ptr = 5
           step = 1
           index = 6
    Так как мы к self.ptr прибавили step и получили индекс смешение по гену
    len_of_number число ограничитель (К примеру если len_of_number является len(cfg.move_directions)
    то мы получим значение ограниченное количеством направлений от числа в гене
    43 % 8 - кол-во направлений = 3 - Вправо и низ)
    """
    index = (self.ptr + step) % len(self.genome)  # Индекс смещения
    index_of_bias = self.genome[index] % len_of_number
    return index_of_bias


def get_next_index(self, step):
    """
    Функция получения следующего индекса смешения
    используется для увеличения УТК на число полученное в смешении
    [...33,43,24,...]
    [... 5, 6, 7,...]
    Пример self.ptr = 5
           step = 1
           index = 6
    В данном примере УТК переместится на 43 (и остановится на 48) от позиции где он находился (Это self.ptr = 5)
    """
    index = (self.ptr + step) % len(self.genome)
    ptr = (self.ptr + self.genome[index]) % len(self.genome)
    return ptr


def move_cell(self, x, y, new_x, new_y):
    """
    Х, y = Передаем текущие координаты клетки
    new_x, new_y = Передаем новые координаты
    И перемещаем клетку
    """
    # Освобождаем текущую позицию
    surface.world_grid[y][x] = None
    # Освобождаем позицию клетки с едой
    surface.world_grid[new_y][new_x] = None
    # Перемещаем бота на новую позицию
    surface.world_grid[new_y][new_x] = self
    self.position = new_x, new_y
