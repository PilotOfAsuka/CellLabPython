import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 5 # размер клетки изменяя этот параметр меняется масштаб
GRID_SIZE = WIDTH // CELL_SIZE
cycle_count = 0
max_temperature_change = 20  # Максимальное изменение температуры
base_temperature = 5  # Базовая температура

# словарь направлений
class Direction:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

move_actions = {
    Direction.UP: lambda: (0, -1),   # Вверх
    Direction.RIGHT: lambda: (1, 0), # Вправо
    Direction.DOWN: lambda: (0, 1),  # Вниз
    Direction.LEFT: lambda: (-1, 0), # Влево
}
#>>>>>>>>>>><<<<<<<<<<<

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bot Simulation')

# Цвета
BKG_color = (6, 189, 189)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FOOD_COLOR = (133,133,133)
MAX_CELL_SIZE = 20
MIN_CELL_SIZE = 10
START_NUMOFCELL = 20

# Класс BotGenome, определяющий поведение и свойства бота
class BotGenome:
    def __init__(self, genome_size=64, food = 500, x = 0, y = 0, color=(0, 255, 0)):
        # Инициализация генома с заданным размером
        self.genome = [random.randint(0, 63) for _ in range(genome_size)]
        self.ptr = 0  # УТК (указатель текущей команды)
        self.food = food
        self.position = (x, y)
        self.color = color

        # функция выполнения генома
    def execute_genome(self, occupied_positions, food_positions):
        self.food -= calculate_energy_cost(temperature, 10)
        command = self.genome[self.ptr]
        self.execute_command(command, occupied_positions, food_positions)

        # функция выполнений команд
    def execute_command(self, command,occupied_positions, food_positions):
        # Выполнение команды в зависимости от числа
        if command in range(10,24):
            self.photosynthesis()
        elif command in range(25,40):
            self.move(occupied_positions, food_positions)
        elif command == range(1,9):
            self.how_many_food()
        else: 
            self.move_ptr_to()
        # Здесь могут быть другие команды....
        
        # функция фотосинтеза
    def photosynthesis(self):
        light_intensity = get_light_intensity(self.position[1])
        self.food += 5 * light_intensity  # Увеличиваем энергию в зависимости от интенсивности света
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
    
    def move(self, occupied_positions, food_positions):
        # Модификация для движения бота
        move_dir_index = (self.ptr + 1) % len(self.genome)
        move_dir = self.genome[move_dir_index] % 4  # Теперь у нас только 4 направления
        dx, dy = move_actions.get(move_dir, lambda: (0, 0))()  # Получаем смещение
        self.food -= calculate_energy_cost(temperature, 10)

        # Обновление позиции бота
        x, y = self.position
        new_x, new_y = ((x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE)

        # Проверяем, свободна ли новая позиция
        if (new_x, new_y) not in occupied_positions:
            # Обновляем позиции в словаре
            del occupied_positions[(x, y)]
            occupied_positions[(new_x, new_y)] = self
            self.position = new_x, new_y
            # Проверяем наличие еды и обновляем уровень энергии
            if (new_x, new_y) in food_positions:
                self.food += 1
                print("Поглотил еду")
                food_positions.remove((new_x, new_y))
            dir_index = (self.ptr + 2) % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)
            
        else:
            dir_index = (self.ptr + 3) % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)

            
        # функция поворота (НЕреализованно)
    def rotate(self):
        rotate_dir_index = (self.ptr + 1) % len(self.genome)
        rotate_dir = self.genome[rotate_dir_index] % 8
        # Пример команды "Rotate"
        #print(f"Бот повернулся на {rotate_dir} ")
        return(rotate_dir)

        # функция перемещения УТК
    def move_ptr_to(self):
        # Перемещение УТК к следующей команде
        self.ptr = (self.ptr + self.genome[self.ptr]) % len(self.genome)

        # функция перемещения указателя текущей команды
    def move_ptr(self):
        # Перемещения УТК к следующей команде
        self.ptr = (self.ptr + 1) % len(self.genome)

        # функция мутации
    def mutate(self, position, new_value):
        self.genome[position] = new_value
        
        
        # функция деления
    def reproduce(self, bots):

        # Получаем список свободных позиций вокруг бота
        free_positions = self.get_free_adjacent_positions(occupied_positions)

        if not free_positions:
            return None  # Нет свободных позиций для размножения

        # Выбираем случайную свободную позицию для нового бота
        new_position = random.choice(free_positions)

        # Создаем нового бота в выбранной позиции
        red_component = max(0, min(255, int(temperature * 10)))
        new_color = (red_component, max(self.color[1] - 10, 0), 0)  # Новый цвет для бота
        new_bot = BotGenome(genome_size=len(self.genome), food=self.food // 2, x=new_position[0], y=new_position[1], color=new_color)
        self.food //= 2  # Делим энергию между родителем и потомком
        return new_bot


        # функция получения свободного места вокруг
    def get_free_adjacent_positions(self, occupied_positions):
        adjacent_positions = [
            ((self.position[0] + dx) % GRID_SIZE, (self.position[1] + dy) % GRID_SIZE)
            for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)
        ]
        return [pos for pos in adjacent_positions if pos not in occupied_positions]
        # функция проверки свободного места
        
    def is_space_to_reproduce(self, occupied_positions):
        # Вычисляем соседние позиции
        adjacent_positions = [
            ((self.position[0] + dx) % GRID_SIZE, (self.position[1] + dy) % GRID_SIZE)
            for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)
        ]
        # Проверяем, есть ли хотя бы одна свободная позиция
        return any(pos not in occupied_positions for pos in adjacent_positions)



#>>>>>>отдельные функции<<<<<<<<<
# функция расчёта потребления энергии от температуры
def calculate_energy_cost(temperature, base_energy_cost):
    optimal_temperature = 5  # Оптимальная температура
    if temperature >= optimal_temperature:
        # Энергозатраты увеличиваются с понижением температуры ниже оптимальной
        energy_cost_multiplier = 1 + (optimal_temperature - temperature) * 0.05
    else:
        # Энергозатраты увеличиваются ещё сильнее при очень низких температурах
        energy_cost_multiplier = 1 + (optimal_temperature - temperature) * 0.5

    return base_energy_cost * energy_cost_multiplier

# Функция для обновления температуры
def update_temperature(cycle_count):
    global temperature
    # Изменяем температуру по синусоиде
    temperature = base_temperature + max_temperature_change * math.sin(math.radians(cycle_count))
    temperature = int(temperature)
    return temperature

def draw_bot_count(bots):
    count_text = font.render(f'Количество клеток: {len(bots)}', True, BLACK)
    screen.blit(count_text, (10, 30))  # Меняйте положение текста при необходимости

# функция отрисовки еды
def draw_food_cells(food_position):
    for pos in food_position:
        rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, FOOD_COLOR, rect) # FOOD_COLOR - цвет еды

# функция отрисовки клеток
def draw_bots(bots):
    for bot in bots:
        x, y = bot.position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, bot.color, rect)

# функция интенсивности света
def get_light_intensity(y):
    # интенсивность уменьшается от верха к низу
    return max(1, GRID_SIZE - y)

font = pygame.font.SysFont(None, 24)  # Выберите подходящий шрифт и размер

# функция подсчета циклов
def draw_cycle_count(cycle_count):
    text = font.render(f'Циклов: {cycle_count}', True, BLACK)
    screen.blit(text, (10, 10))  # Размещение текста в левом верхнем углу

# функция подсчета темпeратуры
def draw_temp_count(temperature):
    text = font.render(f'Темпeратура: {temperature}', True, BLACK)
    screen.blit(text, (10, 50))  # Размещение текста в левом верхнем углу

# функция генерации позиции еды зависищая от высоты
def generate_food_position(width, height):
    x = random.randint(0, width - 1)
    if random.random() < 0.7:  # 70% вероятность
        y = random.randint(height // 2, height - 1)  # Нижняя половина
    else:
        y = random.randint(0, height // 2 - 1)  # Верхняя половина
    return x, y

# Создание нескольких ботов
bots = [BotGenome(x=random.randint(0, GRID_SIZE - 1), y=random.randint(0, GRID_SIZE - 1)) for _ in range(START_NUMOFCELL)]
food_cells = []
new_bots = []
food_positions = ()


# Основной цикл игры
while True:
    food_positions = set(food_cells)
    update_temperature(cycle_count)  # Обновляем температуру

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # Фильтрация ботов с энергией >= 0
    bots = [bot for bot in bots if bot.food >= 0]
           
    # Обновление словаря занятых позиций после удаления ботов
    occupied_positions = {(bot.position[0], bot.position[1]): bot for bot in bots}
    
    # Обновляем состояние каждого бота и фильтруем тех, кто может размножаться
    # Генератор для активных ботов, которые могут двигаться и размножаться
    active_bots = (bot for bot in bots if bot.food >= 0 and bot.is_space_to_reproduce(occupied_positions))

    for bot in active_bots:
        bot.execute_genome(occupied_positions, food_positions)

        # Если бот готов к размножению, пытаемся создать нового бота
        if bot.food > 1000:
            new_bot = bot.reproduce(occupied_positions)
            if new_bot:
                new_bots.append(new_bot)
                occupied_positions[new_bot.position] = new_bot

    # Случайное появление еды
    if random.random() < 0.3:  # 30% вероятность
        food_position = generate_food_position(GRID_SIZE - 1, GRID_SIZE - 1)
        # Убедимся, что еда не появляется на занятой клетке
        if food_position not in occupied_positions and food_position not in food_cells:
            food_cells.append(food_position)


    # В конце основного игрового цикла
    bots.extend(new_bots)  # Добавляем новых ботов в основной список
    new_bots.clear()       # Очищаем список новых ботов для следующего цикла

    

   
    food_positions = set(food_cells)
    # Обновление дисплея
    screen.fill(BKG_color)
    draw_bots(bots)
    draw_food_cells(food_positions)
    cycle_count += 1
    draw_cycle_count(cycle_count)
    draw_bot_count(bots)
    draw_temp_count(temperature)
    pygame.display.flip()
    print(f'Цикл номер: {cycle_count}')
    pygame.time.delay(0)  # Задержка в 100 миллисекунд


