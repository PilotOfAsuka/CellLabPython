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
BACKGROUND_LIGHT_STEP = 120


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
    color = environment.get_cell_color(obj.color, x, y)
    return draw_tile_pixels(pixels, x, y, color, cell_size, viewport_w, viewport_h)


def get_signal_bucket(index):
    if not environment.signal_map:
        return 0
    return environment.signal_map[index] // 8


def get_light_bucket():
    return environment.get_light_bucket(bucket_size=BACKGROUND_LIGHT_STEP)


def get_object_mapped_color(obj, x, y, light_bucket):
    index = environment.map_index(x, y)
    signal_bucket = get_signal_bucket(index)
    cache_key = (obj.color, x, y, environment.environment_version, light_bucket, signal_bucket)

    if getattr(obj, "_render_cache_key", None) != cache_key:
        cycle = light_bucket * BACKGROUND_LIGHT_STEP
        obj._render_cache_key = cache_key
        obj._render_mapped_color = map_color(environment.get_cell_color(obj.color, x, y, cycle))

    return obj._render_mapped_color


def get_signal_mapped_color(x, y, light_bucket):
    index = environment.map_index(x, y)
    signal = environment.signal_map[index] if environment.signal_map else 0
    if signal <= 0:
        return None

    cache_key = (index, signal, environment.environment_version, light_bucket)
    mapped_color = signal_color_cache.get(cache_key)
    if mapped_color is None:
        cycle = light_bucket * BACKGROUND_LIGHT_STEP
        base = environment.get_background_color(x, y, cycle)
        color = environment.blend_color(base, c.SIGNAL_COLOR, min(0.45, signal / 160))
        mapped_color = map_color(color)
        signal_color_cache[cache_key] = mapped_color
    return mapped_color


def build_background_surface(light_bucket):
    viewport_w = v.width - v.gui_offset
    viewport_h = v.height
    bg_surface = pg.Surface((viewport_w, viewport_h))
    bg_surface.fill(c.BKG_COLOR)
    pixels = pg.PixelArray(bg_surface)
    local_color_cache = {}
    cycle = light_bucket * BACKGROUND_LIGHT_STEP

    try:
        for y in range(v.GRID_SIZE_H):
            y1 = y * v.CELL_SIZE
            y2 = min(viewport_h, y1 + v.CELL_SIZE)
            for x in range(v.GRID_SIZE_W):
                x1 = x * v.CELL_SIZE
                x2 = min(viewport_w, x1 + v.CELL_SIZE)
                color = environment.get_background_color(x, y, cycle)
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

    light_bucket = get_light_bucket()
    signature = (v.GRID_SIZE_W, v.GRID_SIZE_H, v.CELL_SIZE, environment.environment_version, light_bucket)
    if background_surface is None or background_signature != signature:
        background_surface = build_background_surface(light_bucket)
        background_signature = signature
        signal_color_cache.clear()
    return background_surface


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
    light_bucket = get_light_bucket()
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
        if cell_size == 1:
            # Для размера 1x1 прямое присваивание пикселя быстрее, чем срез PixelArray.
            for signal_index in tuple(environment.active_signal_indexes):
                x, y = environment.get_xy(signal_index)
                if not (start_x <= x < end_x and start_y <= y < end_y):
                    continue
                if v.world_grid[y][x] is not None:
                    continue
                mapped_color = get_signal_mapped_color(x, y, light_bucket)
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

                pixels[screen_x, screen_y] = get_object_mapped_color(obj, x, y, light_bucket)
                drawn_objects += 1

            return drawn_objects

        for signal_index in tuple(environment.active_signal_indexes):
            x, y = environment.get_xy(signal_index)
            if not (start_x <= x < end_x and start_y <= y < end_y):
                continue
            if v.world_grid[y][x] is not None:
                continue
            mapped_color = get_signal_mapped_color(x, y, light_bucket)
            if mapped_color is not None:
                draw_tile_mapped_pixels(pixels, x, y, mapped_color, cell_size, viewport_w, viewport_h)

        for obj in v.active_objects:
            x, y = obj.position
            if not (start_x <= x < end_x and start_y <= y < end_y):
                continue
            if v.world_grid[y][x] is not obj:
                continue

            mapped_color = get_object_mapped_color(obj, x, y, light_bucket)
            if draw_tile_mapped_pixels(pixels, x, y, mapped_color, cell_size, viewport_w, viewport_h):
                drawn_objects += 1
    finally:
        del pixels

    return drawn_objects
