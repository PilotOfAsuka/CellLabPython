import pygame
import sys
import random
import math
import copy

# функция мутации
def mutate_genome(genome):
    mutation_chance = 0.05  # Шанс мутации для каждого гена
    for i in range(len(genome)):
        if random.random() < mutation_chance:
            genome[i] = random.randint(0, 63)  # Новое случайное значение гена
            
# Инициализация Pygame И его составляющих
pygame.init()
font = pygame.font.SysFont(None, 24)  # Выберите подходящий шрифт и размер

# Константы
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 2 # размер клетки изменяя этот параметр меняется масштаб
GRID_SIZE_W = WIDTH // CELL_SIZE
GRID_SIZE_H = HEIGHT // CELL_SIZE
cycle_count = 0
max_temperature_change = 15  # Максимальное изменение температуры
base_temperature = 5  # Базовая температура
START_NUM_OF_CELL = 30 # Количество начальных клеток
Gen_size = 64 #Размер гена

# кортеж направлений
move_actions = (
    (0, -1),  # Вверх
    (1, 0),  # Вправо
    (0, 1),  # Вниз
    (-1, 0)  # Влево
)

#>>>>>>>>>>><<<<<<<<<<<

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bot Simulation')

# Цвета
BKG_color = (6, 189, 189)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FOOD_COLOR = (133,133,133)

class Food:
    def __init__(self, world, food=0, x = 0, y = 0, color=FOOD_COLOR):
        self.world = world
        self.food = food
        self.color = color
        self.position = (x, y)
    
# Класс BotGenome, определяющий поведение и свойства бота
class BotGenome:
    def __init__(self, world, food = 500, x = 0, y = 0, color=(0, 255, 0), genome=[random.randint(0, 63) for _ in range(Gen_size)]):
        # Инициализация генома с заданным размером
        self.world = world
        self.genome = genome
        self.ptr = 0  # УТК (указатель текущей команды)
        self.food = food
        self.position = (x, y)
        self.color = color
    MAX_ENERGY = 2100  # Максимальный уровень энергии для бота

        # функция выполнения генома
    def execute_genome(self):
        self.food -= calculate_energy_cost(self.world.temperature, 15)
        command = self.genome[self.ptr]
        self.execute_command(command)
        # Проверка на смерть бота, если его пищи нет
        if self.food < 0:
            x, y = self.position
            self.world.world_grid[y][x] = None  # Удаление бота из сетки
        if self.food >= 2000:
            self.reproduce()

        # функция выполнений команд
    def execute_command(self, command):
        # Выполнение команды в зависимости от числа
        if command in range(10,24):
            self.photosynthesis()
        elif command in range(25,30):
            self.move()
        elif command == range(1,9):
            self.how_many_food()
        else: 
            self.move_ptr_to()
        # Здесь могут быть другие команды....
        
        # функция фотосинтеза
    def photosynthesis(self):
        self.food += int(get_light_intensity(self.position[1], self.world.cycle_count))
        
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
        move_dir_index = (self.ptr + 1) % len(self.genome)
        move_dir = self.genome[move_dir_index] % 4  # Теперь у нас только 4 направления
        dx, dy = move_actions[move_dir]  # Получаем смещение

        # Обновление позиции бота
        x, y = self.position
        new_x = (x + dx) % GRID_SIZE_W
        new_y = y + dy if -1 < y + dy < GRID_SIZE_H else y

            # Проверка, свободна ли новая позиция
        if self.world.world_grid[new_y][new_x] is None:
            # Освобождаем текущую позицию
            self.world.world_grid[y][x] = None

            # Перемещаем бота на новую позицию
            self.position = (new_x, new_y)
            self.world.world_grid[new_y][new_x] = self
            # Уменьшение количества еды бота за движение
            self.food -= calculate_energy_cost(self.world.temperature, 15)  # логика расхода энергии
            
        elif isinstance(self.world.world_grid[new_y][new_x], Food):
            # Освобождаем текущую позицию
            self.world.world_grid[y][x] = None
            # Перемещаем бота на новую позицию
            self.world.world_grid[new_y][new_x] = self
            self.position = (new_x, new_y)
            # Увеличение энергии за еду (class Food)
            self.food += 100  # логика расхода энергии  

            
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
        free_positions = self.get_free_adjacent_positions()

        if not free_positions:
            x, y = self.position
            self.world.world_grid[y][x] = None # Удаление бота из сетки если Нет свободных позиций для размножения
            if random.random() < 0.2:
                self.world.world_grid[y][x] = Food(self, x=x,y=y,food=100)
            return
        # Выбираем случайную свободную позицию для нового бота
        x, y = random.choice(free_positions)

        # Копируем геном родителя
        new_genome = self.genome.copy()

        # Проводим мутацию в геноме
        mutate_genome(new_genome)

        # Создаем нового бота с мутированным геномом
        new_color = (0, max(self.color[1] - 5, 0), 0)
        new_bot = BotGenome(self.world, food=self.food // 2, x=x, y=y, color=new_color, genome=new_genome)
        self.world.world_grid[y][x] = new_bot
        self.food //= 4

        # функция получения свободного места вокруг
    def get_free_adjacent_positions(self):
        x, y = self.position
        free_positions = []
        for dx, dy in (
                (-1, -1),
                (0, -1),
                (1, -1),
                (1, 0),
                (1, 1),
                (0, 1),
                (-1, 1),
                (-1, 0),
        ):
            nx = (x + dx) % GRID_SIZE_W
            ny = y + dy if -1 < y + dy < GRID_SIZE_H else y
            if self.world.world_grid[ny][nx] is None:
                free_positions.append((nx, ny))
        return free_positions

# >>>>>>отдельные функции<<<<<<<<<
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


# функция интенсивности света
def get_light_intensity(y, cycle_count, season_length=450):
    season_phase = cycle_count / season_length % 1
    season_intensity = math.sin(season_phase * 1 * math.pi)  # Синусоидальная функция для имитации сезонов
    vertical_intensity = max(1, GRID_SIZE_H - y)  # Изначальная логика
    return vertical_intensity * (0.2 * season_intensity + 0.2)


# Функция для генерации случайной свободной позиции
def random_position(world_grid):
    x = random.randint(0, GRID_SIZE_W - 1)
    y = random.randint(0, GRID_SIZE_H - 1)
    while world_grid[y][x] is not None:
        x = random.randint(0, GRID_SIZE_W - 1)
        y = random.randint(0, GRID_SIZE_H - 1)
    return x, y

class World:
    temperature = base_temperature
    cycle_count = 0
    season = ''

    def __init__(self, screen):
        self.screen = screen
        # Инициализация двумерного массива мира
        self.world_grid = [[None for _ in range(GRID_SIZE_W)] for _ in range(GRID_SIZE_H)]
        for _ in range(START_NUM_OF_CELL):
            x, y = random_position(self.world_grid)
            bot = BotGenome(self, x=x, y=y)
            self.world_grid[y][x] = bot

    def get_current_season(self, season_length=450):
        season_phase = self.cycle_count / season_length % 1
        if 0 <= season_phase < 0.25:
            return "Весна"
        elif 0.25 <= season_phase < 0.5:
            return "Лето"
        elif 0.5 <= season_phase < 0.75:
            return "Осень"
        else:
            return "Зима"

    # Функция для обновления температуры
    def update_temperature(self):
        season_length = 450  # Длина сезонного цикла
        season_phase = (self.cycle_count % season_length) / season_length
        seasonal_temperature_variation = max_temperature_change * math.sin(
            season_phase * 2 * math.pi)  # Сезонное изменение температуры
        self.temperature = int(base_temperature + seasonal_temperature_variation)

    def update(self):
        
        self.update_temperature()  # Обновляем температуру
        self.season = self.get_current_season()  # Обновляем сезон
        # Обновление состояния каждого бота
        for y in range(GRID_SIZE_H):
            for x in range(GRID_SIZE_W):
                obj = self.world_grid[y][x]
                if isinstance(obj, BotGenome):
                    obj.execute_genome()
        self.cycle_count += 1

    # Функция отрисовки бота
    def draw_bot(self, bot):
        x, y = bot.position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, bot.color, rect)

    # функция подсчета циклов
    def draw_cycle_count(self):
        text = font.render(f'Циклов: {self.cycle_count}', True, WHITE)
        self.screen.blit(text, (10, 10))  # Размещение текста в левом верхнем углу

    # функция подсчета температуры
    def draw_temp_count(self):
        text = font.render(f'Темпeратура: {self.temperature}', True, WHITE)
        self.screen.blit(text, (10, 50))  # Размещение текста в левом верхнем углу

    def draw_bot_count(self, count):
        count_text = font.render(f'Количество клеток: {count}', True, WHITE)
        self.screen.blit(count_text, (10, 30))  # Меняйте положение текста при необходимости

    # функция получения сезона
    def draw_season_info(self):
        season_text = font.render(f'Сезон: {self.season}', True, WHITE)
        self.screen.blit(season_text, (10, 70))  # Поместите текст в нужное место на экране

    def draw(self):
        # Отрисовка ботов
        count_of_bots = 0
        for y in range(GRID_SIZE_H):
            for x in range(GRID_SIZE_W):
                obj = self.world_grid[y][x]
                if isinstance(obj, BotGenome):
                    self.draw_bot(obj)
                    count_of_bots += 1
                elif isinstance(obj, Food):
                    self.draw_bot(obj)

        self.draw_cycle_count()
        self.draw_bot_count(count_of_bots)
        self.draw_temp_count()
        self.draw_season_info()


class App:
    def __init__(self):
        self.run = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Bot Simulation')
        self.world = World(self.screen)
        

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def update(self):
        self.world.update()

    def draw(self):
        # Обновление дисплея
        self.screen.fill(BKG_color)

        self.world.draw()

        pygame.display.flip()

    def loop(self):
        while self.run:
            self.event()
            self.update()
            self.draw()

            # print(f'Цикл номер: {self.world.cycle_count}')
            # pygame.time.delay(100)  # Задержка в 100 миллисекунд
        pygame.quit()


if __name__ == '__main__':
    app = App()
    app.loop()
