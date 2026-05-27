from camera.camera import camera
from misc import vars as v
from pygame_init_graphic.pygame_init import pg, surface


# Кэшируем преобразование RGB -> цвет поверхности pygame, чтобы не делать map_rgb на каждой клетке.
color_cache = {}


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


def draw_cell_pixels(pixels, obj, cell_size, viewport_w, viewport_h):
    x, y = obj.position
    return draw_tile_pixels(pixels, x, y, obj.color, cell_size, viewport_w, viewport_h)


def draw_object(obj):
    pixels = pg.PixelArray(surface)
    try:
        draw_cell_pixels(pixels, obj, v.CELL_SIZE * camera.scale, v.width - v.gui_offset, v.height)
    finally:
        del pixels


def draw_surface():
    # Один PixelArray на кадр дешевле, чем отдельный pg.draw.rect для каждой живой клетки.
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
        if cell_size == 1:
            # Для размера 1x1 прямое присваивание пикселя быстрее, чем срез PixelArray.
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

                pixels[screen_x, screen_y] = map_color(obj.color)
                drawn_objects += 1

            return drawn_objects

        for obj in v.active_objects:
            x, y = obj.position
            if not (start_x <= x < end_x and start_y <= y < end_y):
                continue
            if v.world_grid[y][x] is not obj:
                continue

            if draw_cell_pixels(pixels, obj, cell_size, viewport_w, viewport_h):
                drawn_objects += 1
    finally:
        del pixels

    return drawn_objects
