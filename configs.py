import func
import genome
import pygame
# Установка размеров окна
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
FPS = 60
# Мир теперь состоит из клеточек
CELL_SIZE = 3 # размер клетки изменяя этот параметр меняется масштаб
GRID_SIZE_W = width // CELL_SIZE
GRID_SIZE_H = height // CELL_SIZE
START_NUM_OF_CELL = 100
# Инициализация двумерного массива мира
world_grid = [[None for _ in range(GRID_SIZE_W)] for _ in range(GRID_SIZE_H)]
for _ in range(START_NUM_OF_CELL):
    x, y = func.random_position(world_grid)
    bot = genome.BotGenome(world_grid ,x=x, y=y)
    world_grid[y][x] = bot
    
    
    
# кортеж направлений
move_actions = (
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