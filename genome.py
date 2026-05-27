import random
from misc import environment
from misc import vars as v
from misc.func import mutate_genome_new, get_free_adjacent_positions
from misc import colors as c


# Геном - список чисел 0..63. Указатель ptr смотрит на текущую команду,
# а команды часто читают соседние гены как параметры направления или перехода.
food_values = {
    'cell_thinks': {'min': 50, 'max': 30},  # Зависит от температуры
    'photosynthesis': {'min': 100, 'max': -50},  # Зависит от расстояния до солнца
    'predator_thinks': {'min':  50, 'max': 5},  # Зависит от температуры
    'predator_move': {'min': 10, 'max': 5},  # Зависит от температуры
}


class Food:
    __slots__ = (
        "food", "color", "position", "x", "y", "count_of_cycle", "count_of_life", "genome_number",
        "_render_cache_key", "_render_mapped_color"
    )

    def __init__(self, food=50, x=0, y=0, color=c.FOOD_COLOR, genome_number=0):
        self.food = food
        self.color = color
        self.position = x, y
        self.x, self.y = self.position
        self.count_of_cycle = 0
        self.count_of_life = 0
        self.genome_number = genome_number
        self._render_cache_key = None
        self._render_mapped_color = None

    def move(self):
        """
        Перемещение объекта
        """
        # Смотрим на мир сверху, поэтому органика больше не падает вниз.
        return

    def check_death(self):
        if self.get_count_of_life() >= 10000:
            x, y = self.position
            v.world_grid[y][x] = None
            return True
        return False

    def augment_count_of_life(self):
        self.count_of_life += 1
        pass

    def get_count_of_life(self):
        return self.count_of_life


# Класс BotGenome, определяющий поведение и свойства бота
class BotGenome:
    __slots__ = (
        "genome", "genome_len", "ptr", "food", "position", "color", "count_of_reproduce",
        "count_of_cycle", "count_of_life", "max_energy", "_render_cache_key", "_render_mapped_color"
    )

    def __init__(self, food=500, x=0, y=0, color=(50, 255, 50), genome=None):
        # Инициализация генома с заданным размером
        self.genome = [random.randint(0, 63) for _ in range(v.gen_size)] if genome is None else genome
        self.ptr = 0  # УТК (указатель текущей команды)
        self.food = food
        self.position = x, y
        self.color = color
        self.count_of_reproduce = 0
        self.count_of_cycle = 0
        self.count_of_life = 0
        self.max_energy = 1100
        self.genome_len = len(self.genome)
        self._render_cache_key = None
        self._render_mapped_color = None

    # Функция команды "Сколько у меня еды?"
    def how_many_food(self):
        food_index = (self.ptr + 1 + v.food_check_temp_offset) % self.genome_len  # Получаем смещение

        food_genome = self.genome[food_index] * 1000 // 63  # Получаем условие перехода

        if self.food >= food_genome:
            # Если условие перехода меньше количества собственной энергии
            self.ptr = self_get_next_index(self, step=2)
        else:
            # Если условие перехода больше количества собственной энергии
            self.ptr = self_get_next_index(self, step=3)

    # Функция перемещения УТК
    def move_ptr_to(self):
        # Перемещение УТК к следующей команде на основе числа безусловного перехода
        self.ptr = (self.ptr + self.genome[self.ptr]) % self.genome_len

    # Функция перемещения указателя текущей команды
    def move_ptr(self):
        # Перемещения УТК к следующей команде
        self.ptr = (self.ptr + 1) % self.genome_len

    # Опрос какая сейчас температура
    def is_this_temp(self):
        # Перемещаем указатель текущей команды
        self.ptr = self_get_next_index(self, step=v.temp_ptr_step)
        
    # Команда посмотреть    
    def command_view(self):
        # Выбираем направление на основе смещения
        move_dir = self_get_index_of_bias(self, step=1, len_of_number=len(v.move_directions))
        dx, dy = v.move_directions[move_dir]  # Получаем Направление
        
        # Получаем точку куда мы смотрим
        x, y = self.position
        new_x = (x + dx) % v.GRID_SIZE_W
        new_y = (y + dy) % v.GRID_SIZE_H
        target = v.world_grid[new_y][new_x]
        
        # Если на пути пусто
        if target is None:
            # Перемещаем указатель текущей команды
            self.ptr = self_get_next_index(self, step=2)
        # Если на пути органика
        elif target.__class__ is Food:
            # Перемещаем указатель текущей команды
            self.ptr = self_get_next_index(self, step=43)
        # Если на пути клетка
        elif target.__class__ is Cell:
            # Перемещаем указатель текущей команды
            self.ptr = self_get_next_index(self, step=59)
        # Если на пути хищник
        elif target.__class__ is Predator:
            # Перемещаем указатель текущей команды
            self.ptr = self_get_next_index(self, step=24)
            
    # Функция опроса расстояния до солнца и смещения  
    def how_much_distance_to_sun(self):
        x, y = self.position
        sun_dist = 5 - get_cached_light(x, y) * 5 // 100
        # Перемещаем указатель текущей команды
        self.ptr = self_get_next_index(self, step=sun_dist)

    def check_death(self):
        if self.food <= 0:  # Условие смерти клетки при отрицательной энергии
            x, y = self.position
            v.world_grid[y][x] = None  # Удаление бота из сетки
            v.set_bot_position(x, y, False)
            humidity = get_cached_humidity(x, y)
            if random.random() < min(0.35, 0.1 + humidity / 500):
                # Иногда смерть оставляет органику с фрагментом генома: это простая наследуемая среда.
                food = Food(x=x, y=y, food=300, genome_number=self_get_index_of_bias(self, 1, 64),
                            color=get_colors_bias(self, 67, 117, 54, 104, 34, 84))
                food.count_of_cycle = v.global_vars["count_of_cycle"] + 1
                v.world_grid[y][x] = food
                v.register_object(food)
            return True
        return False

    def augment_count_of_life(self):
        self.count_of_life += 1
        pass

    def get_count_of_life(self):
        return self.count_of_life

    def count_neighbors(self):
        x, y = self.position
        return v.neighbor_grid[y * v.GRID_SIZE_W + x]

    def apply_environment_effects(self):
        x, y = self.position
        signal_index = y * v.GRID_SIZE_W + x
        neighbors = v.neighbor_grid[signal_index]
        signal = environment.signal_map[signal_index]

        if neighbors > 4:
            self.food -= (neighbors - 4) * 4
        if signal > 45:
            self.ptr = self_get_next_index(self, step=1 + signal % 5)

        new_signal = signal + 18
        environment.signal_map[signal_index] = 100 if new_signal > 100 else new_signal
        if signal == 0:
            environment.active_signal_indexes.add(signal_index)



class Predator(BotGenome):
    __slots__ = ()

    def __init__(self, food=800, x=0, y=0, color=(230, 1, 92), genome=None):
        super().__init__(food, x, y, color, genome)
        
    # Функция выполнения генома
    def execute_genome(self):
        # Проверка на смерть бота, если его пищи нет
        if self.food <= 0:
            self.check_death()
            return
        x, y = self.position
        signal_index = y * v.GRID_SIZE_W + x
        neighbors = v.neighbor_grid[signal_index]
        signal = environment.signal_map[signal_index]
        if neighbors > 4:
            self.food -= (neighbors - 4) * 4
        if signal > 45:
            self.ptr = self_get_next_index(self, step=1 + signal % 5)
        new_signal = signal + 18
        environment.signal_map[signal_index] = 100 if new_signal > 100 else new_signal
        if signal == 0:
            environment.active_signal_indexes.add(signal_index)
        if self.food <= 0:
            self.check_death()
            return
        if self.food >= 1000:  # Условие для деления клетки
            self.reproduce()
        elif 0 < self.food < 1000:
            # За то что клетка думает, она теряет энергию
            self.food -= v.predator_think_cost
            if self.food <= 0:
                self.check_death()
                return
            command = self.genome[self.ptr]  # УТК
            if command < 15:
                self.move()
            elif command < 25:
                self.how_many_food()
            elif command < 40:
                self.is_this_temp()
            elif command < 50:
                self.command_view()
            elif command < 55:
                self.how_much_distance_to_sun()
            else:
                self.move_ptr_to()
        
    def execute_command(self, command):
        # Хищник тратит энергию на активное движение и может съедать клетки.
        # Выполнение команды в зависимости от числа
        if command < 15:
            self.move()
        elif command < 25:
            self.how_many_food()
        elif command < 40:
            self.is_this_temp()
        elif command < 50:
            self.command_view()
        elif command < 55:
            self.how_much_distance_to_sun()
        else:
            # Если у числа нет команды, то происходит безусловный переход
            self.move_ptr_to()
        # Здесь могут быть другие команды....
        
    # функция движения клетки и проверки на столкновение
    def move(self):
        # Логика расхода энергии
        self.food -= v.predator_move_cost
        if self.food <= 0:
            self.check_death()
            return

        # Выбираем направление на основе смещения
        move_dir = self_get_index_of_bias(self, step=1, len_of_number=len(v.move_directions))
        # Получаем Направление
        dx, dy = v.move_directions[move_dir]

        # Получаем текущие и новые координаты
        x, y = self.position
        new_x = (x + dx) % v.GRID_SIZE_W
        new_y = y + dy if -1 < y + dy < v.GRID_SIZE_H else y
        target = v.world_grid[new_y][new_x]

        # Проверка, свободна ли новая позиция
        if target is None:
            move_cell(self, x, y, new_x, new_y)
            
        # Если куда хочет шагнуть клетка есть еда
        elif target.__class__ is Food:
            # Перемещаем клетку
            food = target

            move_cell(self, x, y, new_x, new_y)
            mutate_genome_new(self.genome, 0.1, food.genome_number)
            self.food += food.food  # Логика расхода энергии
            
            # Перемещаем УТК
            self.ptr = self_get_next_index(self, step=43)

        # Если куда хочет шагнуть клетка есть клетка
        elif target.__class__ is Cell:
            if 0 < get_index_of_bias(target, 2, 10) < 5:
                # Перемещаем клетку
                move_cell(self, x, y, new_x, new_y)

                self.food += 50  # Логика расхода энергии

                # Перемещаем УТК
                self.ptr = self_get_next_index(self, step=24)
            else:
                # Перемещаем УТК
                self.ptr = self_get_next_index(self, step=42)

        # Если куда хочет шагнуть клетка есть хищник   
        elif target.__class__ is Predator:
            if self.food >= 1000:
                self.reproduce()
            else:
                self.ptr = self_get_next_index(self, step=59)

    # Функция деления
    def reproduce(self):
        # Получаем список свободных позиций вокруг бота
        free_positions = get_free_adjacent_positions(self.position)

        if not free_positions:
            x, y = self.position
            # Удаление бота из сетки если Нет свободных позиций для размножения
            v.world_grid[y][x] = None
            v.set_bot_position(x, y, False)
            return

        # Выбираем случайную свободную позицию для нового бота
        x, y = random.choice(free_positions)

        # Копируем геном родителя
        new_genome = self.genome.copy()

        # Проводим мутацию в геноме
        mutate_genome_new(new_genome, 0.10, random.randint(0, 63))

        # Создаем нового бота с мутированным геномом
        new_color = (max(self.color[0] - 1, 90), 0, 0)  # Смещаем цвета
        new_bot = Predator(food=self.food // 4, x=x, y=y, color=new_color, genome=new_genome)  # Создание нового бота
        new_bot.count_of_cycle = v.global_vars["count_of_cycle"] + 1
        v.world_grid[y][x] = new_bot  # Помещаем нового бота в мир
        v.set_bot_position(x, y)
        v.register_object(new_bot)
        self.food //= 4  # Разделяем энергию между родительской и дочерней клетки


class Cell(BotGenome):
    __slots__ = ()

    def __init__(self, food=500, x=0, y=0, color=(0, 255, 0), genome=None):
        super().__init__(food, x, y, color, genome)

        # Функция выполнения генома

    def execute_genome(self):
        # Проверка на смерть бота, если его пищи нет
        if self.food <= 0:
            self.check_death()
            return
        x, y = self.position
        signal_index = y * v.GRID_SIZE_W + x
        neighbors = v.neighbor_grid[signal_index]
        signal = environment.signal_map[signal_index]
        if neighbors > 4:
            self.food -= (neighbors - 4) * 4
        if signal > 45:
            self.ptr = self_get_next_index(self, step=1 + signal % 5)
        new_signal = signal + 18
        environment.signal_map[signal_index] = 100 if new_signal > 100 else new_signal
        if signal == 0:
            environment.active_signal_indexes.add(signal_index)
        if self.food <= 0:
            self.check_death()
            return
        if self.food >= 1000:  # Условие для деления клетки
            self.reproduce()
        elif 0 < self.food < 1000:
            # За то что клетка думает, она теряет энергию
            self.food -= v.cell_think_cost
            if self.food <= 0:
                self.check_death()
                return
            command = self.genome[self.ptr]  # УТК
            if command < 15:
                self.photosynthesis()
            elif command < 24:
                self.how_many_food()
            elif command < 40:
                self.is_this_temp()
            elif command < 50:
                self.command_view()
            elif command < 55:
                self.how_much_distance_to_sun()
            else:
                self.move_ptr_to()

    def execute_command(self, command):
        # Обычная клетка в основном фотосинтезирует и реагирует на условия мира.
        # Выполнение команды в зависимости от числа
        if command < 15:
            self.photosynthesis()
        elif command < 24:
            self.how_many_food()
        elif command < 40:
            self.is_this_temp()
        elif command < 50:
            self.command_view()
        elif command < 55:
            self.how_much_distance_to_sun()
        else:
            # Если у числа нет команды, то происходит безусловный переход
            self.move_ptr_to()
        # Здесь могут быть другие команды....

        # Функция фотосинтеза
    def photosynthesis(self):
        # Логика получения энергии при фотосинтезе
        x, y = self.position
        base_food = v.photosynthesis_by_y[y]
        humidity = get_cached_humidity(x, y)
        light = get_cached_light_by_humidity(y, humidity)
        neighbors = v.neighbor_grid[y * v.GRID_SIZE_W + x]
        pressure_penalty = max(0, neighbors - 3) * 8
        self.food += int(base_food * (0.35 + light / 90) + humidity / 4 - pressure_penalty)
        # Ограничиваем максимальное количество энергии
        self.food = min(self.food, self.max_energy)
        self.move_ptr()  # Переход УТК

    # Функция деления
    def reproduce(self):
        # Получаем список свободных позиций вокруг бота
        free_positions = get_free_adjacent_positions(self.position)

        if not free_positions:
            x, y = self.position
            # Удаление бота из сетки если Нет свободных позиций для размножения
            v.world_grid[y][x] = None
            v.set_bot_position(x, y, False)
            humidity = get_cached_humidity(x, y)
            if random.random() < min(0.35, 0.1 + humidity / 500):
                # С шансом 10 процентов после смерти бота появляется органика (Если нет места для размножения)
                food = Food(
                    x=x, y=y, food=300, genome_number=self_get_index_of_bias(self, 1, 64),
                    color=get_colors_bias(self, 67, 117, 54, 104, 34, 84))
                food.count_of_cycle = v.global_vars["count_of_cycle"] + 1
                v.world_grid[y][x] = food
                v.register_object(food)
            return

        # Выбираем случайную свободную позицию для нового бота
        index_free_pos = self_get_index_of_bias(self, 1, len(free_positions))
        x, y = free_positions[index_free_pos]
        # Копируем геном родителя
        new_genome = self.genome.copy()

        # Проводим мутацию в геноме
        mutate_genome_new(new_genome, 0.10, random.randint(0, 63))

        # Создаем нового бота с мутированным геномом
        new_color = (50, 192 + self.genome[0], 50)  # Смещаем цвета

        if self.count_of_reproduce == 10 and self_get_index_of_bias(self, step=2, len_of_number=2) == 1:
            new_bot = Predator(food=self.food // 2, x=x, y=y,
                               color=(230, 1, 92), genome=new_genome)  # Создание нового бота
            new_bot.count_of_cycle = v.global_vars["count_of_cycle"] + 1
            v.world_grid[y][x] = new_bot  # Помещаем нового бота в мир
            v.set_bot_position(x, y)
            v.register_object(new_bot)
            self.food //= 4  # Разделяем энергию между родительской и дочерней клетки
        else:
            new_bot = Cell(food=self.food // 4, x=x, y=y,
                           color=new_color, genome=new_genome)  # Создание нового бота
            new_bot.count_of_cycle = v.global_vars["count_of_cycle"] + 1
            v.world_grid[y][x] = new_bot  # Помещаем нового бота в мир
            v.set_bot_position(x, y)
            v.register_object(new_bot)
            self.food //= 4  # Разделяем энергию между родительской и дочерней клетки 
            
        self.count_of_reproduce += 1


def self_get_index_of_bias(self, step, len_of_number):
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
    index = (self.ptr + step) % self.genome_len  # Индекс смещения
    index_of_bias = self.genome[index] % len_of_number
    return index_of_bias


def get_cached_humidity(x, y):
    if not environment.humidity_map:
        return 0
    return environment.humidity_map[y * v.GRID_SIZE_W + x]


def get_cached_light_by_humidity(y, humidity):
    light = v.light_height_by_y[y] * v.current_daylight - humidity * 0.22
    if light < 5:
        return 5
    if light > 100:
        return 100
    return int(light)


def get_cached_light(x, y):
    return get_cached_light_by_humidity(y, get_cached_humidity(x, y))


def self_get_next_index(self, step):
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
    index = (self.ptr + step) % self.genome_len
    ptr = (self.ptr + self.genome[index]) % self.genome_len
    return ptr


def move_cell(self, x, y, new_x, new_y):
    """
    Х, y = Передаем текущие координаты клетки
    new_x, new_y = Передаем новые координаты
    И перемещаем клетку
    """
    # Освобождаем текущую позицию
    v.world_grid[y][x] = None
    v.set_bot_position(x, y, False)
    # Освобождаем позицию клетки с едой
    v.world_grid[new_y][new_x] = None
    # Перемещаем бота на новую позицию
    v.world_grid[new_y][new_x] = self
    v.set_bot_position(new_x, new_y)
    self.position = new_x, new_y


def get_index_of_bias(bot, step, len_of_number):
    """
    Функция получения смещения.
    Используется для получения условия на основе числа смещения
    [...33,43,24,...]
    [... 5, 6, 7,...]
    Пример bot.ptr = 5
           step = 1
           index = 6
    Так как мы к self.ptr прибавили step и получили индекс смешение по гену
    len_of_number число ограничитель (К примеру если len_of_number является len(cfg.move_directions)
    то мы получим значение ограниченное количеством направлений от числа в гене
    43 % 8 - кол-во направлений = 3 - Вправо и низ)
    """
    index = (bot.ptr + step) % bot.genome_len  # Индекс смещения
    index_of_bias = bot.genome[index] % len_of_number
    return index_of_bias


def get_colors_bias(self, first_min, first_max, second_min, second_max, third_min, third_max):
    colors = (max(min(self.genome[0] % 255, first_max), first_min),
              max(min(self.genome[0] % 255, second_max), second_min),
              max(min(self.genome[0] % 255, third_max), third_min))

    return colors
