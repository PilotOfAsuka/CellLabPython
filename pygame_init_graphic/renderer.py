from camera.camera import camera
from misc import environment
from misc import vars as v
from misc import colors as c
from pygame_init_graphic.pygame_init import pg, surface


# Кэшируем преобразование RGB -> цвет поверхности pygame, чтобы не делать map_rgb на каждой клетке.
color_cache = {}
signal_color_cache = {}
background_surface = None
background_signature = None
light_overlay_surface = None
light_overlay_signature = None
STATIC_LIGHT_CYCLE = 0
SIGNAL_RENDER_BUCKET_SIZE = 12
LIGHT_OVERLAY_STRIP_H = 10


def map_color(color):
    mapped_color = color_cache.get(color)
    if mapped_color is None:
        mapped_color = surface.map_rgb(color)
        color_cache[color] = mapped_color
    return mapped_color


def draw_tile_pixels(pixels, x, y, color, cell_size, viewport_w, viewport_h):
    # Обрезаем блок клетки по краю игрового поля, чтобы пиксели не залезали в GUI-панель.
    screen_x = (x + camera.x_offset) * cell_size
    screen_y = (y + camera.y_offset) * cell_size
    x1 = max(0, screen_x)
    y1 = max(0, screen_y)
    x2 = min(viewport_w, screen_x + cell_size)
    y2 = min(viewport_h, screen_y + cell_size)

    if x1 >= x2 or y1 >= y2:
        return False

    pixels[x1:x2, y1:y2] = map_color(color)
    return True


def draw_tile_mapped_pixels(pixels, x, y, mapped_color, cell_size, viewport_w, viewport_h):
    # Такой же блок, но цвет уже переведен в формат поверхности.
    screen_x = (x + camera.x_offset) * cell_size
    screen_y = (y + camera.y_offset) * cell_size
    x1 = max(0, screen_x)
    y1 = max(0, screen_y)
    x2 = min(viewport_w, screen_x + cell_size)
    y2 = min(viewport_h, screen_y + cell_size)

    if x1 >= x2 or y1 >= y2:
        return False

    pixels[x1:x2, y1:y2] = mapped_color
    return True


def draw_cell_pixels(pixels, obj, cell_size, viewport_w, viewport_h):
    x, y = obj.position
    color = get_render_cell_color(obj.color, x, y)
    return draw_tile_pixels(pixels, x, y, color, cell_size, viewport_w, viewport_h)


def get_signal_bucket_from_value(signal):
    return signal // SIGNAL_RENDER_BUCKET_SIZE


def get_signal_bucket(index):
    if not environment.signal_map:
        return 0
    return get_signal_bucket_from_value(environment.signal_map[index])


def get_render_cell_color(base_color, x, y):
    humidity = environment.get_humidity(x, y)
    color = base_color

    if humidity > 14:
        color = environment.blend_color(color, c.HUMIDITY_COLOR, min(0.28, humidity / 260))
    return environment.apply_light(color, environment.get_light(x, y, STATIC_LIGHT_CYCLE))


def get_object_mapped_color(obj, x, y):
    cache_key = (obj.color, x, y, environment.environment_version)

    if obj._render_cache_key != cache_key:
        obj._render_cache_key = cache_key
        obj._render_mapped_color = map_color(get_render_cell_color(obj.color, x, y))

    return obj._render_mapped_color


def get_signal_mapped_color(x, y):
    index = environment.map_index(x, y)
    signal = environment.signal_map[index] if environment.signal_map else 0
    if signal <= 0:
        return None

    signal_bucket = max(1, get_signal_bucket_from_value(signal))
    cache_key = signal_bucket
    mapped_color = signal_color_cache.get(cache_key)
    if mapped_color is None:
        signal_power = signal_bucket * SIGNAL_RENDER_BUCKET_SIZE
        color = environment.blend_color(c.BKG_COLOR, c.SIGNAL_COLOR, min(0.62, signal_power / 140))
        mapped_color = map_color(color)
        signal_color_cache[cache_key] = mapped_color
    return mapped_color


def build_background_surface():
    viewport_w = v.width - v.gui_offset
    viewport_h = v.height
    bg_surface = pg.Surface((viewport_w, viewport_h))
    bg_surface.fill(c.BKG_COLOR)
    pixels = pg.PixelArray(bg_surface)
    local_color_cache = {}

    try:
        for y in range(v.GRID_SIZE_H):
            y1 = y * v.CELL_SIZE
            y2 = min(viewport_h, y1 + v.CELL_SIZE)
            for x in range(v.GRID_SIZE_W):
                x1 = x * v.CELL_SIZE
                x2 = min(viewport_w, x1 + v.CELL_SIZE)
                color = environment.get_background_color(x, y, STATIC_LIGHT_CYCLE)
                mapped_color = local_color_cache.get(color)
                if mapped_color is None:
                    mapped_color = bg_surface.map_rgb(color)
                    local_color_cache[color] = mapped_color
                if v.CELL_SIZE == 1:
                    pixels[x1, y1] = mapped_color
                else:
                    pixels[x1:x2, y1:y2] = mapped_color
    finally:
        del pixels

    return bg_surface


def get_background_surface():
    global background_surface, background_signature

    signature = (v.GRID_SIZE_W, v.GRID_SIZE_H, v.CELL_SIZE, environment.environment_version)
    if background_surface is None or background_signature != signature:
        background_surface = build_background_surface()
        background_signature = signature
        signal_color_cache.clear()
    return background_surface


def get_light_overlay_surface():
    global light_overlay_surface, light_overlay_signature

    viewport_w = v.width - v.gui_offset
    viewport_h = v.height
    cell_size = max(1, v.CELL_SIZE * camera.scale)
    daylight_bucket = int(environment.get_daylight() * 80)
    signature = (viewport_w, viewport_h, v.GRID_SIZE_H, cell_size, camera.y_offset, daylight_bucket)
    if light_overlay_surface is not None and light_overlay_signature == signature:
        return light_overlay_surface

    overlay = pg.Surface((viewport_w, viewport_h), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 0))
    daylight = daylight_bucket / 80

    for screen_y in range(0, viewport_h, LIGHT_OVERLAY_STRIP_H):
        world_y = screen_y // cell_size - camera.y_offset
        world_y = max(0, min(v.GRID_SIZE_H - 1, world_y))
        height_factor = 1 - world_y / max(1, v.GRID_SIZE_H - 1)
        day_darkness = int((1 - daylight) * 85)
        depth_darkness = int((1 - height_factor) * 35)
        alpha = max(0, min(120, day_darkness + depth_darkness))
        pg.draw.rect(overlay, (0, 0, 0, alpha), (0, screen_y, viewport_w, LIGHT_OVERLAY_STRIP_H))

    light_overlay_surface = overlay
    light_overlay_signature = signature
    return light_overlay_surface


def draw_light_overlay():
    surface.blit(get_light_overlay_surface(), (0, 0))


def draw_world_background():
    viewport_w = v.width - v.gui_offset
    viewport_h = v.height
    bg_surface = get_background_surface()

    if camera.scale == 1:
        surface.blit(bg_surface, (0, 0))
        return

    surface.fill(c.BKG_COLOR, pg.Rect(0, 0, viewport_w, viewport_h))
    source_rect = pg.Rect(
        max(0, -camera.x_offset * v.CELL_SIZE),
        max(0, -camera.y_offset * v.CELL_SIZE),
        max(1, viewport_w // camera.scale),
        max(1, viewport_h // camera.scale),
    )
    source_rect.clamp_ip(bg_surface.get_rect())
    scaled = pg.transform.scale(
        bg_surface.subsurface(source_rect),
        (source_rect.width * camera.scale, source_rect.height * camera.scale),
    )
    surface.blit(scaled, (0, 0))


def draw_object(obj):
    pixels = pg.PixelArray(surface)
    try:
        draw_cell_pixels(pixels, obj, v.CELL_SIZE * camera.scale, v.width - v.gui_offset, v.height)
    finally:
        del pixels


def draw_surface():
    # Один PixelArray на кадр дешевле, чем отдельный pg.draw.rect для каждой живой клетки.
    draw_world_background()
    cell_size = v.CELL_SIZE * camera.scale
    x_offset = camera.x_offset
    y_offset = camera.y_offset
    viewport_w = v.width - v.gui_offset
    viewport_h = v.height
    start_x = max(0, -x_offset)
    start_y = max(0, -y_offset)
    end_x = min(v.GRID_SIZE_W, start_x + viewport_w // cell_size + 1)
    end_y = min(v.GRID_SIZE_H, start_y + viewport_h // cell_size + 1)
    drawn_objects = 0
    pixels = pg.PixelArray(surface)

    try:
        if cell_size == 1 and x_offset == 0 and y_offset == 0:
            # Самый частый тяжелый режим: весь мир 1:1 на экране.
            # Здесь active_objects уже очищен симуляцией, поэтому можно не проверять каждую точку через world_grid.
            grid = v.world_grid
            grid_w = v.GRID_SIZE_W
            for signal_index in environment.active_signal_indexes:
                x = signal_index % grid_w
                y = signal_index // grid_w
                if grid[y][x] is not None:
                    continue
                mapped_color = get_signal_mapped_color(x, y)
                if mapped_color is not None:
                    pixels[x, y] = mapped_color

            for obj in v.active_objects:
                x, y = obj.position
                pixels[x, y] = get_object_mapped_color(obj, x, y)
                drawn_objects += 1

        elif cell_size == 1:
            # Для размера 1x1 прямое присваивание пикселя быстрее, чем срез PixelArray.
            for signal_index in environment.active_signal_indexes:
                x, y = environment.get_xy(signal_index)
                if not (start_x <= x < end_x and start_y <= y < end_y):
                    continue
                if v.world_grid[y][x] is not None:
                    continue
                mapped_color = get_signal_mapped_color(x, y)
                if mapped_color is None:
                    continue

                screen_x = x + x_offset
                screen_y = y + y_offset
                if 0 <= screen_x < viewport_w and 0 <= screen_y < viewport_h:
                    pixels[screen_x, screen_y] = mapped_color

            for obj in v.active_objects:
                x, y = obj.position
                if not (start_x <= x < end_x and start_y <= y < end_y):
                    continue
                if v.world_grid[y][x] is not obj:
                    continue

                screen_y = y + y_offset
                if screen_y < 0 or screen_y >= viewport_h:
                    continue

                screen_x = x + x_offset
                if screen_x < 0 or screen_x >= viewport_w:
                    continue

                pixels[screen_x, screen_y] = get_object_mapped_color(obj, x, y)
                drawn_objects += 1

        else:
            for signal_index in environment.active_signal_indexes:
                x, y = environment.get_xy(signal_index)
                if not (start_x <= x < end_x and start_y <= y < end_y):
                    continue
                if v.world_grid[y][x] is not None:
                    continue
                mapped_color = get_signal_mapped_color(x, y)
                if mapped_color is not None:
                    draw_tile_mapped_pixels(pixels, x, y, mapped_color, cell_size, viewport_w, viewport_h)

            for obj in v.active_objects:
                x, y = obj.position
                if not (start_x <= x < end_x and start_y <= y < end_y):
                    continue
                if v.world_grid[y][x] is not obj:
                    continue

                mapped_color = get_object_mapped_color(obj, x, y)
                if draw_tile_mapped_pixels(pixels, x, y, mapped_color, cell_size, viewport_w, viewport_h):
                    drawn_objects += 1
    finally:
        del pixels

    draw_light_overlay()
    return drawn_objects
