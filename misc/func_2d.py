from misc.vars import move_directions, world_grid_2d, GRID_SIZE_H, GRID_SIZE_W


def get_free_adjacent_2d_positions(position):
    x, y = position
    free_positions = []
    for dx, dy in move_directions:
        nx = x + dx if -1 < x + dx < GRID_SIZE_W else x
        ny = y + dy if -1 < y + dy < GRID_SIZE_H else y
        if world_grid_2d[get_index(nx, ny)] is None:
            free_positions.append((nx, ny))
    return free_positions  # Возврат свободных позиций


def get_coord_from_index(index):
    y = index // GRID_SIZE_W
    x = index % GRID_SIZE_W

    return x, y


def get_index(x, y):
    return y * GRID_SIZE_W + x