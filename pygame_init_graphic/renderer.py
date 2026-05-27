from camera.camera import camera
from misc.vars import CELL_SIZE, GRID_SIZE_H, GRID_SIZE_W, gui_offset, height, width, world_grid
from pygame_init_graphic.pygame_init import pg, surface


color_cache = {}


def draw_object(obj):
    x, y = obj.position
    size = CELL_SIZE * camera.scale
    rect = ((x + camera.x_offset) * size,
            (y + camera.y_offset) * size,
            size,
            size)
    surface.fill(obj.color, rect)


def draw_surface():
    cell_size = CELL_SIZE * camera.scale
    x_offset = camera.x_offset
    y_offset = camera.y_offset
    viewport_w = width - gui_offset
    viewport_h = height
    start_x = max(0, -x_offset)
    start_y = max(0, -y_offset)
    end_x = min(GRID_SIZE_W, start_x + viewport_w // cell_size + 1)
    end_y = min(GRID_SIZE_H, start_y + viewport_h // cell_size + 1)
    fill_rect = surface.fill
    drawn_objects = 0

    if cell_size == 1:
        pixels = pg.PixelArray(surface)
        try:
            for y in range(start_y, end_y):
                screen_y = y + y_offset
                row = world_grid[y]
                for x in range(start_x, end_x):
                    obj = row[x]
                    if obj is not None:
                        color = obj.color
                        mapped_color = color_cache.get(color)
                        if mapped_color is None:
                            mapped_color = surface.map_rgb(color)
                            color_cache[color] = mapped_color
                        pixels[x + x_offset, screen_y] = mapped_color
                        drawn_objects += 1
        finally:
            del pixels

        return drawn_objects

    for y in range(start_y, end_y):
        screen_y = (y + y_offset) * cell_size
        row = world_grid[y]
        for x in range(start_x, end_x):
            obj = row[x]
            if obj is not None:
                screen_x = (x + x_offset) * cell_size
                fill_rect(obj.color, (screen_x, screen_y, cell_size, cell_size))
                drawn_objects += 1

    return drawn_objects
