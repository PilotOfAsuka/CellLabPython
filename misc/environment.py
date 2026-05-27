import math
import random

from misc import colors as c
from misc import vars as v


humidity_map = bytearray()
signal_map = bytearray()
active_signal_indexes = set()
environment_version = 0


def clamp(value, min_value=0, max_value=100):
    return max(min(int(value), max_value), min_value)


def map_index(x, y):
    return y * v.GRID_SIZE_W + x


def get_xy(index):
    return index % v.GRID_SIZE_W, index // v.GRID_SIZE_W


def get_layer_value(layer, x, y):
    if not (0 <= x < v.GRID_SIZE_W and 0 <= y < v.GRID_SIZE_H):
        return 0
    if not layer:
        return 0
    return layer[map_index(x, y)]


def make_blob_value(x, y, centers):
    value = 0
    for cx, cy, radius, strength in centers:
        distance = math.hypot(x - cx, y - cy)
        if distance < radius:
            value += int((1 - distance / radius) * strength)
    return clamp(value)


def reset_environment():
    global humidity_map, signal_map, active_signal_indexes, environment_version

    size = v.GRID_SIZE_W * v.GRID_SIZE_H
    humidity_map = bytearray(size)
    signal_map = bytearray(size)
    active_signal_indexes = set()
    environment_version += 1

    rng = random.Random(v.GRID_SIZE_W * 31 + v.GRID_SIZE_H * 17 + v.CELL_SIZE)
    humidity_centers = [
        (rng.randrange(v.GRID_SIZE_W), rng.randrange(v.GRID_SIZE_H),
         rng.randrange(18, 58), rng.randrange(45, 100))
        for _ in range(10)
    ]

    for y in range(v.GRID_SIZE_H):
        for x in range(v.GRID_SIZE_W):
            humidity_map[map_index(x, y)] = make_blob_value(x, y, humidity_centers)


def update_environment(cycle):
    # Следы затухают редко и только по активным позициям, поэтому не надо сканировать всю карту.
    if cycle % 4 != 0:
        return

    for index in tuple(active_signal_indexes):
        value = signal_map[index]
        if value <= 3:
            signal_map[index] = 0
            active_signal_indexes.discard(index)
        else:
            signal_map[index] = value - 3


def get_humidity(x, y):
    return get_layer_value(humidity_map, x, y)


def get_signal(x, y):
    return get_layer_value(signal_map, x, y)


def leave_signal(position, amount=18):
    x, y = position
    if not (0 <= x < v.GRID_SIZE_W and 0 <= y < v.GRID_SIZE_H):
        return

    index = map_index(x, y)
    signal_map[index] = clamp(signal_map[index] + amount)
    active_signal_indexes.add(index)


def get_daylight(cycle=None):
    current_cycle = v.global_vars["count_of_cycle"] if cycle is None else cycle
    return 0.65 + 0.35 * math.sin(current_cycle / 1200)


def get_light_bucket(cycle=None, bucket_size=120):
    current_cycle = v.global_vars["count_of_cycle"] if cycle is None else cycle
    return current_cycle // bucket_size


def get_light(x, y, cycle=None):
    # Свет сильнее сверху, слабее внизу, а влажные зоны работают как простая облачность.
    height_factor = 1 - y / max(1, v.GRID_SIZE_H - 1)
    cloud_shadow = get_humidity(x, y) * 0.22
    return clamp(height_factor * 100 * get_daylight(cycle) - cloud_shadow, 5, 100)


def blend_color(base_color, overlay_color, alpha):
    alpha = max(0, min(alpha, 1))
    return tuple(int(base_color[i] * (1 - alpha) + overlay_color[i] * alpha) for i in range(3))


def apply_light(color, light):
    factor = 0.45 + light / 150
    return tuple(clamp(channel * factor, 0, 255) for channel in color)


def get_background_color(x, y, cycle=None):
    humidity = get_humidity(x, y)
    light = get_light(x, y, cycle)
    color = c.BKG_COLOR

    if humidity > 8:
        color = blend_color(color, c.HUMIDITY_COLOR, min(0.55, humidity / 160))
    return apply_light(color, light)


def get_cell_color(base_color, x, y, cycle=None):
    humidity = get_humidity(x, y)
    signal = get_signal(x, y)
    light = get_light(x, y, cycle)
    color = base_color

    if humidity > 14:
        color = blend_color(color, c.HUMIDITY_COLOR, min(0.28, humidity / 260))
    if signal > 16:
        color = blend_color(color, c.SIGNAL_COLOR, min(0.30, signal / 220))
    return apply_light(color, light)


def get_signal_color(x, y):
    signal = get_signal(x, y)
    if signal <= 0:
        return None
    base = get_background_color(x, y)
    return blend_color(base, c.SIGNAL_COLOR, min(0.45, signal / 160))


reset_environment()
