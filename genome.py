import random
import configs as cfg
import func
import objects as objs
gen_size = 64 #Размер гена

# Класс BotGenome, определяющий поведение и свойства бота
class BotGenome:
    def __init__(self, world, food = 700, x = 0, y = 0, color=(0, 255, 0), genome=None):
        # Инициализация генома с заданным размером
        self.world = world
        self.genome = [random.randint(0, 63) for _ in range(gen_size)] if genome is None else genome
        self.ptr = 0  # УТК (указатель текущей команды)
        self.food = food
        self.position = x, y
        self.color = color
    MAX_ENERGY = 1600  # Максимальный уровень энергии для бота

        # функция выполнения генома
    def execute_genome(self):
        self.food -= 5
        command = self.genome[self.ptr]
        self.execute_command(command)
        # Проверка на смерть бота, если его пищи нет
        if self.food < 0:
            x, y = self.position
            cfg.world_grid[y][x] = None  # Удаление бота из сетки
        if self.food >= 1500:
            self.reproduce()
        
        # функция выполнений команд
    def execute_command(self, command):
        # Выполнение команды в зависимости от числа
        if command in range(10,20):
            self.photosynthesis()
        elif command in range(21,35):
            self.move()
        elif command == range(1,9):
            self.how_many_food()
        else: 
            self.move_ptr_to()
        # Здесь могут быть другие команды....
        
    def photosynthesis(self):
        self.food += 100
        self.food = min(self.food, self.MAX_ENERGY)  # Ограничиваем максимальное количество энергии
        self.move_ptr()
    
        # функция команды "сколько у меня еды"
    def how_many_food(self):
        food_index = (self.ptr + 1) % len(self.genome)
        next_ptr_index = (self.ptr + 2) % len(self.genome)
        next_next_ptr_index = (self.ptr + 3) % len(self.genome)
        food_genome = self.genome[food_index] * 15

        if self.food >= food_genome:
            self.ptr = (self.ptr + self.genome[next_ptr_index]) % len(self.genome)
        else:
            self.ptr = (self.ptr + self.genome[next_next_ptr_index]) % len(self.genome)
            
    # функция движения клетки и проверки на столкновение
    def move(self):
        # Модификация для движения бота
        move_dir_index = (self.ptr + 1) % len(self.genome) # Индекс смещения
        move_dir = self.genome[move_dir_index] % len(cfg.move_actions) # Выбираем направление на основе смещения
        dx, dy = cfg.move_actions[move_dir]  # Получаем Направление
        
        # Обновление позиции бота
        x, y = self.position
        new_x = (x + dx) % cfg.GRID_SIZE_W
        new_y = y + dy if -1 < y + dy < cfg.GRID_SIZE_H else y

            # Проверка, свободна ли новая позиция
        if cfg.world_grid[new_y][new_x] is None:
            # Освобождаем текущую позицию
            cfg.world_grid[y][x] = None

            # Перемещаем бота на новую позицию
            cfg.world_grid[new_y][new_x] = self
            self.position = (new_x, new_y)

            # Уменьшение количества еды бота за движение
            self.food -= 10
        elif isinstance(cfg.world_grid[new_y][new_x], objs.Food):
            # Освобождаем текущую позицию
            cfg.world_grid[y][x] = None
            # Освобождаем позицию клетки с едой
            cfg.world_grid[new_y][new_x] = None 
            # Перемещаем бота на новую позицию
            cfg.world_grid[new_y][new_x] = self
            self.position = (new_x, new_y)
            self.food += 1
            dir_index = (self.ptr + 3) % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)
            
        elif isinstance(cfg.world_grid[new_y][new_x], BotGenome):
                dir_index = (self.ptr + 2) % len(self.genome)
                self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)
                
        # функция перемещения УТК
    def move_ptr_to(self):
        # Перемещение УТК к следующей команде
        self.ptr = (self.ptr + self.genome[self.ptr]) % len(self.genome)

        # функция перемещения указателя текущей команды
    def move_ptr(self):
        # Перемещения УТК к следующей команде
        self.ptr = (self.ptr + 1) % len(self.genome)
        
        # функция деления
    def reproduce(self):
        # Получаем список свободных позиций вокруг бота
        free_positions = func.get_free_adjacent_positions(self.position)

        if not free_positions:
            x, y = self.position
            cfg.world_grid[y][x] = None# Удаление бота из сетки если Нет свободных позиций для размножения
            if random.random() < 0.2:
                cfg.world_grid[y][x] = objs.Food(self, x=x,y=y,food=100)
            return
        # Выбираем случайную свободную позицию для нового бота
        x, y = random.choice(free_positions)

        # Копируем геном родителя
        new_genome = self.genome.copy()

        # Проводим мутацию в геноме
        func.mutate_genome(new_genome)

        # Создаем нового бота с мутированным геномом
        new_color = (self.color[0], max(self.color[1] - 1, 90), 0)
        new_bot = BotGenome(self.world, food=self.food // 2, x=x, y=y, color=new_color, genome=new_genome)
        cfg.world_grid[y][x] = new_bot
        self.food //= 4
        