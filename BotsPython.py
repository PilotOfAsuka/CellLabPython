import pygame
import sys
import random
import math
import copy

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 4 # размер клетки изменяя этот параметр меняется масштаб
GRID_SIZE = WIDTH // CELL_SIZE
cycle_count = 0
max_temperature_change = 20  # Максимальное изменение температуры
base_temperature = 10  # Базовая температура
START_NUMOFCELL = 20 # Количество начальных клеток
Gen_size = 64 #Размер гена
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


# Класс BotGenome, определяющий поведение и свойства бота
class BotGenome:
    def __init__(self, food = 500, x = 0, y = 0, color=(0, 255, 0), genome=[random.randint(0, 63) for _ in range(Gen_size)]):
        # Инициализация генома с заданным размером
        self.genome = genome
        self.ptr = 0  # УТК (указатель текущей команды)
        self.food = food
        self.position = (x, y)
        self.color = color
    MAX_ENERGY = 2100  # Максимальный уровень энергии для бота

        # функция выполнения генома
    def execute_genome(self, world_grid):
        self.food -= calculate_energy_cost(temperature, 15)
        command = self.genome[self.ptr]
        self.execute_command(command, world_grid)
        # Проверка на смерть бота, если его пищи нет
        if self.food < 0:
            x, y = self.position
            world_grid[y][x] = None  # Удаление бота из сетки
        if self.food >= 2000:
            self.reproduce(world_grid)

        # функция выполнений команд
    def execute_command(self, command,world_grid):
        # Выполнение команды в зависимости от числа
        if command in range(10,24):
            self.photosynthesis()
        elif command in range(25,30):
            self.move(world_grid)
        elif command == range(1,9):
            self.how_many_food()
        else: 
            self.move_ptr_to()
        # Здесь могут быть другие команды....
        
        # функция фотосинтеза
    def photosynthesis(self):
        light_intensity = get_light_intensity(self.position[1], cycle_count)
        self.food += 1 * light_intensity   # Увеличиваем энергию в зависимости от интенсивности света
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
    
    def move(self,world_grid):
        # Модификация для движения бота
        move_dir_index = (self.ptr + 1) % len(self.genome)
        move_dir = self.genome[move_dir_index] % 4  # Теперь у нас только 4 направления
        dx, dy = move_actions.get(move_dir, lambda: (0, 0))()  # Получаем смещение
        self.food -= calculate_energy_cost(temperature, 10)

        # Обновление позиции бота
        x, y = self.position
        new_x, new_y = ((x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE)

            # Проверка, свободна ли новая позиция
        if world_grid[new_y][new_x] is None:
            # Освобождаем текущую позицию
            world_grid[y][x] = None

            # Перемещаем бота на новую позицию
            self.position = (new_x, new_y)
            world_grid[new_y][new_x] = self

            # Уменьшение количества еды бота за движение
            self.food -= 10  # логика расхода энергии
            
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

        # функция мутации
    def mutate_genome(self, genome):
        mutation_chance = 0.05  # Шанс мутации для каждого гена
        for i in range(len(genome)):
            if random.random() < mutation_chance:
                genome[i] = random.randint(0, 63)  # Новое случайное значение гена
        
        
        # функция деления
    def reproduce(self, world_grid):
        # Получаем список свободных позиций вокруг бота
        free_positions = self.get_free_adjacent_positions(world_grid)

        if not free_positions:
            self.food -= 500 # Нет свободных позиций для размножения
            return
        # Выбираем случайную свободную позицию для нового бота
        new_position = random.choice(free_positions)
        x, y = new_position

        # Копируем геном родителя
        new_genome = copy.deepcopy(self.genome)

        # Проводим мутацию в геноме
        self.mutate_genome(new_genome)

        # Создаем нового бота с мутированным геномом
        red_component = max(0, min(255, int(temperature * 5)))
        new_color = (red_component, max(self.color[1] - 10, 0), 0)
        new_bot = BotGenome(food=self.food // 2, x=x, y=y, color=new_color, genome=new_genome)
        world_grid[y][x] = new_bot
        self.food //= 4

        # функция получения свободного места вокруг
    def get_free_adjacent_positions(self, world_grid):
        x, y = self.position
        free_positions = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE
                if world_grid[ny][nx] is None:
                    free_positions.append((nx, ny))
        return free_positions




#>>>>>>отдельные функции<<<<<<<<<
# функция расчёта потребления энергии от температуры
def calculate_energy_cost(temperature, base_energy_cost):
    optimal_temperature = 20  # Оптимальная температура
    if temperature >= optimal_temperature:
        # Энергозатраты увеличиваются с понижением температуры ниже оптимальной
        energy_cost_multiplier = (optimal_temperature - temperature) * 0.03
    else:
        # Энергозатраты увеличиваются ещё сильнее при очень низких температурах
        energy_cost_multiplier = (optimal_temperature - temperature) * 0.05

    return base_energy_cost * energy_cost_multiplier

# функция получения сезона
def draw_season_info(season):
    season_text = font.render(f'Сезон: {season}', True, WHITE)
    screen.blit(season_text, (10, 70))  # Поместите текст в нужное место на экране
def get_current_season(cycle_count, season_length=450):
    season_phase = (cycle_count % season_length) / season_length
    if 0 <= season_phase < 0.25:
        return "Весна"
    elif 0.25 <= season_phase < 0.5:
        return "Лето"
    elif 0.5 <= season_phase < 0.75:
        return "Осень"
    else:
        return "Зима"
    
# Функция для обновления температуры
def update_temperature(cycle_count):
    global temperature
    season_length = 450  # Длина сезонного цикла
    season_phase = (cycle_count % season_length) / season_length
    seasonal_temperature_variation = max_temperature_change * math.sin(season_phase * 2 * math.pi)  # Сезонное изменение температуры
    temperature = base_temperature + seasonal_temperature_variation
    temperature = int(temperature)
    return temperature


def draw_bot_count(bots):
    count_text = font.render(f'Количество клеток: {len(bots)}', True, WHITE)
    screen.blit(count_text, (10, 30))  # Меняйте положение текста при необходимости

        
# Функция отрисовки бота
def draw_bot(bot):
    x, y = bot.position
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, bot.color, rect)
    
# функция отрисовки клеток
def draw_bots(bots):
    for bot in bots:
        x, y = bot.position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, bot.color, rect)

# функция интенсивности света
def get_light_intensity(y, cycle_count):
    season_length = 450  # Длина сезонного цикла
    season_phase = (cycle_count % season_length) / season_length
    season_intensity = math.sin(season_phase * 1 * math.pi)  # Синусоидальная функция для имитации сезонов
    vertical_intensity = max(1, GRID_SIZE - y)  # Изначальная логика
    return vertical_intensity * (0.5 * season_intensity + 0.5)


font = pygame.font.SysFont(None, 24)  # Выберите подходящий шрифт и размер

# функция подсчета циклов
def draw_cycle_count(cycle_count):
    text = font.render(f'Циклов: {cycle_count}', True, WHITE)
    screen.blit(text, (10, 10))  # Размещение текста в левом верхнем углу

# функция подсчета темпeратуры
def draw_temp_count(temperature):
    text = font.render(f'Темпeратура: {temperature}', True, WHITE)
    screen.blit(text, (10, 50))  # Размещение текста в левом верхнем углу

# Инициализация двумерного массива мира
world_grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Функция для генерации случайной свободной позиции
def random_position(world_grid):
    x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
    while world_grid[y][x] is not None:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
    return x, y

for _ in range(START_NUMOFCELL):
    x, y = random_position(world_grid)
    bot = BotGenome(x=x, y=y)
    world_grid[y][x] = bot
    
# Основной цикл
while True:
    update_temperature(cycle_count)  # Обновляем температуру
    current_season = get_current_season(cycle_count) #Обновляем сезон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # Обновление состояния каждого бота
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            bot = world_grid[y][x]
            if bot is not None:
                bot.execute_genome(world_grid)
                
    # Обновление дисплея
    screen.fill(BKG_color)
    
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            bot = world_grid[y][x]
            if bot is not None:
                draw_bot(bot)
                
    cycle_count += 1
    draw_cycle_count(cycle_count)
    draw_temp_count(temperature)
    draw_season_info(current_season)
    pygame.display.flip()
    print(f'Цикл номер: {cycle_count}')
    pygame.time.delay(100)  # Задержка в 100 миллисекунд
