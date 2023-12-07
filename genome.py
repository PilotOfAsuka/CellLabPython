import random
import configs as cfg
import func
import objects as objs
import surface
import numpy as np

temp, illumination, sun_coord = 0,0,(0,0)
# Класс BotGenome, определяющий поведение и свойства бота
class BotGenome:
    def __init__(self, food = 500, x = 0, y = 0, color=(0, 255, 0), genome=None):
        # Инициализация генома с заданным размером
        self.genome = [random.randint(0, 63) for _ in range(cfg.gen_size)] if genome is None else genome
        self.ptr = 0  # УТК (указатель текущей команды)
        self.food = food
        self.position = x, y
        self.color = color
    MAX_ENERGY = 1100  # Максимальный уровень энергии для бота

    # функция выполнения генома
    def execute_genome(self):
        # Проверка на смерть бота, если его пищи нет
        if self.food < 0: # Условие смерти клетки при отрецательной энергии
            x, y = self.position
            surface.world_grid[y][x] = None  # Удаление бота из сетки
        if self.food >= 1000: # Условие для деления клетки
            self.reproduce() 
            
        self.food -= func.normalize_value(temp,-15,15, 20,10) # За то что клетка думает она теряет энергию
        command = self.genome[self.ptr] # УТК
        self.execute_command(command) # Выполнение команды генома (УТК)

        
        # функция выполнений команд
    def execute_command(self, command):
        # Выполнение команды в зависимости от числа
        if command in range(10,20):
            self.photosynthesis()
        elif command in range(21,25):
            self.move()
        elif command == range(1,9):
            self.how_many_food()
        else:
            # Если у числа нет команды то происходит безусловный переход 
            self.move_ptr_to()
        # Здесь могут быть другие команды....
        
    # Функция фотосинтеза   
    def photosynthesis(self):
        self.food += func.normalize_value(self.food_consumption(),0, 100, 20, 70) + func.normalize_value(temp, -15,15,-10,20)# Логика получения энергии при фотосинтезе
        self.food = min(self.food, self.MAX_ENERGY)  # Ограничиваем максимальное количество энергии
        self.move_ptr()# Переход УТК 
    
    # Функция команды "Сколько у меня еды?"
    def how_many_food(self):
        food_index = (self.ptr + 1) % len(self.genome) # Получаем смещение
        next_ptr_index = (self.ptr + 2) % len(self.genome)
        next_next_ptr_index = (self.ptr + 3) % len(self.genome)
        food_genome = self.genome[food_index] * 15 # Получаем условие перехода 

        if self.food >= food_genome:
            self.ptr = (self.ptr + self.genome[next_ptr_index]) % len(self.genome)# Если условие перехода меньше количеста собственной энергии
        else:
            self.ptr = (self.ptr + self.genome[next_next_ptr_index]) % len(self.genome)# Если условие перехода больше количеста собственной энергии
            
    # функция движения клетки и проверки на столкновение
    def move(self):
        # Модификация для движения бота
        move_dir_index = (self.ptr + 1) % len(self.genome) # Индекс смещения
        move_dir = self.genome[move_dir_index] % len(cfg.move_directions) # Выбираем направление на основе смещения
        dx, dy = cfg.move_directions[move_dir]  # Получаем Направление
        
        # Обновление позиции бота
        x, y = self.position
        new_x = (x + dx) % cfg.GRID_SIZE_W
        new_y = y + dy if -1 < y + dy < cfg.GRID_SIZE_H else y

            # Проверка, свободна ли новая позиция
        if surface.world_grid[new_y][new_x] is None:
            # Освобождаем текущую позицию
            surface.world_grid[y][x] = None
            # Перемещаем бота на новую позицию
            surface.world_grid[new_y][new_x] = self
            self.position = new_x, new_y
            # Уменьшение количества еды бота за движение
            self.food -= func.normalize_value(temp,-15,15, 50,0)# Логика расхода энергии
            
        elif isinstance(surface.world_grid[new_y][new_x], objs.Food):# Если куда хочет шагнуть клетка есть еда
            # Освобождаем текущую позицию
            surface.world_grid[y][x] = None
            # Освобождаем позицию клетки с едой
            surface.world_grid[new_y][new_x] = None 
            # Перемещаем бота на новую позицию
            surface.world_grid[new_y][new_x] = self
            self.position = (new_x, new_y)
            self.food += 1 # Логика расхода энергии
            dir_index = (self.ptr + 3) % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)
            
        elif isinstance(surface.world_grid[new_y][new_x], BotGenome):# Если куда хочет шагнуть клетка есть такая же клетка
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
        free_positions = func.get_free_adjacent_positions(self.position, surface.world_grid)

        if not free_positions:
            x, y = self.position
            surface.world_grid[y][x] = None# Удаление бота из сетки если Нет свободных позиций для размножения
            if random.random() < 0.2:
                surface.world_grid[y][x] = objs.Food(self, x=x,y=y,food=100) # С шансом 20 процентов после смерти бота появляется органика (Если нету места для размножения) 
            return
        
        # Выбираем случайную свободную позицию для нового бота
        x, y = random.choice(free_positions)

        # Копируем геном родителя
        new_genome = self.genome.copy()

        # Проводим мутацию в геноме
        func.mutate_genome(new_genome)

        # Создаем нового бота с мутированным геномом
        new_color = (self.color[0], max(self.color[1] - 1, 90), 0)# Смещаем цвета
        new_bot = BotGenome(food=self.food // 2, x=x, y=y, color=new_color, genome=new_genome)# Создание нового бота
        surface.world_grid[y][x] = new_bot # Помещаем ннового бота в мир 
        self.food //= 2 # Разделяем энергию между родительской и дочерней клетки  
        
        # функция потребления еды взависимости от растояния и силы освещенности
    def food_consumption(self):
        x_obj, y_obj = self.position
        x_sun, y_sun = sun_coord
        # Вычисление расстояния между объектом и солнцем
        distance = np.sqrt((x_obj - x_sun)**2 + (y_obj - y_sun)**2)
        food_consumption = np.clip((illumination / 2) + (100 / (distance + 1)), 0, 200)

        return int(food_consumption)