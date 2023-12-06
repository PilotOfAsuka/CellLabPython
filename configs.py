import func
import genome
import pygame
# Установка размеров окна
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
FPS = 60 # Ограничиваем кол-во FPS 

# Мир теперь состоит из клеточек
CELL_SIZE = 2 # Размер клетки изменяя этот параметр меняется масштаб
GRID_SIZE_W = (width - 200) // CELL_SIZE # Задаем ширину сетки мира (-200 Это отступ для интерфеса)
GRID_SIZE_H = height // CELL_SIZE # Задаем высоту сетки мира 
START_NUM_OF_CELL = 100 # Стартовое число клеток при создании мира 
gen_size = 64 # Размер гена


# Инициализация двумерного массива мира
world_grid = [[None for _ in range(GRID_SIZE_W)] for _ in range(GRID_SIZE_H)] # Мир в котором живут клетки

# Инициализация начальных клеток в мире
for _ in range(START_NUM_OF_CELL):
    x, y = func.random_position(world_grid)
    bot = genome.BotGenome(x=x, y=y)
    world_grid[y][x] = bot
 
# Кортеж направлений
move_directions = (
    (0, -1),  # Вверх
    (1,-1),   # Вверх и вправо
    (1, 0),  # Вправо
    (1, 1),  # Вправо и вниз
    (0, 1),  # Вниз
    (-1, 1), # Вниз и лево
    (-1, 0),  # Влево
    (-1, -1)  # Влево и вверх
)
#>>>>>>>>>>><<<<<<<<<<<