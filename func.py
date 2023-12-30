import random
import configs as cfg
import pygame
import numpy as np
import math
import gui


# Здесь можно хранить одиночные функции

# Функция для генерации случайной свободной позиции
def random_position(world_grid):
    x = random.randint(0, cfg.GRID_SIZE_W - 1)
    y = random.randint(0, cfg.GRID_SIZE_H - 1)
    while world_grid[y][x] is not None:
        x = random.randint(0, cfg.GRID_SIZE_W - 1)
        y = random.randint(0, cfg.GRID_SIZE_H - 1)
    return x, y  # Возврат случайных свободных позиций

                    
# функция получения свободного места вокруг
def get_free_adjacent_positions(position, world_grid):
    x, y = position
    free_positions = []
    for dx, dy in cfg.move_directions:
        nx = x + dx if -1 < x + dx < cfg.GRID_SIZE_W else x
        ny = y + dy if -1 < y + dy < cfg.GRID_SIZE_H else y
        if world_grid[ny][nx] is None:
            free_positions.append((nx, ny))
    return free_positions  # Возврат свободных позиций


# Функция мутации
def mutate_genome(genome):
    mutation_chance = 0.1  # Шанс мутации для каждого гена
    for i in range(len(genome)):
        if random.random() < mutation_chance:
            genome[i] = random.randint(0, 63)  # Новое случайное значение гена


# Функция мутации
def mutate_genome_new(genome, mutation_chance, new_genome):
    """
    genome = Принимает на вход геном
    Mutation_chance = шанс мутации
    new_genome = новое значение
    """
    i = random.randint(0, 63)
    if random.random() < mutation_chance:
        genome[i] = new_genome  # Новое значение гена


# Функция отрисовки объектов
def draw_obj(obj):
    x, y = obj.position
    rect = pygame.Rect((x + gui.camera.x_offset) * (cfg.CELL_SIZE * gui.camera.scale),
                       (y + gui.camera.y_offset) * (cfg.CELL_SIZE * gui.camera.scale),
                       (cfg.CELL_SIZE * gui.camera.scale), (cfg.CELL_SIZE * gui.camera.scale))
    pygame.draw.rect(cfg.screen, obj.color, rect)
    

def weather_simulation(cycle):
    """
    На вход принимает, текущий цикл.
    Возвращает Температуру и Положение солнца по х и у
    """
    # Температура
    min_temp = -15  # Минимальное значение
    max_temp = 15  # Максимальное значение
    t_change_rate = 10000  # Изменять каждые кол-во циклов
    # Рассчитываем угол для синусоиды в пределах от 0 до 2π
    degree = (cycle / t_change_rate) * (2 * math.pi)
    # Используем синусоиду для моделирования изменения температуры
    t_sin = math.sin(degree)
    # Масштабируем синусоиду к диапазону от минимальной до максимальной температуры
    temp = min_temp + (t_sin + 1) * (max_temp - min_temp) / 2

    # Положение солнца зависит от цикла, оно движется от левого верхнего до правого нижнего угла
    change_every = 10  # изменять каждые _ циклов
    sun_x = (cycle // change_every) % (cfg.width-cfg.gui_offset)
    sun_y = (cycle // change_every) % cfg.height
    return int(temp), (sun_x, sun_y)


# функция нормализации значения один диапазон в другой
def normalize_value(input_value, original_min, original_max, target_min, target_max):
    """
    input_value= Входное значение
    original_min= Минимум входного значения
    original_max= Максимум входного значения
    target_min= Минимум выходного значения
    target_max= Максимум выходного значения
    Функция возвращает значение в диапазоне от target_min и до target_max
    """
    # Преобразуем исходное значение в диапазоне от 0 до 1
    normalized = (input_value - original_min) / (original_max - original_min)
    # Преобразуем нормализованное значение в целевой диапазон
    return int(normalized * (target_max - target_min) + target_min)


# Функция расчета евклидово расстояния
def euclidean_distance(point1, point2):
    """
    Функция расчёта евклидово расстояния между двумя точками
    point1= точка номер 1
    point2= точка номер 2
    """
    x1, y1 = point1
    x2, y2 = point2
    distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return int(distance)
