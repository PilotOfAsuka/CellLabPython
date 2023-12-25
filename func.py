import random
import configs as cfg
import pygame
import numpy as np
import math


count_of_cell = 0 # Счетчик кол-во клеток
count_of_food = 0 # Счетчик кол-во органики
count_of_cicle = 0 # Счетчик кол-во циклов
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
def get_free_adjacent_positions(position, world_grid):
    x, y = position
    free_positions = []
    for dx, dy in cfg.move_directions:
        nx = x + dx if -1 < x + dx < cfg.GRID_SIZE_W else x
        ny = y + dy if -1 < y + dy < cfg.GRID_SIZE_H else y
        if world_grid[ny][nx] is None:
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
    
# Функция погоды
# Принимает размер мира, текущий цикл 
# Возвращает Температуру, силу света, и положение солнца
def weather_simulation(world_size_x, world_size_y, cycle):
    # Температура
    min_temp = -15 # Минимальное значение 
    max_temp = 15 # Максимальное значение
    t_change_rate = 10000 #Изменять каждые кол-во циклов
    # Рассчитываем угол для синусоиды в пределах от 0 до 2π
    deegres = (cycle / t_change_rate) * (2 * math.pi)
    # Используем синусоиду для моделирования изменения температуры
    t_sin = math.sin(deegres)
    # Масштабируем синусоиду к диапазону от минимальной до максимальной температуры
    temp = min_temp + (t_sin + 1) * (max_temp - min_temp) / 2

    # Положение солнца зависит от цикла, оно движется от левого верхнего до правого нижнего угла
    change_every = 100  # изменять каждые _ циклов
    sun_x = (cycle // change_every) % cfg.width-cfg.gui_ofset
    sun_y = (cycle // change_every) % cfg.height

    # Сила освещенности зависит от положения солнца (простое представление)
    illumination = np.clip(100 - (abs(sun_x - world_size_x/2) + abs(sun_y - world_size_y/2)), 0, 100)

    return temp, illumination, (sun_x, sun_y)
# Функция обновления погоды
def update_weather():
    temperature, illumination, sun_coord = weather_simulation(cfg.GRID_SIZE_W,cfg.GRID_SIZE_H, count_of_cicle)
    print(sun_coord)
    return int(temperature), int(illumination), sun_coord

# функция нормализации значения один диапазон в другой (например кол-во потребления энергии от 0 до 200 зависит от температуры, или другого значенмия)
def normalize_value(input_value, original_min, original_max, target_min, target_max):
    
    # Преобразуем исходное значение в диапазоне от 0 до 1
    normalized = (input_value - original_min) / (original_max - original_min)
    # Преобразуем нормализованное значение в целевой диапазон
    return int(normalized * (target_max - target_min) + target_min)
# Функция расчета эвклидово растояния 
def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return int(distance)

