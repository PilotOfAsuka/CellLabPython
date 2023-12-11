import random
import configs as cfg
import pygame
import numpy as np


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
# Принимает размер мира, текущий цикл и количество органики в данный момент
# Возвращает Температуру, силу света, и положение солнца
def weather_simulation(world_size_x, world_size_y, cycle, organic_amount):
    # Температура зависит от количества органики и цикла (для простоты используем простую функцию)
    # Основное изменение температуры (от -15 до 15 и обратно) с использованием синусоидальной функции
    base_temperature = 15 * np.sin(np.radians(cycle % 360))
    # Корректировка температуры на основе количества еды (небольшое влияние)
    food_temperature_effect = (organic_amount / 1000) - 0.5  # Например, масштабирование эффекта от -0.5 до +0.5
    # Итоговая температура с учетом корректировки
    temperature = np.clip(base_temperature + food_temperature_effect, -15, 15)

    # Положение солнца зависит от цикла, оно движется от левого верхнего до правого нижнего угла
    change_every = 100  # изменять каждые _ циклов
    sun_x = (cycle // change_every) % world_size_x
    sun_y = (cycle // change_every) % world_size_y

    # Сила освещенности зависит от положения солнца (простое представление)
    illumination = np.clip(100 - (abs(sun_x - world_size_x/2) + abs(sun_y - world_size_y/2)), 0, 100)

    return temperature, illumination, (sun_x, sun_y)

def update_weather():
    temperature, illumination, sun_coord = weather_simulation(cfg.GRID_SIZE_W,cfg.GRID_SIZE_H, count_of_cicle,count_of_food)
    return int(temperature), int(illumination), sun_coord

# функция чормализации значения один диапазон в другой (например кол-во потребления энергии от 0 до 200 зависит от температуры, или другого значенмия)
def normalize_value(input_value, original_min, original_max, target_min, target_max):
    
    # Преобразуем исходное значение в диапазоне от 0 до 1
    normalized = (input_value - original_min) / (original_max - original_min)
    # Преобразуем нормализованное значение в целевой диапазон
    return int(normalized * (target_max - target_min) + target_min)

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return int(distance)

