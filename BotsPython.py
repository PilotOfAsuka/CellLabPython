import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20
GRID_SIZE = WIDTH // CELL_SIZE

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bot Simulation')

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

class BotGenome:
    def __init__(self, genome_size=64, food = 1000, x = 0, y = 0, color=(0, 255, 0)):
        # Инициализация генома с заданным размером
        self.genome = [random.randint(0, 63) for _ in range(genome_size)]
        self.ptr = 0  # УТК (указатель текущей команды)
        self.food = food
        self.position = (x, y)
        self.color = color

    def execute_genome(self):
        command = self.genome[self.ptr]
        self.execute_command(command)


    def execute_command(self, command):
        # Выполнение команды в зависимости от числа
        #print(self.ptr, self.genome[self.ptr])
        if command in {20,21,22,23}:
            self.photosynthesis()
        elif command in {27,28,29,30,31}:
            self.move()
            self.food -= 1
        elif command == 33:
            self.how_many_food()

        else: 
            self.move_ptr_to()
        # Здесь могут быть другие команды

    def photosynthesis(self):
        # Пример команды "фотосинтез"
        self.food += 10
        self.move_ptr()
        #print("Выполняется фотосинтез")

    def how_many_food(self):
        food_index = (self.ptr + 1) % len(self.genome)
        next_ptr_index = (self.ptr + 2) % len(self.genome)
        next_next_ptr_index = (self.ptr + 3) % len(self.genome)
        food_genome = self.genome[food_index] * 15

        if self.food >= food_genome:
            self.ptr = (self.ptr + self.genome[next_ptr_index]) % len(self.genome)
        else:
            self.ptr = (self.ptr + self.genome[next_next_ptr_index]) % len(self.genome)
    def move(self):
         # Модификация для движения бота
        move_dir_index = (self.ptr + 1) % len(self.genome)
        move_dir = self.genome[move_dir_index] % 8
        dx, dy = 0, 0
        if move_dir == 0: dx = 1
        elif move_dir == 1: dx = -1
        elif move_dir == 2: dy = 1
        elif move_dir == 3: dy = -1
        self.food -= 1
        # Обновление позиции бота
        x, y = self.position
        new_x, new_y = ((x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE)
        if not any(bot.position == (new_x, new_y) for bot in bots):  # Проверить, занята ли клетка
            self.position = new_x, new_y
            self.move_ptr()
        else:
            dir_index = (self.ptr + 5) % len(self.genome)
            self.ptr = (self.ptr + self.genome[dir_index]) % len(self.genome)
            



    def rotate(self):
        rotate_dir_index = (self.ptr + 1) % len(self.genome)
        rotate_dir = self.genome[rotate_dir_index] % 8
        # Пример команды "Rotate"
        print(f"Бот повернулся на {rotate_dir} ")
        return(rotate_dir)

    def move_ptr_to(self):
        # Перемещение УТК к следующей команде
        self.ptr = (self.ptr + self.genome[self.ptr]) % len(self.genome)

    def move_ptr(self):
        # Перемещение УТК к следующей команде
        self.ptr = (self.ptr + 1) % len(self.genome)

    def mutate(self, position, new_value):
        # Мутация: изменение значения в определенной ячейке генома
        self.genome[position] = new_value
        print("Произошла мутация")

    def reproduce(self, bots):
        if not self.is_space_to_reproduce(bots):
            return None  # Нет места для деления
        else:
            # Создание нового бота с похожим геномом
            new_genome = self.genome[:]
            mutation_index = random.randint(0, len(new_genome) - 1)
            new_genome[mutation_index] = random.randint(0, 63)
            new_color = (0, max(self.color[1] - 10, 0), 0)  # Уменьшаем зеленый компонент
            new_bot = BotGenome(genome_size=len(new_genome), food=self.food // 2, x=self.position[0], y=self.position[1], color=new_color)
            self.food = self.food // 2  # Поделить энергию между родителем и потомком
            return new_bot

    def is_space_to_reproduce(self, bots):
        adjacent_positions = [
            ((self.position[0] + dx) % GRID_SIZE, (self.position[1] + dy) % GRID_SIZE)
            for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)
        ]
        return any(pos not in [bot.position for bot in bots] for pos in adjacent_positions)




def draw_bots(bots):
    for bot in bots:
        x, y = bot.position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, bot.color, rect)

# Создание нескольких ботов
bots = [BotGenome(x=random.randint(0, GRID_SIZE - 1), y=random.randint(0, GRID_SIZE - 1)) for _ in range(10)]
# Создание бота с геномом и запуск его выполнения для демонстрации



# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    new_bots = []
    for bot in bots:
        # Выполнение команды генома для каждого бота
        bot.execute_genome()
        if bot.food > 2000 and bot.is_space_to_reproduce(bots):
            new_bot = bot.reproduce(bots)
            if new_bot:
                print("клетка поделилась")
                new_bots.append(new_bot)


    # Удаление ботов с нулевым или отрицательным уровнем энергии
    bots = [bot for bot in bots if bot.food >= 0]




    bots.extend(new_bots)

    screen.fill(WHITE)
    draw_grid()
    draw_bots(bots)
    pygame.display.flip()

