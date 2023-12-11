import random
import configs as cfg
import func
import objects as objs
import surface
import numpy as np

temp, illumination, sun_coord = 0, 0, (0, 0)
# Класс BotGenome, определяющий поведение и свойства бота


class BotGenome:
    def __init__(self, food=500, x=0, y=0, color=(0, 255, 0), genome=None):
        # Инициализация генома с заданным размером
        self.genome = [random.randint(0, 63) for _ in range(
            cfg.gen_size)] if genome is None else genome
        self.ptr = 0  # УТК (указатель текущей команды)
        self.food = food
        self.position = x, y
        self.color = color
    MAX_ENERGY = 1100  # Максимальный уровень энергии для бота

    # функция выполнения генома
    def execute_genome(self):
        # Проверка на смерть бота, если его пищи нет
        if self.food <= 0:  # Условие смерти клетки при отрецательной энергии
            x, y = self.position
            surface.world_grid[y][x] = None  # Удаление бота из сетки
        elif self.food >= 1000:  # Условие для деления клетки
            self.reproduce()
        elif self.food in range(1,1000):
            # За то что клетка думает она теряет энергию
            self.food -= func.normalize_value(temp, -15, 15, 10, 5)
            command = self.genome[self.ptr]  # УТК
            self.execute_command(command)  # Выполнение команды генома (УТК)

        # функция выполнений команд

    def execute_command(self, command):
        # Выполнение команды в зависимости от числа
        if command in range(10, 20):
            self.photosynthesis()
        elif command in range(21, 25):
            self.move()
        elif command == range(0, 9):
            self.how_many_food()
        elif command in range(26, 30):
            self.is_this_temp()
        elif command in range(31, 40):
            self.command_view()
        else:
            # Если у числа нет команды то происходит безусловный переход
            self.move_ptr_to()
        # Здесь могут быть другие команды....

    # Функция фотосинтеза
    def photosynthesis(self):
        illumination, sun_dist = self.food_consumption()
        # Логика получения энергии при фотосинтезе
        self.food += func.normalize_value(sun_dist, 250, 0, 1, 50)
        # Ограничиваем максимальное количество энергии
        self.food = min(self.food, self.MAX_ENERGY)
        self.move_ptr()  # Переход УТК

    # Функция команды "Сколько у меня еды?"
    def how_many_food(self):
        food_index = (self.ptr + 1) % len(self.genome)  # Получаем смещение
        next_ptr_index = (self.ptr + 2 + func.euclidean_distance(self.position, sun_coord)) % len(self.genome)
        next_next_ptr_index = (self.ptr + 3 + func.euclidean_distance(self.position, sun_coord)) % len(self.genome)
        food_genome = self.genome[food_index] * 15  # Получаем условие перехода

        if self.food >= food_genome:
            # Если условие перехода меньше количеста собственной энергии
            self.ptr = (
                self.ptr + self.genome[next_ptr_index]) % len(self.genome)
        else:
            # Если условие перехода больше количеста собственной энергии
            self.ptr = (
                self.ptr + self.genome[next_next_ptr_index]) % len(self.genome)

    # функция движения клетки и проверки на столкновение
    def move(self):
        # Модификация для движения бота
        move_dir_index = (self.ptr + 1) % len(self.genome)  # Индекс смещения
        # Выбираем направление на основе смещения
        move_dir = self.genome[move_dir_index] % len(cfg.move_directions)
        dx, dy = cfg.move_directions[move_dir]  # Получаем Направление

        # Обновление позиции бота
        x, y = self.position
        new_x = (x + dx) % cfg.GRID_SIZE_W
        new_y = (y + dy) % cfg.GRID_SIZE_H

        # Проверка, свободна ли новая позиция
        if surface.world_grid[new_y][new_x] is None:
            # Освобождаем текущую позицию
            surface.world_grid[y][x] = None
            # Перемещаем бота на новую позицию
            surface.world_grid[new_y][new_x] = self
            self.position = new_x, new_y
            # Уменьшение количества еды бота за движение
            # Логика расхода энергии
            self.food -= func.normalize_value(temp, -15, 15, 50, 0)

        # Если куда хочет шагнуть клетка есть еда
        elif isinstance(surface.world_grid[new_y][new_x], objs.Food):
            # Освобождаем текущую позицию
            surface.world_grid[y][x] = None
            # Освобождаем позицию клетки с едой
            surface.world_grid[new_y][new_x] = None
            # Перемещаем бота на новую позицию
            surface.world_grid[new_y][new_x] = self
            self.position = (new_x, new_y)
            self.food += 1  # Логика расхода энергии
            dir_index = (
                self.ptr + 3 + func.normalize_value(self.food, 0, 1000, 1, 10)) % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)

        # Если куда хочет шагнуть клетка есть такая же клетка
        elif isinstance(surface.world_grid[new_y][new_x], BotGenome):
            dir_index = (self.ptr + 2) % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)

    # функция перемещения УТК
    def move_ptr_to(self):
        # Перемещение УТК к следующей команде на основе числа безусловного перехода
        self.ptr = (self.ptr + self.genome[self.ptr]) % len(self.genome)

    # функция перемещения указателя текущей команды
    def move_ptr(self):
        # Перемещения УТК к следующей команде
        self.ptr = (self.ptr + 1) % len(self.genome)

    # функция деления
    def reproduce(self):
        # Получаем список свободных позиций вокруг бота
        free_positions = func.get_free_adjacent_positions(
            self.position, surface.world_grid)

        if not free_positions:
            x, y = self.position
            # Удаление бота из сетки если Нет свободных позиций для размножения
            surface.world_grid[y][x] = None
            if random.random() < 0.1:
                # С шансом 10 процентов после смерти бота появляется органика (Если нету места для размножения)
                surface.world_grid[y][x] = objs.Food(self, x=x, y=y, food=100)
            return

        # Выбираем случайную свободную позицию для нового бота
        x, y = random.choice(free_positions)

        # Копируем геном родителя
        new_genome = self.genome.copy()

        # Проводим мутацию в геноме
        func.mutate_genome(new_genome)

        # Создаем нового бота с мутированным геномом
        new_color = (self.color[0], max(
            self.color[1] - 1, 90), 0)  # Смещаем цвета
        new_bot = BotGenome(food=self.food // 2, x=x, y=y,
                            color=new_color, genome=new_genome)  # Создание нового бота
        surface.world_grid[y][x] = new_bot  # Помещаем ннового бота в мир
        self.food //= 4  # Разделяем энергию между родительской и дочерней клетки

        # функция потребления еды взависимости от растояния и силы освещенности
    def food_consumption(self):
        x_obj, y_obj = self.position
        x_sun, y_sun = sun_coord
        # Вычисление расстояния между объектом и солнцем
        distance = np.sqrt((x_obj - x_sun)**2 + (y_obj - y_sun)**2)
        food_consumption = np.clip(
            (illumination / 2) + (100 / (distance + 1)), 0, 100)

        return int(food_consumption), int(distance)

    def is_this_temp(self):
        temp_index = (
            self.ptr + func.normalize_value(temp, -15, 15, 30, 0)) % len(self.genome)
        self.ptr = (self.ptr + self.genome[temp_index]) % len(self.genome)
        
    def command_view(self):
        move_dir_index = (self.ptr + 1) % len(self.genome)  # Индекс смещения
        # Выбираем направление на основе смещения взгляда
        move_dir = self.genome[move_dir_index] % len(cfg.move_directions)
        dx, dy = cfg.move_directions[move_dir]  # Получаем Направление
        # получаем точку куда мы смотрим
        x, y = self.position
        new_x = (x + dx) % cfg.GRID_SIZE_W
        new_y = (y + dy) % cfg.GRID_SIZE_H
        
        if surface.world_grid[new_y][new_x] is None:
            dir_index = (self.ptr + 2)  % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)

        elif isinstance(surface.world_grid[new_y][new_x], objs.Food):
            dir_index = (self.ptr + 43)  % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)

        elif isinstance(surface.world_grid[new_y][new_x], Cell):
            dir_index = (self.ptr + 59)  % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)

        elif isinstance(surface.world_grid[new_y][new_x], Predator):
            dir_index = (self.ptr + 24)  % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)

        

class Predator(BotGenome):
    def __init__(self, food=800, x=0, y=0, color=(255, 0, 0), genome=None):
        super().__init__(food, x, y, color, genome)
        
        # функция выполнения генома
    def execute_genome(self):
        # Проверка на смерть бота, если его пищи нет
        if self.food <= 0:  # Условие смерти клетки при отрецательной энергии
            x, y = self.position
            surface.world_grid[y][x] = None  # Удаление бота из сетки
        elif self.food >= 1000:  # Условие для деления клетки
            self.reproduce()
        elif self.food in range(1,1000):
            # За то что клетка думает она теряет энергию
            #self.food -= func.normalize_value(temp, -15, 15, 2, 1)
            command = self.genome[self.ptr]  # УТК
            self.execute_command(command)  # Выполнение команды генома (УТК)
        
    def execute_command(self, command):
        # Выполнение команды в зависимости от числа

        if command in range(0, 15):
            self.move()
        elif command == range(16, 30):
            self.how_many_food()
        elif command in range(31, 40):
            self.is_this_temp()
        elif command in range(41, 50):
            self.command_view()
        else:
            # Если у числа нет команды то происходит безусловный переход
            self.move_ptr_to()
        # Здесь могут быть другие команды....
        
    # функция движения клетки и проверки на столкновение
    def move(self):
        self.food -= func.normalize_value(temp, -15, 15, 40, 30)
        # Модификация для движения бота
        move_dir_index = (self.ptr + 1) % len(self.genome)  # Индекс смещения
        # Выбираем направление на основе смещения
        move_dir = self.genome[move_dir_index] % len(cfg.move_directions)
        dx, dy = cfg.move_directions[move_dir]  # Получаем Направление

        # Обновление позиции бота
        x, y = self.position
        new_x = (x + dx) % cfg.GRID_SIZE_W
        new_y = (y + dy) % cfg.GRID_SIZE_H

        # Проверка, свободна ли новая позиция
        if surface.world_grid[new_y][new_x] is None:
            # Освобождаем текущую позицию
            surface.world_grid[y][x] = None
            # Перемещаем бота на новую позицию
            surface.world_grid[new_y][new_x] = self
            self.position = new_x, new_y
            # Уменьшение количества еды бота за движение
            # Логика расхода энергии
            
        # Если куда хочет шагнуть клетка есть еда
        elif isinstance(surface.world_grid[new_y][new_x], objs.Food):
            # Освобождаем текущую позицию
            surface.world_grid[y][x] = None
            # Освобождаем позицию клетки с едой
            surface.world_grid[new_y][new_x] = None
            # Перемещаем бота на новую позицию
            surface.world_grid[new_y][new_x] = self
            self.position = new_x, new_y
            self.food += 1  # Логика расхода энергии
            dir_index = (self.ptr + 43)  % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)

        # Если куда хочет шагнуть клетка есть клетка
        elif isinstance(surface.world_grid[new_y][new_x], Cell):
            # Освобождаем текущую позицию
            surface.world_grid[y][x] = None
            # Освобождаем позицию клетки с едой
            surface.world_grid[new_y][new_x] = None
            # Перемещаем бота на новую позицию
            surface.world_grid[new_y][new_x] = self
            self.position = new_x, new_y
            self.food += 100  # Логика расхода энергии
            dir_index = (self.ptr + 24) % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)
        elif isinstance(surface.world_grid[new_x][new_y], Predator):
            dir_index = (self.ptr + 59) % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)

    # функция деления
    def reproduce(self):
        # Получаем список свободных позиций вокруг бота
        free_positions = func.get_free_adjacent_positions(
            self.position, surface.world_grid)

        if not free_positions:
            x, y = self.position
            # Удаление бота из сетки если Нет свободных позиций для размножения
            surface.world_grid[y][x] = None
            if random.random() < 0.1:
                # С шансом 10 процентов после смерти бота появляется органика (Если нету места для размножения)
                surface.world_grid[y][x] = objs.Food(self, x=x, y=y, food=100)
            return

        # Выбираем случайную свободную позицию для нового бота
        x, y = random.choice(free_positions)

        # Копируем геном родителя
        new_genome = self.genome.copy()

        # Проводим мутацию в геноме
        func.mutate_genome(new_genome)

        # Создаем нового бота с мутированным геномом
        new_color = (max(self.color[0] - 1, 90),0, 0)  # Смещаем цвета
        new_bot = Predator(food=self.food // 2, x=x, y=y,color=new_color, genome=new_genome)  # Создание нового бота
        surface.world_grid[y][x] = new_bot  # Помещаем ннового бота в мир
        self.food //= 4  # Разделяем энергию между родительской и дочерней клетки

class Cell(BotGenome):
    def __init__(self, food=500, x=0, y=0, color=(0, 255, 0), genome=None):
        super().__init__(food, x, y, color, genome)
        
    # функция движения клетки и проверки на столкновение
    def move(self):
        # Модификация для движения бота
        move_dir_index = (self.ptr + 1) % len(self.genome)  # Индекс смещения
        # Выбираем направление на основе смещения
        move_dir = self.genome[move_dir_index] % len(cfg.move_directions)
        dx, dy = cfg.move_directions[move_dir]  # Получаем Направление

        # Обновление позиции бота
        x, y = self.position
        new_x = (x + dx) % cfg.GRID_SIZE_W
        new_y = (y + dy) % cfg.GRID_SIZE_H

        # Проверка, свободна ли новая позиция
        if surface.world_grid[new_y][new_x] is None:
            # Освобождаем текущую позицию
            surface.world_grid[y][x] = None
            # Перемещаем бота на новую позицию
            surface.world_grid[new_y][new_x] = self
            self.position = new_x, new_y
            # Уменьшение количества еды бота за движение
            # Логика расхода энергии
            self.food -= func.normalize_value(temp, -15, 15, 50, 0)

        # Если куда хочет шагнуть клетка есть еда
        elif isinstance(surface.world_grid[new_y][new_x], objs.Food):
            # Освобождаем текущую позицию
            surface.world_grid[y][x] = None
            # Освобождаем позицию клетки с едой
            surface.world_grid[new_y][new_x] = None
            # Перемещаем бота на новую позицию
            surface.world_grid[new_y][new_x] = self
            self.position = (new_x, new_y)
            self.food += 1  # Логика расхода энергии
            dir_index = (self.ptr + 43 + int(func.normalize_value(self.food, 0, 1000, 1, 10))) % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)

        # Если куда хочет шагнуть клетка есть такая же клетка
        elif isinstance(surface.world_grid[new_y][new_x], Cell):
            dir_index = (self.ptr + 59) % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)
        
        elif isinstance(surface.world_grid[new_y][new_x],Predator):
            dir_index = (self.ptr + 24) % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)
            
        # функция деления
    def reproduce(self):
        # Получаем список свободных позиций вокруг бота
        free_positions = func.get_free_adjacent_positions(
            self.position, surface.world_grid)

        if not free_positions:
            x, y = self.position
            # Удаление бота из сетки если Нет свободных позиций для размножения
            surface.world_grid[y][x] = None
            if random.random() < 0.1:
                # С шансом 10 процентов после смерти бота появляется органика (Если нету места для размножения)
                surface.world_grid[y][x] = objs.Food(self, x=x, y=y, food=100)
            return

        # Выбираем случайную свободную позицию для нового бота
        x, y = random.choice(free_positions)

        # Копируем геном родителя
        new_genome = self.genome.copy()

        # Проводим мутацию в геноме
        func.mutate_genome(new_genome)

        # Создаем нового бота с мутированным геномом
        new_color = (self.color[0], max(
            self.color[1] - 1, 90), 0)  # Смещаем цвета
        new_bot = Cell(food=self.food // 2, x=x, y=y,
                            color=new_color, genome=new_genome)  # Создание нового бота
        surface.world_grid[y][x] = new_bot  # Помещаем ннового бота в мир
        self.food //= 4  # Разделяем энергию между родительской и дочерней клетки

