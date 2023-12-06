import random
import configs as cfg
import pygame
#Здесь можно хранить одиночные функции

# Функция для генерации случайной свободной позиции
def random_position(world_grid):
    x = random.randint(0, cfg.GRID_SIZE_W - 1)
    y = random.randint(0, cfg.GRID_SIZE_H - 1)
    while world_grid[y][x] is not None:
        x = random.randint(0, cfg.GRID_SIZE_W - 1)
        y = random.randint(0, cfg.GRID_SIZE_H - 1)
    return x, y #Возврат случайных свободных позиций

                    
# функция получения свободного места вокруг
def get_free_adjacent_positions(position):
    x, y = position
    free_positions = []
    for dx, dy in cfg.move_directions:
        nx = (x + dx) % cfg.GRID_SIZE_W
        ny = y + dy if -1 < y + dy < cfg.GRID_SIZE_H else y
        if cfg.world_grid[ny][nx] is None:
            free_positions.append((nx, ny))
    return free_positions # Возврат свободных позиций

# функция мутации
def mutate_genome(genome):
    mutation_chance = 0.05  # Шанс мутации для каждого гена
    for i in range(len(genome)):
        if random.random() < mutation_chance:
            genome[i] = random.randint(0, 63)  # Новое случайное значение гена

# Функция отрисовки объектов
def draw_obj(obj):
    x, y = obj.position
    rect = pygame.Rect(x * cfg.CELL_SIZE, y * cfg.CELL_SIZE, cfg.CELL_SIZE, cfg.CELL_SIZE)
    pygame.draw.rect(cfg.screen, obj.color, rect)